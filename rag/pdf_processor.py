from PyPDF2 import PdfReader
import os


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = os.path.dirname(__file__)

KNOWLEDGE_BASE_PATH = os.path.join(
    BASE_DIR,
    "knowledge_base"
)


# ==================================================
# PDF TEXT EXTRACTION FUNCTION
# ==================================================

def extract_pdf_text():

    combined_text = ""

    if not os.path.exists(KNOWLEDGE_BASE_PATH):

        raise FileNotFoundError(
            f"Knowledge base folder not found:\n"
            f"{KNOWLEDGE_BASE_PATH}"
        )

    pdf_files = [

        file_name

        for file_name in os.listdir(
            KNOWLEDGE_BASE_PATH
        )

        if file_name.endswith(".pdf")

    ]

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF files found inside knowledge_base"
        )

    for file_name in pdf_files:

        pdf_path = os.path.join(
            KNOWLEDGE_BASE_PATH,
            file_name
        )

        print(
            f"\nProcessing PDF: {file_name}"
        )

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            text = page.extract_text()

            if text:

                combined_text += text + "\n"

    print(
        f"\nTotal extracted characters: "
        f"{len(combined_text)}"
    )

    return combined_text


# ==================================================
# TEST MODE
# ==================================================

if __name__ == "__main__":

    raw_text = extract_pdf_text()

    print(
        "\n========== EXTRACTED TEXT ==========\n"
    )

    print(raw_text[:5000])