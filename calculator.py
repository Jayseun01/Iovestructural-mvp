"""
Calculator Engine: Scales template + generates reinforcement
Core logic for staircase design generation
"""

import math
import pandas as pd
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from config import INPUT_PARAMETERS_BY_FAMILY, BAR_WEIGHTS

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class StairGeometry:
    """Calculated staircase geometry"""
    floor_height: float
    stair_width: float
    tread_depth: float
    riser_height: float
    riser_count: int
    flight_rise: float
    flight_length: float
    landing_length: float
    waist_thickness: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RebarPattern:
    """Single reinforcement bar pattern"""
    location: str
    bar_size: str
    spacing: float
    count: int
    total_length: float
    weight_per_bar: float
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @property
    def total_weight(self) -> float:
        return self.weight_per_bar * self.count


# ============================================================================
# GEOMETRY CALCULATOR
# ============================================================================

def calculate_derived_parameters(
    user_inputs: Dict,
    family_id: str,
) -> Dict:
    """
    Calculate all derived parameters from user inputs
    """
    
    floor_height = user_inputs.get("floor_height", 3000)
    stair_width = user_inputs.get("stair_width", 1200)
    tread_depth = user_inputs.get("tread_depth", 300)
    
    # Get target riser from family config
    family_config = INPUT_PARAMETERS_BY_FAMILY.get(family_id, {})
    target_riser = (
        family_config.get("derived_outputs", {})
        .get("riser_count", {})
        .get("target_riser", 175)
    )
    
    # Calculate riser count and height
    riser_count = math.ceil(floor_height / target_riser)
    actual_riser_height = floor_height / riser_count
    
    # Validate riser (IS456: 150-190mm)
    MIN_RISER, MAX_RISER = 150, 190
    if not (MIN_RISER <= actual_riser_height <= MAX_RISER):
        riser_count = math.ceil(floor_height / MAX_RISER)
        if floor_height / riser_count < MIN_RISER:
            riser_count = math.floor(floor_height / MIN_RISER)
        actual_riser_height = floor_height / riser_count
    
    # Calculate flight dimensions
    flight_rise = floor_height / 2
    flight_length = (riser_count // 2) * tread_depth
    landing_length = stair_width + 200
    
    # Calculate structural dimensions
    waist_thickness = flight_rise / 20
    waist_thickness = max(120, min(200, waist_thickness))
    
    return {
        "floor_height": floor_height,
        "stair_width": stair_width,
        "tread_depth": tread_depth,
        "riser_height": actual_riser_height,
        "riser_count": riser_count,
        "flight_rise": flight_rise,
        "flight_length": flight_length,
        "landing_length": landing_length,
        "waist_thickness": waist_thickness,
    }


# ============================================================================
# VALIDATION
# ============================================================================

def validate_design(
    user_inputs: Dict,
    derived: Dict,
    family_id: str,
) -> Dict:
    """
    Validate design against building codes
    """
    
    riser_height = derived.get("riser_height", 0)
    tread_depth = user_inputs.get("tread_depth", 0)
    floor_height = user_inputs.get("floor_height", 0)
    stair_width = user_inputs.get("stair_width", 0)
    
    issues = []
    warnings = []
    
    # IS456 Validation
    if not (150 <= riser_height <= 190):
        issues.append(
            f"Riser height {riser_height:.0f}mm outside IS456 range (150-190mm)"
        )
    
    if not (250 <= tread_depth <= 350):
        issues.append(
            f"Tread depth {tread_depth:.0f}mm should be 250-350mm"
        )
    
    # Comfort formula: 2*riser + tread = 600±30mm
    comfort = 2 * riser_height + tread_depth
    if not (570 <= comfort <= 630):
        warnings.append(
            f"Comfort formula: 2*riser + tread = {comfort:.0f}mm (ideal 600±30mm)"
        )
    
    # Stair width validation
    if stair_width < 900:
        issues.append(f"Stair width {stair_width:.0f}mm too narrow (min 900mm)")
    elif stair_width > 2000:
        warnings.append(f"Stair width {stair_width:.0f}mm is unusually wide")
    
    if issues:
        return {
            "is_valid": False,
            "message": "Design has critical issues",
            "issues": issues,
            "warnings": warnings,
        }
    
    return {
        "is_valid": True,
        "message": f"✅ Valid design: {derived['riser_count']:.0f} risers @ {riser_height:.0f}mm, {tread_depth}mm tread",
        "issues": [],
        "warnings": warnings,
    }


# ============================================================================
# REINFORCEMENT GENERATION
# ============================================================================

def generate_reinforcement_schedule(
    geometry: Dict,
) -> Tuple[List[RebarPattern], str]:
    """
    Generate rebar schedule from geometry
    """
    
    rebars = []
    stair_width = geometry.get("stair_width", 1200)
    flight_length = geometry.get("flight_length", 2000)
    
    # ===== MAIN BOTTOM BARS =====
    rebars.append(RebarPattern(
        location="waist_slab_bottom",
        bar_size="Y16",
        spacing=150,
        count=math.ceil(stair_width / 150),
        total_length=stair_width * math.ceil(stair_width / 150),
        weight_per_bar=BAR_WEIGHTS.get("Y16", 1.0) * (stair_width / 1000),
    ))
    
    # ===== TOP BARS =====
    rebars.append(RebarPattern(
        location="waist_slab_top",
        bar_size="Y12",
        spacing=200,
        count=math.ceil(stair_width / 200),
        total_length=stair_width * math.ceil(stair_width / 200),
        weight_per_bar=BAR_WEIGHTS.get("Y12", 1.0) * (stair_width / 1000),
    ))
    
    # ===== DISTRIBUTION BARS =====
    rebars.append(RebarPattern(
        location="tread_riser_distribution",
        bar_size="Y12",
        spacing=200,
        count=int(flight_length / 200),
        total_length=flight_length,
        weight_per_bar=BAR_WEIGHTS.get("Y12", 1.0) * (flight_length / 1000),
    ))
    
    # ===== CORNER BARS =====
    rebars.append(RebarPattern(
        location="corner_bars",
        bar_size="Y16",
        spacing=0,
        count=4,
        total_length=800,
        weight_per_bar=BAR_WEIGHTS.get("Y16", 1.0) * 0.8,
    ))
    
    total_weight = sum(r.total_weight for r in rebars)
    summary = f"{len(rebars)} rebar patterns | Total weight: {total_weight:.1f}kg"
    
    return rebars, summary


# ============================================================================
# OUTPUT GENERATION
# ============================================================================

def schedule_to_dataframe(rebars: List[RebarPattern]) -> pd.DataFrame:
    """Convert rebar list to pandas DataFrame"""
    rows = []
    for rebar in rebars:
        rows.append({
            "Location": rebar.location.replace("_", " ").title(),
            "Bar Size": rebar.bar_size,
            "Spacing (mm)": f"{rebar.spacing:.0f}" if rebar.spacing > 0 else "Fixed",
            "Count": rebar.count,
            "Total Length (m)": f"{rebar.total_length / 1000:.2f}",
            "Weight/Bar (kg)": f"{rebar.weight_per_bar:.2f}",
            "Total Weight (kg)": f"{rebar.total_weight:.2f}",
        })
    return pd.DataFrame(rows)


def generate_stair_design(
    user_inputs: Dict,
    derived: Dict,
) -> Dict:
    """
    Main function: Generate complete staircase design
    """
    
    geometry = StairGeometry(
        floor_height=derived["floor_height"],
        stair_width=derived["stair_width"],
        tread_depth=derived["tread_depth"],
        riser_height=derived["riser_height"],
        riser_count=int(derived["riser_count"]),
        flight_rise=derived["flight_rise"],
        flight_length=derived["flight_length"],
        landing_length=derived["landing_length"],
        waist_thickness=derived["waist_thickness"],
    )
    
    rebars, rebar_summary = generate_reinforcement_schedule(geometry.to_dict())
    schedule_df = schedule_to_dataframe(rebars)
    
    return {
        "geometry": geometry.to_dict(),
        "rebars": [r.to_dict() for r in rebars],
        "rebar_schedule": schedule_df,
        "rebar_summary": rebar_summary,
        "total_weight": sum(r.total_weight for r in rebars),
    }
