from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import shutil
import traceback

from agents.validation_agent import ValidationAgent
from agents.kpi_agent import KPIAgent
from agents.risk_agent import IntelligenceAgent
from agents.executive_ai_agent import ExecutiveAIAgent

# ==================================================
# FASTAPI INITIALIZATION
# ==================================================

app = FastAPI()


# ==================================================
# CORS CONFIGURATION
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==================================================
# OPENROUTER API KEY
# ==================================================

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# ==================================================
# GLOBAL AGENT TRACKER
# ==================================================

agent_progress = []

latest_fraud_context = {

    "fraud_analytics": "",

    "ai_recommendations": ""

}
# ==================================================
# HOME ROUTE
# ==================================================

@app.get("/")
async def home():

    return FileResponse(
        "frontend/index.html"
    )

# ==================================================
# AGENT STATUS ROUTE
# ==================================================

@app.get("/agent-status")
def get_agent_status():

    return {

        "progress":
        agent_progress

    }


# ==================================================
# DATASET ANALYSIS ROUTE
# ==================================================

@app.post("/analyze-dataset")
def analyze_dataset(

    file: UploadFile = File(...)

):

    global agent_progress

    # RESET STATUS

    agent_progress = []

    try:

        # ==========================================
        # SAVE UPLOADED FILE
        # ==========================================

        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ==========================================
        # VALIDATION AGENT
        # ==========================================

        print("\n[VALIDATION AGENT STARTED]")

        agent_progress.append(
            "Validation Agent Running"
        )

        validation_agent = ValidationAgent(
            file_path
        )

        dataset_loaded = (
            validation_agent.load_dataset()
        )

        if not dataset_loaded:

            return {

                "error":
                "Dataset Loading Failed"

            }

        validation_summary = (
            validation_agent.validation_summary()
        )
        print("VALIDATION SUMMARY GENERATED")
        # UPDATE STATUS

        agent_progress.remove(
            "Validation Agent Running"
        )

        agent_progress.append(
            "Validation Agent Completed"
        )

        print("[VALIDATION AGENT COMPLETED]")


        # ==========================================
        # KPI AGENT
        # ==========================================

        print("\n[KPI AGENT STARTED]")

        agent_progress.append(
            "KPI Intelligence Agent Running"
        )

        kpi_agent = KPIAgent(
            validation_agent.df
        )

        kpi_summary = (
            kpi_agent.kpi_summary()
        )
        print("KPI SUMMARY GENERATED")

        # UPDATE STATUS

        agent_progress.remove(
            "KPI Intelligence Agent Running"
        )

        agent_progress.append(
            "KPI Intelligence Agent Completed"
        )

        print("[KPI AGENT COMPLETED]")


        # ==========================================
        # RISK INTELLIGENCE AGENT
        # ==========================================

        print("\n[RISK INTELLIGENCE AGENT STARTED]")

        agent_progress.append(
            "Risk Intelligence Agent Running"
        )

        intelligence_agent = IntelligenceAgent(

            validation_agent.df,

            kpi_summary

        )

        intelligence_summary = (

            intelligence_agent
            .intelligence_summary()

        )
        print("INTELLIGENCE SUMMARY GENERATED")

        # UPDATE STATUS

        agent_progress.remove(
            "Risk Intelligence Agent Running"
        )

        agent_progress.append(
            "Risk Intelligence Agent Completed"
        )

        print("[RISK INTELLIGENCE AGENT COMPLETED]")
        print("STARTING EXECUTIVE AI")


        # ==========================================
        # EXECUTIVE AI AGENT
        # ==========================================

        print("\n[EXECUTIVE AI AGENT STARTED]")

        agent_progress.append(
            "Executive AI Agent Running"
        )

        ai_recommendations = ""

        try:

            executive_ai_agent = ExecutiveAIAgent(

                OPENROUTER_API_KEY,

                kpi_summary,

                intelligence_summary

            )

            ai_recommendations = (

                executive_ai_agent
                .generate_ai_recommendations()

            )
            print("EXECUTIVE AI RESPONSE GENERATED")

        except Exception as e:

            print("\nEXECUTIVE AI ERROR:")
            print(e)

            ai_recommendations = (
                "AI recommendation engine unavailable."
            )

        finally:

            # UPDATE STATUS

            if (
                "Executive AI Agent Running"
                in agent_progress
            ):

                agent_progress.remove(
                    "Executive AI Agent Running"
                )

            agent_progress.append(
                "Executive AI Agent Completed"
            )

        print("[EXECUTIVE AI AGENT COMPLETED]")
        # ==========================================
        # STORE LIVE FRAUD CONTEXT
        # ==========================================

        latest_fraud_context["fraud_analytics"] = str(
            intelligence_summary
        )

        latest_fraud_context["ai_recommendations"] = (
            ai_recommendations
        )
        


        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return {

            "validation_summary": {

                "schema_validation":
                validation_summary[
                    "schema_validation"
                ],

                "missing_values":
                validation_summary[
                    "missing_values"
                ].to_dict(),

                "duplicate_rows":
                int(
                    validation_summary[
                        "duplicate_rows"
                    ]
                ),

                "datatype_validation":
                validation_summary[
                    "datatype_validation"
                ],

                "fraud_label_validation":
                validation_summary[
                    "fraud_label_validation"
                ]

            },

            "kpi_summary": {

                "total_transactions":
                int(
                    kpi_summary[
                        "total_transactions"
                    ]
                ),

                "total_fraud_transactions":
                int(
                    kpi_summary[
                        "total_fraud_transactions"
                    ]
                ),

                "fraud_percentage":
                float(
                    kpi_summary[
                        "fraud_percentage"
                    ]
                ),

                "total_transaction_volume":
                float(
                    kpi_summary[
                        "total_transaction_volume"
                    ]
                ),

                "average_transaction_amount":
                float(
                    kpi_summary[
                        "average_transaction_amount"
                    ]
                ),

                "total_fraud_amount":
                float(
                    kpi_summary[
                        "total_fraud_amount"
                    ]
                ),

                "fraud_percentage_by_type":
                kpi_summary[
                    "fraud_percentage_by_type"
                ].to_dict(),

                "highest_risk_transaction_type":
                kpi_summary[
                    "highest_risk_transaction_type"
                ]

            },

            "intelligence_summary":
            intelligence_summary,

            "ai_recommendations":
            ai_recommendations

        }

    # ==================================================
    # GLOBAL ERROR HANDLER
    # ==================================================

    except Exception as e:

        traceback.print_exc()

        return {

            "error":
            str(e)

        }
# ==================================================
# AI COPILOT ROUTE
# ==================================================

@app.post("/copilot-query")
async def copilot_query(question: dict):

    from rag.copilot import generate_copilot_response

    print("BEFORE FUNCTION")

    user_question = question["question"]

    fraud_analytics = latest_fraud_context[
        "fraud_analytics"
    ]

    ai_recommendations = latest_fraud_context[
        "ai_recommendations"
    ]

    result = generate_copilot_response(
        user_question,
        fraud_analytics,
        ai_recommendations
    )

    print("AFTER FUNCTION")

    return {
        "response": result
    }