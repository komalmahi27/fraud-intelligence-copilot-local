# ============================================
# EXECUTIVE AI AGENT
# ============================================

import requests
import json


class ExecutiveAIAgent:

    # ----------------------------------------
    # Initialize Agent
    # ----------------------------------------

    def __init__(

        self,

        api_key,

        kpi_summary,

        intelligence_summary

    ):

        self.api_key = api_key

        self.kpi_summary = kpi_summary

        self.intelligence_summary = (
            intelligence_summary
        )

        self.api_url = (
            "https://openrouter.ai/api/v1/chat/completions"
        )

    # ----------------------------------------
    # Generate Prompt
    # ----------------------------------------

    def generate_prompt(self):

        prompt = f"""

You are a senior financial fraud intelligence analyst.

Analyze the following fraud intelligence data
and generate:

1. Executive fraud observations
2. Fraud mitigation recommendations
3. Operational risk insights
4. Banking security recommendations
5. Strategic fraud prevention suggestions

KPI SUMMARY:

{self.kpi_summary}


INTELLIGENCE SUMMARY:

{self.intelligence_summary}

"""

        return prompt

    # ----------------------------------------
    # Generate AI Recommendations
    # ----------------------------------------

    def generate_ai_recommendations(self):

        headers = {

            "Authorization":
            f"Bearer {self.api_key}",

            "Content-Type":
            "application/json"

        }

        payload = {

            "model":
            "openai/gpt-3.5-turbo",

            "messages": [

                {

                    "role": "user",

                    "content":
                    self.generate_prompt()

                }

            ]

        }

        response = requests.post(

            self.api_url,

            headers=headers,

            data=json.dumps(payload)

        )

        result = response.json()

        ai_output = (

            result['choices'][0]
            ['message']['content']

        )

        return ai_output