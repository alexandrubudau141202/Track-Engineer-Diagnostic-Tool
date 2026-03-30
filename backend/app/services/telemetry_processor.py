"""
Telemetry Processor
Converts raw telemetry data into actionable metrics and anomaly detection
"""

from typing import List, Dict, Optional
import statistics
from app.models.scenario import TelemetryPoint
from app.models.telemetry import TelemetryMetrics, AnomalyDetection, ProcessedTelemetry
from app.services.gt3r_knowledge import DIAGNOSIS_THRESHOLDS


class TelemetryProcessor:
    """Process raw telemetry data and extract metrics"""
    
    def __init__(self, telemetry: List[TelemetryPoint], scenario_id: str):
        self.telemetry = telemetry
        self.scenario_id = scenario_id
        self.anomalies: List[AnomalyDetection] = []
    
    def process(self) -> ProcessedTelemetry:
        """Main processing pipeline"""
        if not self.telemetry:
            return self._empty_result()
        
        try:
            # Compute all metrics
            metrics = self._compute_metrics()
            
            # Detect anomalies
            self._detect_anomalies()
            
            return ProcessedTelemetry(
                scenario_id=self.scenario_id,
                metrics=metrics,
                anomalies=self.anomalies,
                raw_data_points=len(self.telemetry),
                processing_status="success"
            )
        except Exception as e:
            return ProcessedTelemetry(
                scenario_id=self.scenario_id,
                metrics=TelemetryMetrics(
                    lap_count=0,
                    avg_speed_kmh=0,
                    max_speed_kmh=0,
                    min_speed_kmh=0
                ),
                anomalies=[],
                raw_data_points=len(self.telemetry),
                processing_status=f"error: {str(e)}"
            )
    
    def _empty_result(self) -> ProcessedTelemetry:
        """Return empty result when no telemetry provided"""
        return ProcessedTelemetry(
            scenario_id=self.scenario_id,
            metrics=TelemetryMetrics(
                lap_count=0,
                avg_speed_kmh=0,
                max_speed_kmh=0,
                min_speed_kmh=0
            ),
            anomalies=[],
            raw_data_points=0,
            processing_status="no_data"
        )
    
    # ========== SPEED METRICS ==========
    def _compute_speed_metrics(self) -> Dict:
        """Compute speed-based metrics"""
        speeds = [p.speed_kmh for p in self.telemetry]
        
        return {
            "avg_speed_kmh": round(statistics.mean(speeds), 2) if speeds else 0,
            "max_speed_kmh": max(speeds) if speeds else 0,
            "min_speed_kmh": min(speeds) if speeds else 0,
        }
    
    # ========== TIRE METRICS ==========
    def _compute_tire_metrics(self) -> Dict:
        """Compute tire temperature and pressure metrics"""
        tire_temps_fl = [p.tire_temp_fl_c for p in self.telemetry if p.tire_temp_fl_c > 0]
        tire_temps_fr = [p.tire_temp_fr_c for p in self.telemetry if p.tire_temp_fr_c > 0]
        tire_temps_rl = [p.tire_temp_rl_c for p in self.telemetry if p.tire_temp_rl_c > 0]
        tire_temps_rr = [p.tire_temp_rr_c for p in self.telemetry if p.tire_temp_rr_c > 0]
        
        tire_pressures_fl = [p.tire_pressure_fl_bar for p in self.telemetry if p.tire_pressure_fl_bar > 0]
        tire_pressures_fr = [p.tire_pressure_fr_bar for p in self.telemetry if p.tire_pressure_fr_bar > 0]
        tire_pressures_rl = [p.tire_pressure_rl_bar for p in self.telemetry if p.tire_pressure_rl_bar > 0]
        tire_pressures_rr = [p.tire_pressure_rr_bar for p in self.telemetry if p.tire_pressure_rr_bar > 0]
        
        # Average temperatures
        avg_temps = {
            "fl": round(statistics.mean(tire_temps_fl), 1) if tire_temps_fl else 0,
            "fr": round(statistics.mean(tire_temps_fr), 1) if tire_temps_fr else 0,
            "rl": round(statistics.mean(tire_temps_rl), 1) if tire_temps_rl else 0,
            "rr": round(statistics.mean(tire_temps_rr), 1) if tire_temps_rr else 0,
        }
        
        # Temperature deltas (spread across lap)
        temp_deltas = {
            "fl": round(max(tire_temps_fl or [0]) - min(tire_temps_fl or [0]), 1),
            "fr": round(max(tire_temps_fr or [0]) - min(tire_temps_fr or [0]), 1),
            "rl": round(max(tire_temps_rl or [0]) - min(tire_temps_rl or [0]), 1),
            "rr": round(max(tire_temps_rr or [0]) - min(tire_temps_rr or [0]), 1),
        }
        
        # Average pressures
        avg_pressures = {
            "fl": round(statistics.mean(tire_pressures_fl), 2) if tire_pressures_fl else 0,
            "fr": round(statistics.mean(tire_pressures_fr), 2) if tire_pressures_fr else 0,
            "rl": round(statistics.mean(tire_pressures_rl), 2) if tire_pressures_rl else 0,
            "rr": round(statistics.mean(tire_pressures_rr), 2) if tire_pressures_rr else 0,
        }
        
        # Pressure drift (start vs end)
        pressure_drift = {}
        if tire_pressures_fl:
            pressure_drift["fl"] = round(tire_pressures_fl[-1] - tire_pressures_fl[0], 2)
        if tire_pressures_fr:
            pressure_drift["fr"] = round(tire_pressures_fr[-1] - tire_pressures_fr[0], 2)
        if tire_pressures_rl:
            pressure_drift["rl"] = round(tire_pressures_rl[-1] - tire_pressures_rl[0], 2)
        if tire_pressures_rr:
            pressure_drift["rr"] = round(tire_pressures_rr[-1] - tire_pressures_rr[0], 2)
        
        # Tire degradation (temp-based estimate, simplified)
        tire_deg = self._estimate_tire_degradation(avg_temps)
        
        return {
            "avg_tire_temp_c": avg_temps,
            "tire_temp_delta_c": temp_deltas,
            "avg_tire_pressure_bar": avg_pressures,
            "pressure_delta_bar": pressure_drift,
            "tire_degradation_percent": tire_deg
        }
    
    def _estimate_tire_degradation(self, avg_temps: Dict) -> Dict:
        """Estimate tire wear based on temperature"""
        deg = {}
        for corner, temp in avg_temps.items():
            if temp < 60:
                deg[corner] = 0  # Cold tire, no wear
            elif temp < 85:
                deg[corner] = round((temp - 60) / 25 * 20, 1)  # 0-20%
            elif temp < 100:
                deg[corner] = round(20 + (temp - 85) / 15 * 30, 1)  # 20-50%
            elif temp < 110:
                deg[corner] = round(50 + (temp - 100) / 10 * 30, 1)  # 50-80%
            else:
                deg[corner] = 100  # Overheated
        return deg
    
    # ========== BRAKING METRICS ==========
    def _compute_brake_metrics(self) -> Dict:
        """Compute braking-related metrics"""
        brake_pressures = [p.brake_pressure_bar for p in self.telemetry if p.brake_pressure_bar > 0]
        brake_percents = [p.brake_percent for p in self.telemetry if p.brake_percent > 0]
        
        # Longitudinal G during braking (proxy for deceleration)
        braking_events = [
            p.longitudinal_g for p in self.telemetry 
            if p.brake_percent > DIAGNOSIS_THRESHOLDS["brake_pressure_high"]
        ]
        
        # Detect braking inefficiency
        inefficiency_count = 0
        for p in self.telemetry:
            if (p.brake_percent > DIAGNOSIS_THRESHOLDS["brake_pressure_high"] and 
                p.longitudinal_g < DIAGNOSIS_THRESHOLDS["deceleration_threshold"]):
                inefficiency_count += 1
        
        return {
            "avg_brake_pressure_bar": round(statistics.mean(brake_pressures), 2) if brake_pressures else 0,
            "max_brake_pressure_bar": max(brake_pressures) if brake_pressures else 0,
            "braking_inefficiency_events": inefficiency_count
        }
    
    # ========== G-FORCE METRICS ==========
    def _compute_gforce_metrics(self) -> Dict:
        """Compute lateral and longitudinal G-force metrics"""
        lateral_gs = [abs(p.lateral_g) for p in self.telemetry]
        long_gs = [p.longitudinal_g for p in self.telemetry]
        
        return {
            "max_lateral_g": round(max(lateral_gs), 2) if lateral_gs else 0,
            "max_longitudinal_g": round(max(long_gs), 2) if long_gs else 0,
            "avg_lateral_g": round(statistics.mean(lateral_gs), 2) if lateral_gs else 0
        }
    
    # ========== STEERING METRICS ==========
    def _compute_steering_metrics(self) -> Dict:
        """Compute steering input metrics"""
        steering_angles = [abs(p.steering_angle_deg) for p in self.telemetry]
        
        return {
            "avg_steering_angle_deg": round(statistics.mean(steering_angles), 2) if steering_angles else 0,
            "max_steering_angle_deg": round(max(steering_angles), 2) if steering_angles else 0
        }
    
    # ========== UNDERSTEER/OVERSTEER DETECTION ==========
    def _compute_balance_metrics(self) -> Dict:
        """Detect understeer and oversteer events"""
        understeer_events = 0
        oversteer_events = 0
        
        for p in self.telemetry:
            # Understeer: High steering angle but low lateral G (not enough grip)
            if (abs(p.steering_angle_deg) > DIAGNOSIS_THRESHOLDS["steering_angle_high"] and 
                p.lateral_g < DIAGNOSIS_THRESHOLDS["lateral_g_threshold"]):
                understeer_events += 1
            
            # Oversteer: Yaw rate high relative to steering angle (rear sliding out)
            if p.yaw_rate_deg_per_sec > 5 and abs(p.steering_angle_deg) < 5:
                oversteer_events += 1
        
        return {
            "understeer_events": understeer_events,
            "oversteer_events": oversteer_events
        }
    
    # ========== THROTTLE/BRAKE OVERLAP ==========
    def _compute_throttle_brake_overlap(self) -> float:
        """Compute percentage of lap with both throttle and brake active"""
        overlap_count = 0
        for p in self.telemetry:
            if p.throttle_percent > 0 and p.brake_percent > 0:
                overlap_count += 1
        
        return round((overlap_count / len(self.telemetry)) * 100, 1) if self.telemetry else 0
    
    # ========== LAP COUNTING ==========
    def _count_laps(self) -> int:
        """Count number of laps (simplified: count RPM drops as lap markers)"""
        # This is a placeholder; real implementation would track a specific corner or distance
        return 1
    
    # ========== MAIN METRICS ASSEMBLY ==========
    def _compute_metrics(self) -> TelemetryMetrics:
        """Assemble all metrics into TelemetryMetrics object"""
        speed_metrics = self._compute_speed_metrics()
        tire_metrics = self._compute_tire_metrics()
        brake_metrics = self._compute_brake_metrics()
        gforce_metrics = self._compute_gforce_metrics()
        steering_metrics = self._compute_steering_metrics()
        balance_metrics = self._compute_balance_metrics()
        throttle_brake_overlap = self._compute_throttle_brake_overlap()
        
        return TelemetryMetrics(
            lap_count=self._count_laps(),
            avg_speed_kmh=speed_metrics["avg_speed_kmh"],
            max_speed_kmh=speed_metrics["max_speed_kmh"],
            min_speed_kmh=speed_metrics["min_speed_kmh"],
            understeer_events=balance_metrics["understeer_events"],
            oversteer_events=balance_metrics["oversteer_events"],
            avg_tire_temp_c=tire_metrics["avg_tire_temp_c"],
            tire_temp_delta_c=tire_metrics["tire_temp_delta_c"],
            tire_degradation_percent=tire_metrics["tire_degradation_percent"],
            avg_tire_pressure_bar=tire_metrics["avg_tire_pressure_bar"],
            pressure_delta_bar=tire_metrics["pressure_delta_bar"],
            avg_brake_pressure_bar=brake_metrics["avg_brake_pressure_bar"],
            max_brake_pressure_bar=brake_metrics["max_brake_pressure_bar"],
            braking_inefficiency_events=brake_metrics["braking_inefficiency_events"],
            max_lateral_g=gforce_metrics["max_lateral_g"],
            max_longitudinal_g=gforce_metrics["max_longitudinal_g"],
            avg_lateral_g=gforce_metrics["avg_lateral_g"],
            avg_steering_angle_deg=steering_metrics["avg_steering_angle_deg"],
            max_steering_angle_deg=steering_metrics["max_steering_angle_deg"],
            throttle_brake_overlap_percent=throttle_brake_overlap
        )
    
    # ========== ANOMALY DETECTION ==========
    def _detect_anomalies(self):
        """Detect and log anomalies in telemetry"""
        # Tire temperature spikes
        for corner in ["fl", "fr", "rl", "rr"]:
            temps = self._get_tire_temps_by_corner(corner)
            if temps:
                max_temp = max(temps)
                if max_temp > DIAGNOSIS_THRESHOLDS["tire_temp_high"]:
                    self.anomalies.append(AnomalyDetection(
                        anomaly_type="tire_overtemp",
                        severity="high" if max_temp > 110 else "medium",
                        timestamp_ms=0,
                        evidence=[f"{corner.upper()} tire reached {max_temp}°C"]
                    ))
        
        # Brake fade detection
        for i, p in enumerate(self.telemetry):
            if (p.brake_percent > DIAGNOSIS_THRESHOLDS["brake_pressure_high"] and 
                p.longitudinal_g < DIAGNOSIS_THRESHOLDS["deceleration_threshold"]):
                self.anomalies.append(AnomalyDetection(
                    anomaly_type="brake_fade_risk",
                    severity="medium",
                    timestamp_ms=p.timestamp_ms,
                    evidence=["High brake input with low deceleration"]
                ))
                break  # Only log once
        
        # Tire pressure anomalies
        for corner in ["fl", "fr", "rl", "rr"]:
            pressures = self._get_tire_pressures_by_corner(corner)
            if pressures:
                avg_p = statistics.mean(pressures)
                if avg_p > DIAGNOSIS_THRESHOLDS["tire_pressure_high"]:
                    self.anomalies.append(AnomalyDetection(
                        anomaly_type="tire_pressure_high",
                        severity="medium",
                        timestamp_ms=0,
                        evidence=[f"{corner.upper()} average pressure {avg_p:.1f} bar"]
                    ))
    
    def _get_tire_temps_by_corner(self, corner: str) -> List[float]:
        """Extract tire temps by corner (fl, fr, rl, rr)"""
        temps = []
        for p in self.telemetry:
            if corner == "fl":
                temps.append(p.tire_temp_fl_c)
            elif corner == "fr":
                temps.append(p.tire_temp_fr_c)
            elif corner == "rl":
                temps.append(p.tire_temp_rl_c)
            elif corner == "rr":
                temps.append(p.tire_temp_rr_c)
        return [t for t in temps if t > 0]
    
    def _get_tire_pressures_by_corner(self, corner: str) -> List[float]:
        """Extract tire pressures by corner"""
        pressures = []
        for p in self.telemetry:
            if corner == "fl":
                pressures.append(p.tire_pressure_fl_bar)
            elif corner == "fr":
                pressures.append(p.tire_pressure_fr_bar)
            elif corner == "rl":
                pressures.append(p.tire_pressure_rl_bar)
            elif corner == "rr":
                pressures.append(p.tire_pressure_rr_bar)
        return [pr for pr in pressures if pr > 0]


# ========== CONVENIENCE FUNCTION ==========
def process_telemetry(telemetry: List[TelemetryPoint], scenario_id: str) -> ProcessedTelemetry:
    """Convenience function to process telemetry"""
    processor = TelemetryProcessor(telemetry, scenario_id)
    return processor.process()