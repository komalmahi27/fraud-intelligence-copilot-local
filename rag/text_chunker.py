# rag/text_chunker.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.pdf_processor import extract_pdf_text


# ==================================================
# CHUNK CREATION FUNCTION
# ==================================================

def create_chunks():

    print("\nLOADING PDF TEXT...\n")

    raw_text = extract_pdf_text()

    print(
        f"Total extracted characters: "
        f"{len(raw_text)}"
    )

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )

    chunks = text_splitter.split_text(
        raw_text
    )

    print(
        f"\nTotal chunks created: "
        f"{len(chunks)}"
    )

    return chunks


# ==================================================
# GENERATE CHUNKS
# ==================================================

chunks = create_chunks()


# ==================================================
# TEST MODE
# ==================================================

if __name__ == "__main__":

    print(
        "\n========== TOTAL CHUNKS ==========\n"
    )

    print(len(chunks))

    print(
        "\n========== SAMPLE CHUNK ==========\n"
    )

    if chunks:

        print(chunks[0])

    else:

        print("No chunks generated.")