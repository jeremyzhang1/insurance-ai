import pinecone
import logging
from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, INDEX_NAME

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index_name = INDEX_NAME

'''
def initialize_index():
    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)
    pinecone.create_index(index_name, dimension=768, metric="euclidean")
    pinecone.deinit()

initialize_index()
'''

def remove_non_ascii(text):
    return text.encode('ascii', 'ignore').decode('ascii')


def store_in_db(chunks, chunk_embeddings):
    if not chunks or not chunk_embeddings:
        logging.error("Chunks or chunk embeddings list is empty. Aborting upsert operation.")
        return None

    if len(chunks) != len(chunk_embeddings):
        logging.error("Length of chunks and chunk embeddings don't match. Aborting upsert operation.")
        return None

    formatted_vectors = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        if len(chunk) > 512 or len(chunk) < 1:
            #chunk_id = generate_id(chunk)
            continue
        else:
            #chunk_id = chunk.strip()
            chunk_id = remove_non_ascii(chunk)
        
        formatted_vectors.append((chunk_id, embedding.tolist(), {}))

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    if index_name in pinecone.list_indexes():
        index = pinecone.Index(index_name)
    else:
        index = pinecone.create_index(index_name, dimension=768, metric="euclidean")

    upsert_result = index.upsert(vectors=formatted_vectors)


'''
def query_db(query_embedding, top_k=5):
    pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
    query_embedding = query_embedding.tolist() if isinstance(query_embedding, torch.Tensor) else query_embedding
    query_result = index.query(queries=[query_embedding], top_k=top_k)  
    pinecone.deinit()
    return query_result
'''
def delete_index():
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    pinecone.delete_index(index_name)
    pinecone.deinit()
