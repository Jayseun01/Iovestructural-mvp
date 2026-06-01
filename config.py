"""
Configuration and Constants for iLoveStructural Staircase Designer
Complete parametric definitions for all stair families
"""

import re

# ============================================================================
# INPUT PARAMETERS BY STAIR FAMILY
# ============================================================================

INPUT_PARAMETERS_BY_FAMILY = {
    "half_turn_u_shape_dog_leg": {
        "display_name": "Half-Turn (U-Shape) - Dog Leg",
        "description": "Most common residential stair with 180° turn and landing",
        "core_inputs": {
            "floor_height": {
                "display": "Floor Height (F.F to F.F)",
                "unit": "mm",
                "min": 2400,
                "max": 5000,
                "typical": 3000,
                "step": 50,
                "description": "Total vertical distance the stair must span",
            },
            "stair_width": {
                "display": "Stair Width",
                "unit": "mm",
                "min": 900,
                "max": 2000,
                "typical": 1200,
                "step": 50,
                "description": "Clear width of stair flight",
            },
            "tread_depth": {
                "display": "Tread Depth (Going)",
                "unit": "mm",
                "min": 250,
                "max": 350,
                "typical": 300,
                "step": 10,
                "description": "Horizontal depth of each step",
            },
        },
        "derived_outputs": {
            "riser_height": {
                "display": "Riser Height",
                "unit": "mm",
                "calculation_rule": "floor_height / riser_count",
                "validation": "Must be 150-190mm (IS456 / EC2)",
                "auto_calculate": True,
            },
            "riser_count": {
                "display": "Number of Risers",
                "unit": "count",
                "calculation_rule": "ceil(floor_height / target_riser_height)",
                "target_riser": 175,
                "auto_calculate": True,
            },
            "flight_rise": {
                "display": "Flight Rise (Half of total)",
                "unit": "mm",
                "calculation_rule": "floor_height / 2",
                "auto_calculate": True,
            },
            "flight_length": {
                "display": "Flight Length (Horizontal)",
                "unit": "mm",
                "calculation_rule": "riser_count * tread_depth",
                "auto_calculate": True,
            },
            "landing_length": {
                "display": "Landing Length",
                "unit": "mm",
                "calculation_rule": "Usually stair_width + 200mm",
                "auto_calculate": True,
            },
            "waist_thickness": {
                "display": "Waist Slab Thickness",
                "unit": "mm",
                "calculation_rule": "flight_rise / 20",
                "auto_calculate": True,
            },
        }
    },
    "quarter_turn_l_shape": {
        "display_name": "Quarter-Turn (L-Shape)",
        "description": "90° turn with single quarter-space landing",
        "core_inputs": {
            "floor_height": {
                "display": "Floor Height (F.F to F.F)",
                "unit": "mm",
                "min": 2400,
                "max": 5000,
                "typical": 3000,
                "step": 50,
            },
            "stair_width": {
                "display": "Stair Width",
                "unit": "mm",
                "min": 900,
                "max": 2000,
                "typical": 1200,
                "step": 50,
            },
            "tread_depth": {
                "display": "Tread Depth",
                "unit": "mm",
                "min": 250,
                "max": 350,
                "typical": 300,
                "step": 10,
            },
        },
        "derived_outputs": {
            "riser_height": {"display": "Riser Height", "unit": "mm", "auto_calculate": True},
            "riser_count": {"display": "Number of Risers", "unit": "count", "auto_calculate": True},
            "flight_rise": {"display": "Flight Rise", "unit": "mm", "auto_calculate": True},
            "flight_length": {"display": "Flight Length", "unit": "mm", "auto_calculate": True},
            "waist_thickness": {"display": "Waist Slab Thickness", "unit": "mm", "auto_calculate": True},
        }
    },
    "straight_single_flight": {
        "display_name": "Straight - Single Flight",
        "description": "Straight stair without landing or turn",
        "core_inputs": {
            "floor_height": {
                "display": "Floor Height",
                "unit": "mm",
                "min": 2400,
                "max": 4500,
                "typical": 3000,
                "step": 50,
            },
            "stair_width": {
                "display": "Stair Width",
                "unit": "mm",
                "min": 900,
                "max": 2000,
                "typical": 1200,
                "step": 50,
            },
            "tread_depth": {
                "display": "Tread Depth",
                "unit": "mm",
                "min": 250,
                "max": 350,
                "typical": 300,
                "step": 10,
            },
        },
        "derived_outputs": {
            "riser_height": {"display": "Riser Height", "unit": "mm", "auto_calculate": True},
            "riser_count": {"display": "Number of Risers", "unit": "count", "auto_calculate": True},
            "flight_rise": {"display": "Flight Rise", "unit": "mm", "auto_calculate": True},
            "flight_length": {"display": "Flight Length", "unit": "mm", "auto_calculate": True},
            "waist_thickness": {"display": "Waist Slab Thickness", "unit": "mm", "auto_calculate": True},
        }
    },
    "spiral_circular": {
        "display_name": "Spiral - Circular",
        "description": "Spiral staircase around central column",
        "core_inputs": {
            "floor_height": {
                "display": "Floor Height",
                "unit": "mm",
                "min": 2400,
                "max": 5000,
                "typical": 3000,
                "step": 50,
            },
            "stair_diameter": {
                "display": "Stair Diameter",
                "unit": "mm",
                "min": 1400,
                "max": 3000,
                "typical": 1800,
                "step": 50,
            },
            "tread_depth": {
                "display": "Tread Depth",
                "unit": "mm",
                "min": 250,
                "max": 350,
                "typical": 300,
                "step": 10,
            },
        },
        "derived_outputs": {
            "riser_height": {"display": "Riser Height", "unit": "mm", "auto_calculate": True},
            "riser_count": {"display": "Number of Risers", "unit": "count", "auto_calculate": True},
            "steps_per_turn": {"display": "Steps per Revolution", "unit": "count", "auto_calculate": True},
            "waist_thickness": {"display": "Slab Thickness", "unit": "mm", "auto_calculate": True},
        }
    },
}

# ============================================================================
# REINFORCEMENT STANDARDS
# ============================================================================

REINFORCEMENT_STANDARDS = {
    "IS456_2000_India": {
        "code_name": "Indian Standard IS456:2000",
        "country": "India",
        "minimum_cover": {"bottom": 30, "top": 20, "sides": 25},
        "bar_constraints": {
            "minimum_size": "Y10",
            "maximum_spacing": 300,
            "minimum_spacing": 100,
        },
        "riser_and_tread": {
            "rule": "Y12 @ 200mm c/c both ways",
            "adjustments": [
                {"span": 2000, "config": "Y10 @ 250mm c/c"},
                {"span": 3000, "config": "Y12 @ 200mm c/c"},
                {"span": 3500, "config": "Y16 @ 200mm c/c"},
            ]
        },
    },
    "EC2_Eurocode_2": {
        "code_name": "Eurocode 2 (EU)",
        "country": "Europe",
        "minimum_cover": {"bottom": 25, "top": 20},
    },
    "ACI_318_USA": {
        "code_name": "ACI 318 (USA)",
        "country": "USA",
        "minimum_cover": {"bottom": 1.5, "top": 1.5},
    },
}

# ============================================================================
# BAR WEIGHT TABLE (kg/m)
# ============================================================================

BAR_WEIGHTS = {
    "Y8": 0.395,
    "Y10": 0.617,
    "Y12": 0.888,
    "Y16": 1.580,
    "Y20": 2.466,
    "Y25": 3.853,
    "Y32": 6.313,
}

# ============================================================================
# LAYER ROLES & STYLES
# ============================================================================

LAYER_ROLE_OPTIONS = [
    "geometry",
    "dimension",
    "reinforcement",
    "landing",
    "tread_riser",
    "section",
    "annotation",
    "hidden",
]

ROLE_COLORS = {
    "geometry": "#e5e7eb",
    "dimension": "#fde047",
    "reinforcement": "#fb7185",
    "landing": "#38bdf8",
    "tread_riser": "#34d399",
    "section": "#c084fc",
    "annotation": "#f8fafc",
    "hidden": "#94a3b8",
}
