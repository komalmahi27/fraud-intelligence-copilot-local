# rag/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np


# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

print("\nLOADING EMBEDDING MODEL...\n")

MODEL = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("EMBEDDING MODEL LOADED")


# ==================================================
# GENERATE EMBEDDINGS
# ==================================================

def generate_embeddings(chunks):

    print("\nGENERATING EMBEDDINGS...\n")

    embeddings = MODEL.encode(

        chunks,

        convert_to_numpy=True,

        show_progress_bar=True,

        normalize_embeddings=True

    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    print(
        f"\nGenerated {len(embeddings)} embeddings"
    )

    print(
        f"Embedding dimension: "
        f"{embeddings.shape[1]}"
    )

    return embeddings


# ==================================================
# TEST MODE
# ==================================================

if __name__ == "__main__":

    from rag.text_chunker import chunks

    embeddings = generate_embeddings(
        chunks
    )

    print(
        "\n========== EMBEDDING RESULTS ==========\n"
    )

    print(
        f"Total embeddings: {len(embeddings)}"
    )

    print(
        f"Embedding dimension: "
        f"{embeddings.shape[1]}"
    )