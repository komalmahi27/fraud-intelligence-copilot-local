# rag/retriever.py

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(__file__)

INDEX_PATH = os.path.join(
    BASE_DIR,
    "faiss_index",
    "fraud_knowledge.index"
)

CHUNKS_PATH = os.path.join(
    BASE_DIR,
    "faiss_index",
    "chunks.pkl"
)


# ==================================================
# LOAD MODEL ONCE
# ==================================================

print("\n[RETRIEVER] Loading embedding model...")

MODEL = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("[RETRIEVER] Model loaded")


# ==================================================
# LOAD FAISS INDEX ONCE
# ==================================================

if not os.path.exists(INDEX_PATH):
    raise FileNotFoundError(
        f"FAISS index not found: {INDEX_PATH}"
    )

INDEX = faiss.read_index(INDEX_PATH)

print(
    f"[RETRIEVER] FAISS index loaded "
    f"({INDEX.ntotal} vectors)"
)


# ==================================================
# LOAD CHUNKS ONCE
# ==================================================

if not os.path.exists(CHUNKS_PATH):
    raise FileNotFoundError(
        f"Chunks file not found: {CHUNKS_PATH}"
    )

with open(CHUNKS_PATH, "rb") as f:
    CHUNKS = pickle.load(f)

print(
    f"[RETRIEVER] Loaded {len(CHUNKS)} chunks"
)


# ==================================================
# RETRIEVAL FUNCTION
# ==================================================

def retrieve_relevant_chunks(
    query: str,
    top_k: int = 5
):

    try:

        print("\n========== RETRIEVAL START ==========")
        print("QUERY:", query)

        if not query:
            return []

        # ==========================================
        # GENERATE QUERY EMBEDDING
        # ==========================================

        query_embedding = MODEL.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        print(
            "Embedding shape:",
            query_embedding.shape
        )

        # ==========================================
        # FAISS SEARCH
        # ==========================================

        distances, indices = INDEX.search(
            query_embedding,
            top_k
        )

        print(
            "Retrieved indices:",
            indices[0]
        )

        # ==========================================
        # FETCH CHUNKS
        # ==========================================

        results = []

        for idx in indices[0]:

            if (
                idx >= 0
                and idx < len(CHUNKS)
            ):

                results.append(
                    CHUNKS[idx]
                )

        print(
            f"Retrieved {len(results)} chunks"
        )

        print("========== RETRIEVAL END ==========\n")

        return results

    except Exception as e:

        print(
            "\n[RETRIEVER ERROR]"
        )

        print(str(e))

        return []