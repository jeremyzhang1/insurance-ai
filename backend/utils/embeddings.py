import spacy
import torch
from transformers import BertTokenizer, BertForQuestionAnswering, BertModel

nlp_ner = spacy.load("en_core_web_sm")

tokenizer_bert = BertTokenizer.from_pretrained("bert-base-uncased")
model_bert = BertModel.from_pretrained("bert-base-uncased")

model_qa = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

def create_embedding(text):
    inputs = tokenizer_bert(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    return outputs["pooler_output"].squeeze().numpy()

def ner_chunk(text):
    doc = nlp_ner(text)
    chunks = [ent.text for ent in doc.ents]
    return chunks

def chunk_and_embed(text):
    chunks = ner_chunk(text)
    chunk_embeddings = [create_embedding(chunk) for chunk in chunks]
    return chunks, chunk_embeddings

def get_qa_embedding(question, context):
    inputs = tokenizer_bert(question, context, return_tensors="pt", truncation=True
