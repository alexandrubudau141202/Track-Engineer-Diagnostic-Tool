"""
Diagnosis Engine
Identifies car/driver problems and generates setup recommendations based on telemetry,
driver feedback, and GT3 R setup knowledge.
"""

from typing import List, Optional
from app.models.scenario import ScenarioRequest
from app.models.telemetry import ProcessedTelemetry
from app.models.diagnosis import (
    DiagnosisResult, Problem, Recommendation, SetupDelta, DriverCoaching
)
from app.services.gt3r_knowledge import (
    PROBLEM_SOLUTIONS, DIAGNOSIS_THRESHOLDS, get_solution, is_problem_severity
)
from app.services.telemetry_processor import process_telemetry


class DiagnosisEngine:
    """Main diagnosis logic"""
    
    def __init__(self, scenario: ScenarioRequest, processed_telemetry: ProcessedTelemetry):
        self.scenario = scenario
        self.telemetry = processed_telemetry
        self.problems: List[Problem] = []
        self.recommendations: List[Recommendation] = []
    
    def diagnose(self) -> DiagnosisResult:
        """Main diagnosis pipeline"""
        # Step 1: Identify problems based on telemetry + feedback
        self._identify_problems()
        
        # Step 2: Rank by severity/confidence
        self._rank_problems()
        
        # Step 3: Generate recommendations for each problem
        self._generate_recommendations()
        
        # Step 4: Generate setup delta and coaching
        setup_delta = self._generate_setup_delta()
        coaching = self._generate_driver_coaching()
        
        # Step 5: Build summary
        summary = self._build_summary()
        
        return DiagnosisResult(
            scenario_id=self.scenario.scenario_id or "unknown",
            primary_problem=self.problems[0].type if self.problems else "balanced",
            overall_confidence_percent=self.problems[0].confidence_percent if self.problems else 50,
            problems_detected=self.problems,
            recommendations=self.recommendations,
            setup_delta=setup_delta,
            driver_coaching=coaching,
            summary=summary
        )
    
    # ========== PROBLEM IDENTIFICATION ==========
    def _identify_problems(self):
        """Identify problems from telemetry and driver feedback"""
        feedback = self.scenario.driver_feedback
        metrics = self.telemetry.metrics
        
        # Understeer Entry
        if self._check_understeer_entry(feedback, metrics):
            self.problems.append(self._build_problem(
                "understeer_entry",
                self._score_understeer_entry(feedback, metrics)
            ))
        
        # Understeer Mid-Corner
        if self._check_understeer_mid_corner(feedback, metrics):
            self.problems.append(self._build_problem(
                "understeer_mid_corner",
                self._score_understeer_mid_corner(feedback, metrics)
            ))
        
        # Understeer Exit
        if self._check_understeer_exit(feedback, metrics):
            self.problems.append(self._build_problem(
                "understeer_exit",
                self._score_understeer_exit(feedback, metrics)
            ))
        
        # Oversteer Entry
        if self._check_oversteer_entry(feedback, metrics):
            self.problems.append(self._build_problem(
                "oversteer_entry",
                self._score_oversteer_entry(feedback, metrics)
            ))
        
        # Oversteer Mid-Corner
        if self._check_oversteer_mid_corner(feedback, metrics):
            self.problems.append(self._build_problem(
                "oversteer_mid_corner",
                self._score_oversteer_mid_corner(feedback, metrics)
            ))
        
        # Oversteer Exit
        if self._check_oversteer_exit(feedback, metrics):
            self.problems.append(self._build_problem(
                "oversteer_exit",
                self._score_oversteer_exit(feedback, metrics)
            ))
        
        # Tire Degradation
        if self._check_tire_degradation_front(metrics):
            self.problems.append(self._build_problem(
                "tire_degradation_front",
                self._score_tire_degradation_front(metrics)
            ))
        
        if self._check_tire_degradation_rear(metrics):
            self.problems.append(self._build_problem(
                "tire_degradation_rear",
                self._score_tire_degradation_rear(metrics)
            ))
        
        # Brake Issues
        if self._check_brake_fade(metrics):
            self.problems.append(self._build_problem(
                "brake_fade",
                self._score_brake_fade(metrics)
            ))
        
        if self._check_brake_balance(feedback):
            self.problems.append(self._build_problem(
                "brake_balance_instability",
                self._score_brake_balance(feedback)
            ))
        
        # If no problems detected, car is balanced
        if not self.problems:
            self.problems.append(self._build_problem("balanced", 80))
    
    # ========== UNDERSTEER CHECKS ==========
    def _check_understeer_entry(self, feedback, metrics) -> bool:
        return (
            feedback.understeer > DIAGNOSIS_THRESHOLDS["understeer_feedback_threshold"] or
            (metrics.max_steering_angle_deg > 10 and metrics.max_lateral_g < 1.0)
        )
    
    def _score_understeer_entry(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer > 2:
            score += 40
        if metrics.max_steering_angle_deg > 10:
            score += 20
        if metrics.max_lateral_g < 1.0:
            score += 20
        return min(score, 100)
    
    def _check_understeer_mid_corner(self, feedback, metrics) -> bool:
        return (
            feedback.understeer > 2 and 
            metrics.understeer_events > 1
        )
    
    def _score_understeer_mid_corner(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer > 2:
            score += 35
        if metrics.understeer_events > 2:
            score += 30
        if metrics.max_lateral_g < 1.0:
            score += 20
        return min(score, 100)
    
    def _check_understeer_exit(self, feedback, metrics) -> bool:
        return (
            feedback.understeer > 2 and 
            feedback.exit_traction > 1
        )
    
    def _score_understeer_exit(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer > 2:
            score += 35
        if feedback.exit_traction > 2:
            score += 30
        if metrics.throttle_brake_overlap_percent > 5:
            score += 20
        return min(score, 100)
    
    # ========== OVERSTEER CHECKS ==========
    def _check_oversteer_entry(self, feedback, metrics) -> bool:
        return feedback.understeer < -DIAGNOSIS_THRESHOLDS["oversteer_feedback_threshold"]
    
    def _score_oversteer_entry(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer < -2:
            score += 50
        if metrics.oversteer_events > 1:
            score += 30
        return min(score, 100)
    
    def _check_oversteer_mid_corner(self, feedback, metrics) -> bool:
        return (
            feedback.understeer < -2 and 
            feedback.mid_corner_balance < -1
        )
    
    def _score_oversteer_mid_corner(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer < -3:
            score += 40
        if metrics.oversteer_events > 2:
            score += 35
        if feedback.mid_corner_balance < -2:
            score += 25
        return min(score, 100)
    
    def _check_oversteer_exit(self, feedback, metrics) -> bool:
        return (
            feedback.understeer < -2 and 
            feedback.exit_traction < -1
        )
    
    def _score_oversteer_exit(self, feedback, metrics) -> int:
        score = 0
        if feedback.understeer < -3:
            score += 35
        if feedback.exit_traction < -2:
            score += 35
        if metrics.oversteer_events > 1:
            score += 30
        return min(score, 100)
    
    # ========== TIRE CHECKS ==========
    def _check_tire_degradation_front(self, metrics) -> bool:
        front_temps = metrics.avg_tire_temp_c
        return (
            (front_temps.get("fl", 0) > 95 or front_temps.get("fr", 0) > 95) and
            metrics.tire_degradation_percent.get("fl", 0) > 30
        )
    
    def _score_tire_degradation_front(self, metrics) -> int:
        score = 0
        if metrics.avg_tire_temp_c.get("fl", 0) > 100:
            score += 35
        if metrics.tire_degradation_percent.get("fl", 0) > 50:
            score += 35
        if metrics.tire_temp_delta_c.get("fl", 0) > 10:
            score += 20
        return min(score, 100)
    
    def _check_tire_degradation_rear(self, metrics) -> bool:
        rear_temps = metrics.avg_tire_temp_c
        return (
            (rear_temps.get("rl", 0) > 95 or rear_temps.get("rr", 0) > 95) and
            metrics.tire_degradation_percent.get("rr", 0) > 30
        )
    
    def _score_tire_degradation_rear(self, metrics) -> int:
        score = 0
        if metrics.avg_tire_temp_c.get("rr", 0) > 100:
            score += 35
        if metrics.tire_degradation_percent.get("rr", 0) > 50:
            score += 35
        if metrics.tire_temp_delta_c.get("rr", 0) > 10:
            score += 20
        return min(score, 100)
    
    # ========== BRAKE CHECKS ==========
    def _check_brake_fade(self, metrics) -> bool:
        return (
            metrics.max_brake_pressure_bar > 70 and
            metrics.braking_inefficiency_events > 2
        )
    
    def _score_brake_fade(self, metrics) -> int:
        score = 0
        if metrics.max_brake_pressure_bar > 80:
            score += 40
        if metrics.braking_inefficiency_events > 3:
            score += 40
        return min(score, 100)
    
    def _check_brake_balance(self, feedback) -> bool:
        return feedback.brake_stability < -2
    
    def _score_brake_balance(self, feedback) -> int:
        score = 0
        if feedback.brake_stability < -2:
            score += 60
        if feedback.brake_stability < -3:
            score += 20
        return min(score, 100)
    
    # ========== UTILITY METHODS ==========
    def _build_problem(self, problem_type: str, confidence: int) -> Problem:
        """Build a Problem object with evidence"""
        solution = get_solution(problem_type)
        
        evidence = []
        if problem_type == "understeer_entry":
            if self.scenario.driver_feedback.understeer > 2:
                evidence.append(f"Driver reports understeer: +{self.scenario.driver_feedback.understeer}")
            if self.telemetry.metrics.max_steering_angle_deg > 10:
                evidence.append(f"High steering angle: {self.telemetry.metrics.max_steering_angle_deg}°")
            if self.telemetry.metrics.max_lateral_g < 1.0:
                evidence.append(f"Low lateral G in corners: {self.telemetry.metrics.max_lateral_g}G")
        
        # Add more evidence building for other problem types as needed
        # For now, use the solution's root causes as fallback
        if not evidence:
            evidence = solution.get("root_causes", [])[:2]
        
        return Problem(
            type=problem_type,
            severity=is_problem_severity(problem_type, confidence),
            confidence_percent=confidence,
            evidence=evidence,
            affected_area=self._get_affected_area(problem_type)
        )
    
    def _get_affected_area(self, problem_type: str) -> str:
        """Map problem type to affected area"""
        mapping = {
            "understeer_entry": "entry",
            "understeer_mid_corner": "mid_corner",
            "understeer_exit": "exit",
            "oversteer_entry": "entry",
            "oversteer_mid_corner": "mid_corner",
            "oversteer_exit": "exit",
            "brake_fade": "braking",
            "brake_balance_instability": "braking",
        }
        return mapping.get(problem_type, "all")
    
    def _rank_problems(self):
        """Sort problems by severity and confidence"""
        self.problems.sort(
            key=lambda p: (p.severity != "high", p.confidence_percent),
            reverse=True
        )
    
    # ========== RECOMMENDATION GENERATION ==========
    def _generate_recommendations(self):
        """Generate setup recommendations for each problem"""
        for i, problem in enumerate(self.problems):
            solution = get_solution(problem.type)
            
            if solution.get("primary_solution"):
                primary = solution["primary_solution"]
                self.recommendations.append(Recommendation(
                    priority=1,
                    action=primary.get("action", ""),
                    delta=primary.get("delta", ""),
                    rationale=primary.get("rationale", ""),
                    expected_impact=primary.get("expected_impact", "")
                ))
            
            # Add secondary solutions (max 2)
            for j, secondary in enumerate(solution.get("secondary_solutions", [])[:2]):
                self.recommendations.append(Recommendation(
                    priority=j + 2,
                    action=secondary.get("action", ""),
                    delta=secondary.get("delta", ""),
                    rationale=secondary.get("rationale", ""),
                    expected_impact=secondary.get("expected_impact", "")
                ))
    
    def _generate_setup_delta(self) -> SetupDelta:
        """Generate recommended setup changes"""
        delta = SetupDelta()
        
        # Parse recommendations and extract setup deltas
        for rec in self.recommendations[:3]:  # Top 3 recommendations only
            if rec.action == "increase_rear_wing_angle":
                delta.rear_wing_angle_deg = rec.delta
            elif rec.action == "decrease_rear_wing_angle" or rec.action == "reduce_rear_wing_angle":
                delta.rear_wing_angle_deg = rec.delta
            elif rec.action == "increase_front_wing_angle":
                delta.front_wing_angle_deg = rec.delta
            elif rec.action == "reduce_front_brake_bias":
                delta.front_brake_bias_percent = rec.delta
            elif rec.action == "increase_front_brake_bias":
                delta.front_brake_bias_percent = rec.delta
            elif rec.action == "increase_traction_control_level":
                delta.traction_control_level = rec.delta
        
        return delta
    
    def _generate_driver_coaching(self) -> Optional[DriverCoaching]:
        """Generate driver coaching based on problems"""
        if not self.problems:
            return None
        
        coaching_lines = []
        
        if any(p.type.startswith("understeer") for p in self.problems):
            coaching_lines.append({
                "type": "braking_points",
                "text": "Try braking later into corners; carry more speed to load the tires."
            })
            coaching_lines.append({
                "type": "acceleration_strategy",
                "text": "Apply throttle smoothly; avoid abrupt inputs that can cause understeer on exit."
            })
        
        if any(p.type.startswith("oversteer") for p in self.problems):
            coaching_lines.append({
                "type": "line_adjustments",
                "text": "Ease off the throttle mid-corner; let the car rotate naturally without forcing it."
            })
            coaching_lines.append({
                "type": "acceleration_strategy",
                "text": "Progressive throttle application on exit; avoid sudden inputs."
            })
        
        if coaching_lines:
            return DriverCoaching(
                braking_points=coaching_lines[0].get("text", "") if any(c["type"] == "braking_points" for c in coaching_lines) else "",
                acceleration_strategy=coaching_lines[1].get("text", "") if len(coaching_lines) > 1 else "",
                line_adjustments=next((c["text"] for c in coaching_lines if c["type"] == "line_adjustments"), ""),
                gear_strategy="Maintain current gear strategy; focus on balance adjustments."
            )
        
        return None
    
    def _build_summary(self) -> str:
        """Build plain-English summary"""
        if not self.problems:
            return "No major issues detected. Car setup is well-balanced."
        
        primary = self.problems[0]
        summary = f"Primary issue: {primary.type} ({primary.severity} severity, {primary.confidence_percent}% confidence). "
        summary += f"Recommended: {self.recommendations[0].action if self.recommendations else 'No action'} "
        summary += f"({self.recommendations[0].delta if self.recommendations else ''})."
        
        return summary


# ========== CONVENIENCE FUNCTION ==========
def diagnose(scenario: ScenarioRequest) -> DiagnosisResult:
    """Convenience function to run full diagnosis"""
    processed_telemetry = process_telemetry(scenario.telemetry, scenario.scenario_id or "unknown")
    engine = DiagnosisEngine(scenario, processed_telemetry)
    return engine.diagnose()