from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
index = None


def add_documents(text_chunks):

    global documents, index

    embeddings = model.encode(text_chunks)

    dimension = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    documents.extend(text_chunks)


def search(query, top_k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for idx in indices[0]:
        results.append(documents[idx])

    return results