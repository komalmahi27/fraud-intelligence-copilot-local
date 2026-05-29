# ============================================
# VALIDATION AGENT
# ============================================

import pandas as pd


class ValidationAgent:

    # ----------------------------------------
    # Initialize Agent
    # ----------------------------------------

    def __init__(self, file_path):

        self.file_path = file_path

        self.df = None

        # Required financial fraud columns

        self.required_columns = [

            "amount",
            "type",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
            "isFraud"

        ]

    # ----------------------------------------
    # Load Dataset
    # ----------------------------------------

    def load_dataset(self):

        try:

            self.df = pd.read_csv(self.file_path,nrows=50000)

            return True

        except Exception as e:

            print(f"Dataset Loading Error: {e}")

            return False

    # ----------------------------------------
    # Schema Validation
    # ----------------------------------------

    def validate_schema(self):

        dataset_columns = self.df.columns.tolist()

        missing_columns = [

            column

            for column in self.required_columns

            if column not in dataset_columns

        ]

        if len(missing_columns) > 0:

            return {

                "status": False,

                "missing_columns": missing_columns

            }

        return {

            "status": True,

            "missing_columns": []

        }

    # ----------------------------------------
    # Missing Value Check
    # ----------------------------------------

    def check_missing_values(self):

        missing_values = (

            self.df
            .isnull()
            .sum()

        )

        return missing_values

    # ----------------------------------------
    # Duplicate Check
    # ----------------------------------------

    def check_duplicates(self):

        duplicates = (

            self.df
            .duplicated()
            .sum()

        )

        return duplicates

    # ----------------------------------------
    # Data Type Validation
    # ----------------------------------------

    def validate_data_types(self):

        expected_numeric_columns = [

            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest"

        ]

        invalid_columns = []

        for column in expected_numeric_columns:

            if not pd.api.types.is_numeric_dtype(
                self.df[column]
            ):

                invalid_columns.append(column)

        if len(invalid_columns) > 0:

            return {

                "status": False,

                "invalid_columns": invalid_columns

            }

        return {

            "status": True,

            "invalid_columns": []

        }

    # ----------------------------------------
    # Fraud Label Validation
    # ----------------------------------------

    def validate_fraud_labels(self):

        unique_values = (
            self.df['isFraud']
            .unique()
        )

        valid_values = {0, 1}

        if not set(unique_values).issubset(valid_values):

            return False

        return True

    # ----------------------------------------
    # Complete Validation Pipeline
    # ----------------------------------------

    def validation_summary(self):

        schema_validation = self.validate_schema()

        datatype_validation = self.validate_data_types()

        fraud_label_validation = (
            self.validate_fraud_labels()
        )

        summary = {

            "schema_validation":
            schema_validation,

            "missing_values":
            self.check_missing_values(),

            "duplicate_rows":
            self.check_duplicates(),

            "datatype_validation":
            datatype_validation,

            "fraud_label_validation":
            fraud_label_validation

        }

        return summary