# ============================================
# INTELLIGENCE AGENT
# ============================================

class IntelligenceAgent:

    # ----------------------------------------
    # Initialize Agent
    # ----------------------------------------

    def __init__(self, dataframe, kpi_summary):

        self.df = dataframe

        self.kpi_summary = kpi_summary

    # ----------------------------------------
    # Fraud Concentration Analysis
    # ----------------------------------------

    def fraud_concentration_analysis(self):

        fraud_by_type = (
            self.kpi_summary[
                "fraud_percentage_by_type"
            ]
        )

        highest_risk = (
            fraud_by_type.idxmax()
        )

        return (
            f"Fraud activity is heavily "
            f"concentrated around "
            f"{highest_risk} transactions."
        )

    # ----------------------------------------
    # High Value Fraud Analysis
    # ----------------------------------------

    def high_value_fraud_analysis(self):

        fraud_df = (

            self.df[
                self.df['isFraud'] == 1
            ]

        )

        average_fraud_amount = (

            fraud_df['amount']
            .mean()

        )

        return (
            f"Fraudulent transactions "
            f"demonstrate unusually high "
            f"average transaction amounts "
            f"of {average_fraud_amount:,.2f}."
        )

    # ----------------------------------------
    # Balance Depletion Analysis
    # ----------------------------------------

    def balance_depletion_analysis(self):

        fraud_df = (

            self.df[
                self.df['isFraud'] == 1
            ]

        )

        average_balance_reduction = (

            fraud_df['oldbalanceOrg']
            -
            fraud_df['newbalanceOrig']

        ).mean()

        return (
            f"Fraudulent transactions "
            f"frequently involve aggressive "
            f"sender balance depletion "
            f"patterns averaging "
            f"{average_balance_reduction:,.2f}."
        )

    # ----------------------------------------
    # Operational Risk Observation
    # ----------------------------------------

    def operational_risk_observation(self):

        highest_risk = (

            self.kpi_summary[
                "highest_risk_transaction_type"
            ]['transaction_type']

        )

        return (
            f"{highest_risk} operations represent "
            f"the highest fraud exposure area "
            f"within the financial ecosystem."
        )

    # ----------------------------------------
    # Complete Intelligence Summary
    # ----------------------------------------

    def intelligence_summary(self):

        insights = [

            self.fraud_concentration_analysis(),

            self.high_value_fraud_analysis(),

            self.balance_depletion_analysis(),

            self.operational_risk_observation()

        ]

        return insights