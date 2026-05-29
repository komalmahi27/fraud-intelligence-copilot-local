# ============================================
# MAIN ORCHESTRATION FILE
# ============================================

from agents.validation_agent import ValidationAgent
from agents.kpi_agent import KPIAgent
from agents.risk_agent import IntelligenceAgent
from agents.executive_ai_agent import ExecutiveAIAgent

import traceback


# ============================================
# DATASET PATH
# ============================================

dataset_path = (
    "data/PS_20174392719_1491204439457_log.csv"
)


# ============================================
# OPENROUTER API KEY
# ============================================

OPENROUTER_API_KEY = (
    "YOUR_OPENROUTER_API_KEY"
)


# ============================================
# MAIN EXECUTION
# ============================================

try:

    print("\n")
    print("=" * 70)
    print("AI FRAUD INTELLIGENCE PLATFORM")
    print("=" * 70)


    # ========================================
    # VALIDATION AGENT
    # ========================================

    print("\n[1/4] VALIDATION AGENT STARTING...\n")

    validation_agent = ValidationAgent(
        dataset_path
    )

    dataset_loaded = (
        validation_agent.load_dataset()
    )

    if not dataset_loaded:

        print("❌ DATASET LOADING FAILED")
        exit()

    validation_report = (
        validation_agent.validation_summary()
    )

    print("✅ VALIDATION AGENT COMPLETED\n")

    print("=" * 70)
    print("VALIDATION REPORT")
    print("=" * 70)

    for key, value in validation_report.items():

        print(f"\n{key}:\n")
        print(value)


    # ========================================
    # KPI AGENT
    # ========================================

    print("\n")
    print("=" * 70)
    print("[2/4] KPI INTELLIGENCE AGENT STARTING...")
    print("=" * 70)

    kpi_agent = KPIAgent(
        validation_agent.df
    )

    kpi_summary = (
        kpi_agent.kpi_summary()
    )

    print("✅ KPI AGENT COMPLETED\n")

    print("=" * 70)
    print("KPI INTELLIGENCE REPORT")
    print("=" * 70)

    for key, value in kpi_summary.items():

        print(f"\n{key}:\n")
        print(value)


    # ========================================
    # INTELLIGENCE AGENT
    # ========================================

    print("\n")
    print("=" * 70)
    print("[3/4] FRAUD INTELLIGENCE AGENT STARTING...")
    print("=" * 70)

    intelligence_agent = IntelligenceAgent(

        validation_agent.df,

        kpi_summary

    )

    intelligence_summary = (
        intelligence_agent
        .intelligence_summary()
    )

    print("✅ INTELLIGENCE AGENT COMPLETED\n")

    print("=" * 70)
    print("FRAUD INTELLIGENCE REPORT")
    print("=" * 70)

    for insight in intelligence_summary:

        print(f"\n🧠 {insight}")


    # ========================================
    # EXECUTIVE AI AGENT
    # ========================================

    print("\n")
    print("=" * 70)
    print("[4/4] EXECUTIVE AI AGENT STARTING...")
    print("=" * 70)

    executive_ai_agent = ExecutiveAIAgent(

        OPENROUTER_API_KEY,

        kpi_summary,

        intelligence_summary

    )

    try:

        ai_recommendations = (

            executive_ai_agent
            .generate_ai_recommendations()

        )

    except Exception as e:

        print("\n❌ EXECUTIVE AI AGENT FAILED")
        print(e)

        ai_recommendations = (
            "AI recommendation engine failed."
        )

    print("✅ EXECUTIVE AI AGENT COMPLETED\n")

    print("=" * 70)
    print("AI EXECUTIVE FRAUD RECOMMENDATIONS")
    print("=" * 70)

    print("\n")
    print(ai_recommendations)
    print("\n")


    # ========================================
    # FINAL SUCCESS
    # ========================================

    print("=" * 70)
    print("AI FRAUD INTELLIGENCE PIPELINE COMPLETED")
    print("=" * 70)


# ============================================
# GLOBAL ERROR HANDLING
# ============================================

except Exception as e:

    print("\n")
    print("=" * 70)
    print("SYSTEM FAILURE DETECTED")
    print("=" * 70)

    traceback.print_exc()

    print("\n")