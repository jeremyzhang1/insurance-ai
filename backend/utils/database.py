import pinecone

pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
index_name = "insurance_documents"

def initialize_index():
    # Check if the index exists
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, metric="cosine")
    pinecone.deinit()

def store_in_db(chunks, chunk_embeddings):
    pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
    upsert_result = pinecone.upsert(index_name, items=zip(chunks, chunk_embeddings))
    pinecone.deinit()
    return upsert_result

def query_db(query_embedding, top_k=5):
    pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
    query_result = pinecone.query(index_name, queries=[query_embedding], top_k=top_k)
    pinecone.deinit()
    return query_result

def delete_index():
    pinecone.init(api_key="fedcf13e-6b3e-4104-ae6d-00767426ae05", environment="us-west4-gcp-free")
    pinecone.delete_index(index_name)
    pinecone.deinit()
