# ============================================
# KPI AGENT
# ============================================

class KPIAgent:

    # ----------------------------------------
    # Initialize Agent
    # ----------------------------------------

    def __init__(self, dataframe):

        self.df = dataframe

    # ----------------------------------------
    # Total Transactions
    # ----------------------------------------

    def total_transactions(self):

        return len(self.df)

    # ----------------------------------------
    # Total Fraud Transactions
    # ----------------------------------------

    def total_fraud_transactions(self):

        fraud_count = (

            self.df['isFraud']
            .sum()

        )

        return fraud_count

    # ----------------------------------------
    # Fraud Percentage
    # ----------------------------------------

    def fraud_percentage(self):

        fraud_percentage = (

            self.total_fraud_transactions()
            /
            self.total_transactions()

        ) * 100

        return fraud_percentage

    # ----------------------------------------
    # Total Transaction Volume
    # ----------------------------------------

    def total_transaction_volume(self):

        total_volume = (

            self.df['amount']
            .sum()

        )

        return total_volume

    # ----------------------------------------
    # Average Transaction Amount
    # ----------------------------------------

    def average_transaction_amount(self):

        average_amount = (

            self.df['amount']
            .mean()

        )

        return average_amount

    # ----------------------------------------
    # Total Fraud Amount
    # ----------------------------------------

    def total_fraud_amount(self):

        fraud_amount = (

            self.df[
                self.df['isFraud'] == 1
            ]['amount']
            .sum()

        )

        return fraud_amount

    # ----------------------------------------
    # Fraud Percentage by Type
    # ----------------------------------------

    def fraud_percentage_by_type(self):

        fraud_percentage = (

            self.df
            .groupby('type')['isFraud']
            .mean()

        ) * 100

        return fraud_percentage.sort_values(
            ascending=False
        )

    # ----------------------------------------
    # Highest Risk Transaction Type
    # ----------------------------------------

    def highest_risk_transaction_type(self):

        fraud_by_type = (
            self.fraud_percentage_by_type()
        )

        highest_risk_type = (
            fraud_by_type.idxmax()
        )

        highest_risk_percentage = (
            fraud_by_type.max()
        )

        return {

            "transaction_type":
            highest_risk_type,

            "fraud_percentage":
            highest_risk_percentage

        }

    # ----------------------------------------
    # Complete KPI Summary
    # ----------------------------------------

    def kpi_summary(self):

        summary = {

            "total_transactions":
            self.total_transactions(),

            "total_fraud_transactions":
            self.total_fraud_transactions(),

            "fraud_percentage":
            self.fraud_percentage(),

            "total_transaction_volume":
            self.total_transaction_volume(),

            "average_transaction_amount":
            self.average_transaction_amount(),

            "total_fraud_amount":
            self.total_fraud_amount(),

            "fraud_percentage_by_type":
            self.fraud_percentage_by_type(),

            "highest_risk_transaction_type":
            self.highest_risk_transaction_type()

        }

        return summary