import pinecone
import numpy as np
import logging

pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
index_name = "insurancedocuments"
VECTOR_DIMENSION = 768

def remove_non_ascii(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def store_vectors_in_index(chunks, chunk_embeddings):
    if not chunks or not chunk_embeddings:
        logging.error("Chunks or chunk embeddings list is empty. Aborting upsert operation.")
        return

    if len(chunks) != len(chunk_embeddings):
        logging.error("Length of chunks and chunk embeddings don't match. Aborting upsert operation.")
        return

    formatted_vectors = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        chunk_id = remove_non_ascii(chunk)
        formatted_vectors.append((chunk_id, embedding, {}))

    if index_name in pinecone.list_indexes():
        index = pinecone.Index(index_name)
    else:
        logging.error("Index not found. Please create it first.")
        return

    upsert_result = index.upsert(vectors=formatted_vectors)
    return upsert_result

if __name__ == "__main__":
    sample_chunks = []
    sample_embeddings = [np.random.randn(VECTOR_DIMENSION).tolist() for _ in range(len(sample_chunks))]

    result = store_vectors_in_index(sample_chunks, sample_embeddings)
    print("Upsert result:", result)
