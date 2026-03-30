"""
GT3 R Knowledge Base
Porsche 911 GT3 R setup reference and problem-solution mappings
Based on real GT3 R engineering practices
"""

# ============ NOMINAL SETUPS ============
NOMINAL_SETUP = {
    "front_wing_angle_deg": 8,
    "rear_wing_angle_deg": 15,
    "front_brake_bias_percent": 52,
    "fuel_load_liters": 45,
    "tire_compound": "soft",
    "tire_pressures": {
        "fl_bar": 28.5,
        "fr_bar": 28.5,
        "rl_bar": 29.0,
        "rr_bar": 29.0
    },
    "abs_level": 1,
    "traction_control_level": 1
}

SETUP_RANGES = {
    "front_wing_angle_deg": {"min": 0, "max": 15, "step": 0.5},
    "rear_wing_angle_deg": {"min": 0, "max": 20, "step": 0.5},
    "front_brake_bias_percent": {"min": 40, "max": 65, "step": 1},
    "fuel_load_liters": {"min": 20, "max": 70, "step": 1},
    "tire_pressure_bar": {"min": 27, "max": 31, "step": 0.1},
}

# ============ PROBLEM SOLUTIONS ============
PROBLEM_SOLUTIONS = {
    "understeer_entry": {
        "severity_indicator": "High steering input + low lateral G in turn-in",
        "root_causes": [
            "Front wing too low (insufficient downforce)",
            "Front brake bias too high (over-braking balance)",
            "Tire pressures low (loss of stiffness)",
            "Driver: Late turn-in point"
        ],
        "primary_solution": {
            "action": "increase_front_wing_angle",
            "delta": "+0.5° to +1.0°",
            "rationale": "Add front downforce to improve turn-in grip",
            "expected_impact": "Reduce understeer angle by 2-3°, improve front bite"
        },
        "secondary_solutions": [
            {
                "action": "reduce_front_brake_bias",
                "delta": "-1% to -2%",
                "rationale": "Reduce front brake force to help mid-brake turn-in"
            },
            {
                "action": "increase_front_tire_pressure",
                "delta": "+0.2 to +0.3 bar",
                "rationale": "Increase tire sidewall stiffness for better response"
            },
            {
                "action": "driver_technique",
                "delta": "Carry more speed into corner, apply throttle earlier",
                "rationale": "Load the tires earlier; let mechanical grip work"
            }
        ]
    },
    
    "understeer_mid_corner": {
        "severity_indicator": "Steering angle constant/increasing but speed drops; high yaw rate lag",
        "root_causes": [
            "Rear wing too low (insufficient downforce)",
            "Tire pressure too low (tire rolling, losing grip)",
            "High fuel load (weight bias forward)",
            "Driver: Too much steering lock applied"
        ],
        "primary_solution": {
            "action": "increase_rear_wing_angle",
            "delta": "+1.0° to +1.5°",
            "rationale": "Add rear downforce to improve balance and reduce yaw lag",
            "expected_impact": "Improve mid-corner response by 1-2 mph turn-in speed"
        },
        "secondary_solutions": [
            {
                "action": "increase_rear_tire_pressure",
                "delta": "+0.2 to +0.3 bar",
                "rationale": "Reduce tire rolling; improve lateral stiffness"
            },
            {
                "action": "reduce_front_brake_bias",
                "delta": "-1%",
                "rationale": "Help front end rotate mid-corner"
            },
            {
                "action": "driver_technique",
                "delta": "Reduce steering input; use smoother inputs",
                "rationale": "Let the car rotate naturally; don't fight the physics"
            }
        ]
    },
    
    "understeer_exit": {
        "severity_indicator": "Power application causes push; front slides out under throttle",
        "root_causes": [
            "Front wing angle too low (insufficient downforce under load)",
            "Traction control level too low (wheel spin → understeer)",
            "Tire compound too soft or worn",
            "Driver: Too aggressive throttle application"
        ],
        "primary_solution": {
            "action": "increase_traction_control_level",
            "delta": "+1 (0→1 or 1→2)",
            "rationale": "Reduce wheel slip under power, improve traction"
        },
        "secondary_solutions": [
            {
                "action": "increase_front_wing_angle",
                "delta": "+0.5°",
                "rationale": "Add front downforce for grip under acceleration"
            },
            {
                "action": "increase_front_tire_pressure",
                "delta": "+0.2 bar",
                "rationale": "Improve sidewall support under lateral load + power"
            }
        ]
    },
    
    "oversteer_entry": {
        "severity_indicator": "Rear slides immediately on turn-in; yaw rate spikes early",
        "root_causes": [
            "Rear wing too high (too much rear downforce)",
            "Front brake bias too low (weight on rear mid-brake)",
            "Rear tire pressure too high (loss of compliance)",
            "Driver: Too sharp an input"
        ],
        "primary_solution": {
            "action": "reduce_rear_wing_angle",
            "delta": "-0.5° to -1.0°",
            "rationale": "Reduce rear downforce; improve balance"
        },
        "secondary_solutions": [
            {
                "action": "increase_front_brake_bias",
                "delta": "+1% to +2%",
                "rationale": "Keep weight forward during braking; reduce rear instability"
            },
            {
                "action": "reduce_rear_tire_pressure",
                "delta": "-0.1 to -0.2 bar",
                "rationale": "Improve rear tire compliance; reduce harshness"
            }
        ]
    },
    
    "oversteer_mid_corner": {
        "severity_indicator": "Rear slides mid-corner; yaw rate uncontrolled",
        "root_causes": [
            "Rear wing angle too high",
            "Rear tire pressure too high (overstiff)",
            "High speed + high downforce combination",
            "Driver: Over-throttle input"
        ],
        "primary_solution": {
            "action": "reduce_rear_wing_angle",
            "delta": "-1.0° to -1.5°",
            "rationale": "Reduce rear instability"
        },
        "secondary_solutions": [
            {
                "action": "reduce_rear_tire_pressure",
                "delta": "-0.2 to -0.3 bar",
                "rationale": "Improve tire compliance; reduce transient oversteer"
            }
        ]
    },
    
    "oversteer_exit": {
        "severity_indicator": "Power application causes rear slide; loss of traction",
        "root_causes": [
            "Rear wing angle too high (rear-biased downforce)",
            "Traction control level too low",
            "Rear tire pressure too high",
            "Driver: Too aggressive throttle"
        ],
        "primary_solution": {
            "action": "increase_traction_control_level",
            "delta": "+1",
            "rationale": "Reduce rear wheelspin; improve traction"
        },
        "secondary_solutions": [
            {
                "action": "reduce_rear_wing_angle",
                "delta": "-0.5°",
                "rationale": "Reduce rear-biased aerodynamic overload"
            },
            {
                "action": "reduce_rear_tire_pressure",
                "delta": "-0.2 bar",
                "rationale": "Improve rear tire compliance under power"
            }
        ]
    },
    
    "tire_degradation_front": {
        "severity_indicator": "Front tire temps spike (100°C+); pressures climb; grip loss mid-corner",
        "root_causes": [
            "Too much downforce on front (over-working the tires)",
            "Front tire pressures already high",
            "Aggressive front-end driving style"
        ],
        "primary_solution": {
            "action": "reduce_front_wing_angle",
            "delta": "-0.5°",
            "rationale": "Reduce front tire workload and heat"
        },
        "secondary_solutions": [
            {
                "action": "reduce_front_tire_pressure",
                "delta": "-0.2 to -0.3 bar",
                "rationale": "Increase tire compliance; reduce temperature build-up"
            },
            {
                "action": "pace_management",
                "delta": "Ease off slightly; let tires cool",
                "rationale": "Front tires may be at end of life"
            }
        ]
    },
    
    "tire_degradation_rear": {
        "severity_indicator": "Rear tire temps high; rear pressure rising; loss of exit traction",
        "root_causes": [
            "Too much rear downforce or high exit speeds",
            "Tire pressures too low (rolling)",
            "Aggressive throttle application"
        ],
        "primary_solution": {
            "action": "reduce_rear_wing_angle",
            "delta": "-0.5°",
            "rationale": "Reduce rear tire workload"
        },
        "secondary_solutions": [
            {
                "action": "increase_rear_tire_pressure",
                "delta": "+0.2 bar",
                "rationale": "Reduce tire rolling; maintain sidewall stiffness longer"
            },
            {
                "action": "pace_management",
                "delta": "Extend stint length or swap tires",
                "rationale": "Tires may be approaching end-of-life"
            }
        ]
    },
    
    "brake_fade": {
        "severity_indicator": "Brake pressure high but deceleration low; brake distances increasing",
        "root_causes": [
            "Brake fluid temperature too high (loss of friction material)",
            "Brake pads worn or contaminated",
            "Front brake bias too aggressive"
        ],
        "primary_solution": {
            "action": "reduce_front_brake_bias",
            "delta": "-2% to -3%",
            "rationale": "Shift load to rear brakes; cool front brakes"
        },
        "secondary_solutions": [
            {
                "action": "technique_adjustment",
                "delta": "Trail-brake less aggressively; ease off brake pedal earlier",
                "rationale": "Reduce brake thermal load"
            },
            {
                "action": "pace_management",
                "delta": "Extend braking zone; plan for longer stops",
                "rationale": "Let brakes cool naturally"
            }
        ]
    },
    
    "brake_balance_instability": {
        "severity_indicator": "Braking pulls left/right; brake balance feels untrustworthy",
        "root_causes": [
            "Brake bias too extreme (front or rear over-braking)",
            "Brake pad wear imbalance (front vs rear)",
            "Suspension geometry under heavy braking"
        ],
        "primary_solution": {
            "action": "adjust_front_brake_bias_toward_center",
            "delta": "±1%",
            "rationale": "Find the neutral braking point; reduce pull/push"
        }
    },
    
    "balanced": {
        "severity_indicator": "Car feels composed; good balance across all phases; no major issues",
        "root_causes": [],
        "primary_solution": {
            "action": "maintain_current_setup",
            "delta": "No change recommended",
            "rationale": "Setup is well-tuned. Fine-tune only if specific improvement area exists."
        },
        "notes": "Monitor tire wear and fuel strategy for stint management."
    }
}


# ============ THRESHOLD VALUES ============
DIAGNOSIS_THRESHOLDS = {
    "understeer_feedback_threshold": 2,  # Driver feedback ≥ +2 = understeer
    "oversteer_feedback_threshold": -2,  # Driver feedback ≤ -2 = oversteer
    "steering_angle_high": 10,  # Degrees (indicates high input)
    "lateral_g_threshold": 1.0,  # G (cornering intensity)
    "brake_pressure_high": 70,  # % (heavy braking)
    "deceleration_threshold": 0.5,  # G (expected for "high" brake input)
    "tire_temp_high": 100,  # °C
    "tire_temp_concern": 95,  # °C
    "tire_pressure_high": 30.0,  # Bar
    "tire_pressure_low": 27.5,  # Bar
}


# ============ HELPER FUNCTIONS ============
def get_solution(problem_type: str) -> dict:
    """Retrieve solution matrix for a problem type"""
    return PROBLEM_SOLUTIONS.get(problem_type, PROBLEM_SOLUTIONS["balanced"])


def get_nominal_setup() -> dict:
    """Return nominal (baseline) GT3 R setup"""
    return NOMINAL_SETUP.copy()


def is_problem_severity(problem_type: str, confidence: int) -> str:
    """Determine severity based on problem type and confidence"""
    if confidence >= 80:
        return "high"
    elif confidence >= 60:
        return "medium"
    else:
        return "low"


def get_setup_adjustment_guide() -> dict:
    """Return all setup parameters and their effects"""
    return {
        "front_wing_angle_deg": {
            "effect": "Front downforce",
            "increase": "More entry grip, later apex, can cause mid-corner understeer if too high",
            "decrease": "Less entry grip, earlier apex, can cause entry oversteer if too low"
        },
        "rear_wing_angle_deg": {
            "effect": "Rear downforce",
            "increase": "Better exit traction, earlier turn-in, can cause mid-corner understeer if overdone",
            "decrease": "Less exit grip, later apex, can cause oversteer if too low"
        },
        "front_brake_bias_percent": {
            "effect": "Front brake load distribution",
            "increase": "More front brake power, helps turn-in, can lock front wheels",
            "decrease": "More rear brake power, extends mid-corner, can cause understeer on exit"
        },
        "tire_pressure": {
            "effect": "Tire stiffness and compliance",
            "increase": "More responsive, less rolling, higher temps, can cause understeer if too high",
            "decrease": "More compliant, better grip, lower temps, can cause rolling/understeer if too low"
        }
    }