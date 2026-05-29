import os

from dotenv import load_dotenv
from openai import OpenAI

from rag.retriever import retrieve_relevant_chunks
from rag.prompt_builder import build_copilot_prompt


# ==================================================
# LOAD ENV VARIABLES
# ==================================================

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env"
    )


# ==================================================
# OPENROUTER CLIENT
# ==================================================

CLIENT = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

print("OPENROUTER CLIENT INITIALIZED")


# ==================================================
# COPILOT RESPONSE FUNCTION
# ==================================================

def generate_copilot_response(
    user_question,
    fraud_analytics,
    ai_recommendations
):

    try:

        print("\n===================================")
        print("COPILOT STARTED")
        print("QUESTION:", user_question)
        print("===================================\n")

        # ======================================
        # VALIDATE QUESTION
        # ======================================

        if not user_question:

            return (
                "Please provide a valid question."
            )

        # ======================================
        # RAG RETRIEVAL
        # ======================================

        retrieved_chunks = retrieve_relevant_chunks(
            user_question
        )

        if not retrieved_chunks:

            retrieved_chunks = [
                "No relevant policy documents were retrieved."
            ]

        print("RETRIEVAL SUCCESS")
        print(
            f"Retrieved {len(retrieved_chunks)} chunks"
        )

        # ======================================
        # BUILD PROMPT
        # ======================================

        final_prompt = build_copilot_prompt(

            user_question,

            retrieved_chunks,

            fraud_analytics,

            ai_recommendations

        )

        print("PROMPT BUILT")

        # ======================================
        # OPENROUTER REQUEST
        # ======================================

        response = CLIENT.chat.completions.create(

            model="openai/gpt-4o-mini",

            messages=[

                {
                    "role": "system",

                    "content": """
You are an Enterprise Fraud Intelligence Copilot.

Your responsibilities:

- Interpret fraud policies
- Interpret compliance procedures
- Interpret investigation guidelines
- Analyze live fraud intelligence
- Explain risk patterns
- Recommend actions based on policy evidence

Rules:

1. Prioritize retrieved policy documents.
2. Use live fraud analytics when available.
3. Use AI recommendations when relevant.
4. Never invent policies.
5. If information is unavailable, say so.
6. Provide concise executive-level responses.
"""
                },

                {
                    "role": "user",

                    "content": final_prompt
                }

            ]

        )

        print(
            "OPENROUTER RESPONSE RECEIVED"
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        print(
            "COPILOT RESPONSE GENERATED"
        )

        return answer

    except Exception as e:

        print("\n===================================")
        print("COPILOT ERROR")
        print(str(e))
        print("===================================\n")

        return (
            "The Enterprise Fraud Intelligence "
            "Copilot is currently unavailable. "
            "Please try again later."
        )