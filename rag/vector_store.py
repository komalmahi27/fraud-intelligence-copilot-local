import os
import pickle
import faiss
import numpy as np

from rag.text_chunker import chunks
from rag.embeddings import generate_embeddings


# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(__file__)

FAISS_DIR = os.path.join(
    BASE_DIR,
    "faiss_index"
)

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "fraud_knowledge.index"
)

CHUNKS_PATH = os.path.join(
    FAISS_DIR,
    "chunks.pkl"
)


# ==================================================
# BUILD VECTOR STORE
# ==================================================

def build_vector_store():

    print("\n===================================")
    print("BUILDING VECTOR STORE")
    print("===================================\n")

    # ==========================================
    # CREATE OUTPUT DIRECTORY
    # ==========================================

    os.makedirs(
        FAISS_DIR,
        exist_ok=True
    )

    # ==========================================
    # GENERATE EMBEDDINGS
    # ==========================================

    embeddings = generate_embeddings(
        chunks
    )

    embedding_array = np.asarray(
        embeddings,
        dtype=np.float32
    )

    print(
        f"Embedding shape: "
        f"{embedding_array.shape}"
    )

    # ==========================================
    # CREATE FAISS INDEX
    # ==========================================

    dimension = embedding_array.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    # ==========================================
    # STORE VECTORS
    # ==========================================

    index.add(
        embedding_array
    )

    print(
        f"Stored {index.ntotal} vectors"
    )

    # ==========================================
    # SAVE INDEX
    # ==========================================

    faiss.write_index(
        index,
        INDEX_PATH
    )

    # ==========================================
    # SAVE CHUNK MAPPING
    # ==========================================

    with open(
        CHUNKS_PATH,
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )

    print(
        "\nFAISS INDEX SAVED"
    )

    print(
        f"Index Path: {INDEX_PATH}"
    )

    print(
        f"Chunks Path: {CHUNKS_PATH}"
    )

    print(
        "\nVECTOR STORE BUILD COMPLETE\n"
    )


# ==================================================
# EXECUTE DIRECTLY
# ==================================================

if __name__ == "__main__":

    build_vector_store()