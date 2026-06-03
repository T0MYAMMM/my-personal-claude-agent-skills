#!/usr/bin/env python3
"""
Automation Decision Visualizer

Generates ASCII art diagrams for automation decisions.
Can be embedded in markdown reports or displayed in terminal.
"""

from typing import Dict, List


def generate_score_breakdown(scores: Dict[str, int], total: int) -> str:
    """Generate visual score breakdown"""

    # Bar chart for each dimension
    bars = []
    max_width = 40

    dimensions = {
        "frequency": "Frequency",
        "time": "Time",
        "error_cost": "Error Cost",
        "longevity": "Longevity"
    }

    for key, label in dimensions.items():
        score = scores.get(key, 0)
        bar_width = int((score / 5.0) * max_width)
        bar = "█" * bar_width
        bars.append(f"{label:12} [{score}/5] {bar}")

    diagram = f"""
╔══════════════════════════════════════════════════════════╗
║            AUTOMATION SCORE BREAKDOWN                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  {bars[0]:52}  ║
║  {bars[1]:52}  ║
║  {bars[2]:52}  ║
║  {bars[3]:52}  ║
║                                                          ║
║  Total Score: {total:4d}                                     ║
║  Formula: {scores['frequency']} × {scores['time']} × {scores['error_cost']} × {scores['longevity']} = {total:3d}                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    return diagram


def generate_decision_tree(score: int, decision: str) -> str:
    """Generate decision tree visualization"""

    # Determine position on tree
    if score > 40:
        marker = ">>> AUTOMATE NOW"
        pos_high = " ◄━━━━ YOU ARE HERE"
        pos_mid = ""
        pos_low = ""
    elif score >= 20:
        marker = ">>> AUTOMATE IF EASY"
        pos_high = ""
        pos_mid = " ◄━━━━ YOU ARE HERE"
        pos_low = ""
    else:
        marker = ">>> STAY MANUAL"
        pos_high = ""
        pos_mid = ""
        pos_low = " ◄━━━━ YOU ARE HERE"

    tree = f"""
              AUTOMATION DECISION TREE

                  YOUR SCORE: {score}
                       │
                       │
        ┌──────────────┴──────────────┐
        │                             │
    Score > 40                   Score ≤ 40
        │                             │
        │                  ┌──────────┴──────────┐
        │                  │                     │
  ✅ AUTOMATE NOW    Score 20-40            Score < 20
     (High ROI){pos_high}       │                     │
                         │                     │
                   AUTOMATE IF EASY      ❌ STAY MANUAL
                    (< 4 hrs){pos_mid}       (Low ROI){pos_low}


  {marker}

"""
    return tree


def generate_threshold_gauge(score: int) -> str:
    """Generate gauge showing score relative to thresholds"""

    # Gauge with markers at 20 and 40
    gauge_width = 50
    max_score = 100  # For display purposes

    # Clamp score to reasonable range
    display_score = min(score, max_score)

    # Calculate position
    pos = int((display_score / max_score) * gauge_width)
    threshold_20 = int((20 / max_score) * gauge_width)
    threshold_40 = int((40 / max_score) * gauge_width)

    # Build gauge line
    gauge = [' '] * gauge_width

    # Mark thresholds
    gauge[threshold_20] = '│'
    gauge[threshold_40] = '│'

    # Mark current position
    if pos < gauge_width:
        gauge[pos] = '●'

    gauge_str = ''.join(gauge)

    # Zone labels
    if score < 20:
        zone = "STAY MANUAL"
        emoji = "❌"
    elif score < 40:
        zone = "AUTOMATE IF EASY"
        emoji = "🤔"
    else:
        zone = "AUTOMATE NOW"
        emoji = "✅"

    diagram = f"""
╔══════════════════════════════════════════════════════════╗
║                 DECISION THRESHOLD GAUGE                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  0 ├{gauge_str}┤ 100+    ║
║     │           │                                        ║
║    20          40                                        ║
║                                                          ║
║  Zone: {zone:20} {emoji}                        ║
║  Your Score: {score:4d}                                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    return diagram


def generate_break_even_timeline(build_hours: float, weekly_savings: float, score: int) -> str:
    """Generate timeline showing break-even point"""

    if weekly_savings <= 0:
        return """
[Break-even analysis not available - insufficient time savings data]
"""

    break_even_weeks = build_hours / weekly_savings
    months = break_even_weeks / 4.3

    # Create timeline (24 months)
    timeline_months = 24
    timeline_width = 48

    break_even_pos = int((break_even_weeks / 4.3 / timeline_months) * timeline_width)
    break_even_pos = min(break_even_pos, timeline_width - 1)

    # Build timeline
    timeline = ['-'] * timeline_width
    timeline[break_even_pos] = '↓'

    timeline_str = ''.join(timeline)

    # Calculate 1-year ROI
    roi_1yr = (52 * weekly_savings) - build_hours

    diagram = f"""
╔══════════════════════════════════════════════════════════╗
║              BREAK-EVEN TIMELINE                         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Build Cost: {build_hours:5.1f} hours                               ║
║  Weekly Savings: {weekly_savings:5.1f} hours                         ║
║  Break-Even: {break_even_weeks:5.1f} weeks ({months:4.1f} months)              ║
║                                                          ║
║  0 months ├{timeline_str}┤ 24 months   ║
║            BREAK-EVEN POINT                              ║
║                                                          ║
║  ROI after 1 year: {roi_1yr:6.1f} hours {'(POSITIVE ✅)' if roi_1yr > 0 else '(NEGATIVE ❌)':16}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    return diagram


def generate_risk_matrix(override_flags: List[str], error_cost: int) -> str:
    """Generate risk factor matrix"""

    # Determine risk level
    risk_count = len(override_flags)
    high_error = error_cost >= 5

    if risk_count == 0 and not high_error:
        risk_level = "LOW"
        risk_emoji = "✅"
    elif risk_count <= 2 and error_cost <= 3:
        risk_level = "MEDIUM"
        risk_emoji = "⚠️"
    else:
        risk_level = "HIGH"
        risk_emoji = "🚨"

    # Format flags
    if override_flags:
        flag_lines = []
        for i, flag in enumerate(override_flags[:5], 1):  # Max 5 for display
            flag_lines.append(f"║  {i}. {flag:50} ║")
        if len(override_flags) > 5:
            flag_lines.append(f"║     ... and {len(override_flags) - 5} more                                  ║")
        flags_str = "\n".join(flag_lines)
    else:
        flags_str = "║  No significant risk factors identified              ║"

    diagram = f"""
╔══════════════════════════════════════════════════════════╗
║                   RISK ASSESSMENT                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Risk Level: {risk_level:10} {risk_emoji}                            ║
║  Risk Factors: {risk_count:2d}                                       ║
║  Error Cost: {error_cost}/5 {'(HIGH)' if error_cost >= 5 else '(MED)' if error_cost >= 3 else '(LOW)':6}                             ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
{flags_str}
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Recommendation:                                         ║
║  {('ADD VALIDATION LAYER' if risk_level != 'LOW' else 'Proceed with standard testing'):50}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    return diagram


def generate_full_report_visualization(task_data: Dict) -> str:
    """Generate complete visualization for markdown report"""

    score = (task_data["scores"]["frequency"] *
             task_data["scores"]["time"] *
             task_data["scores"]["error_cost"] *
             task_data["scores"]["longevity"])

    decision = "AUTOMATE NOW" if score > 40 else "AUTOMATE IF EASY" if score >= 20 else "STAY MANUAL"

    # Calculate weekly savings for break-even
    freq_hours = {5: 7, 3: 4, 1: 1, 0: 0}
    time_hours = {5: 2, 3: 1, 1: 0.5, 0: 0.1}
    weekly_savings = (freq_hours.get(task_data["scores"]["frequency"], 0) *
                     time_hours.get(task_data["scores"]["time"], 0))

    # Generate all visualizations
    parts = [
        "```",
        generate_score_breakdown(task_data["scores"], score).strip(),
        "",
        generate_threshold_gauge(score).strip(),
        "",
        generate_decision_tree(score, decision).strip(),
        ""
    ]

    if task_data.get("build_estimate", 0) > 0 and weekly_savings > 0:
        parts.append(generate_break_even_timeline(
            task_data["build_estimate"],
            weekly_savings,
            score
        ).strip())
        parts.append("")

    if task_data.get("override_flags") or task_data["scores"]["error_cost"] >= 3:
        parts.append(generate_risk_matrix(
            task_data.get("override_flags", []),
            task_data["scores"]["error_cost"]
        ).strip())

    parts.append("```")

    return "\n".join(parts)


if __name__ == "__main__":
    # Test visualization
    test_data = {
        "task_name": "Invoice Generation",
        "scores": {
            "frequency": 3,
            "time": 3,
            "error_cost": 5,
            "longevity": 5
        },
        "override_flags": ["High-stakes without validation", "Regulated industry"],
        "build_estimate": 8.0
    }

    print("\n" + "="*60)
    print("AUTOMATION DECISION VISUALIZATION TEST")
    print("="*60)
    print(generate_full_report_visualization(test_data))
