import torch
from transformers import BertTokenizer, BertForQuestionAnswering, BertModel, BertForTokenClassification
import openai
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import OPENAI_API_KEY

MAX_LEN = 40

tokenizer_bert = BertTokenizer.from_pretrained("bert-base-uncased")
model_bert = BertModel.from_pretrained("bert-base-uncased")
model_qa = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer_ner = BertTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
model_ner = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

model = "text-davinci-003"
openai.api_key = os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def gpt3_summarize(text):
    max_tokens = 3000
    prompt=f"Summarize without losing any context dont include non ascii characters: {text}"
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokens = tokenizer.encode(prompt)
    num_tokens = len(tokens)

    if num_tokens > max_tokens:
        tokens = tokens[:-1]
        tokens = tokens[:max_tokens]
        prompt = tokenizer.decode(tokens)

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text

def create_embedding(text):
    inputs = tokenizer_bert(text, return_tensors="pt", truncation=True, padding=True, max_length=MAX_LEN)
    with torch.no_grad():
        outputs = model_bert(**inputs)
    return outputs["pooler_output"].squeeze().numpy()


def extract_entities(tokens, predictions):
    chunks = []
    current_chunk = []
    for token, label_idx in zip(tokens[0], predictions[0]):
        label = model_ner.config.id2label[label_idx.item()]
        if label.startswith("B-"):
            if current_chunk:
                chunks.append(tokenizer_ner.decode(current_chunk, skip_special_tokens=True))
                current_chunk = []
            current_chunk.append(token)
        elif label.startswith("I-") and current_chunk:
            current_chunk.append(token)
        else:
            if current_chunk:
                chunks.append(tokenizer_ner.decode(current_chunk, skip_special_tokens=True))
                current_chunk = []
    return chunks

def ner_chunk(text):
    tokenized_text = tokenizer_ner.tokenize(text)
    print("Tokenized Text:", tokenized_text)

    adjusted_max_len = MAX_LEN - 2  # -2 for [CLS] and [SEP]

    sub_sequences = [tokenized_text[i:i+adjusted_max_len] for i in range(0, len(tokenized_text), adjusted_max_len)]
    print("Sub Sequences:", sub_sequences)

    chunks = []
    for sub_seq in sub_sequences:
        
        tokens = tokenizer_ner.encode(sub_seq, add_special_tokens=True, return_tensors="pt")
        outputs = model_ner(tokens).logits
        predictions = torch.argmax(outputs, dim=2)
        chunks += extract_entities(tokens, predictions)
        print("Extracted Entities:", extract_entities(tokens, predictions))
    print("All Chunks:", chunks)

    return chunks

'''
def simple_chunk(text):
    chunks = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    return chunks
'''

def simple_chunk(text):
    chunks = [text[i:i+MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    summaries = []

    print(f"Total Chunks to Process: {len(chunks)}")
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(gpt3_summarize, chunk): chunk for chunk in chunks}
        for i, future in enumerate(as_completed(futures)):
            chunk = futures[future]
            try:
                summary = future.result()
                summaries.append(summary)
                print(f"Processed Chunk {i + 1}/{len(chunks)}")
            except Exception as e:
                print(f"Error processing chunk: {e}")

    print("All Chunks Processed.")
    return summaries

def chunk_and_embed(text):
    #print(text)
    chunks = simple_chunk(text)
    chunk_embeddings = [create_embedding(chunk) for chunk in chunks]
    return chunks, chunk_embeddings

def get_qa_embedding(question, context):
    inputs = tokenizer_bert(question, context, return_tensors="pt", truncation=True, padding=True, max_length=MAX_LEN)
    with torch.no_grad():
        answer = model_qa(**inputs)
    start, end = torch.argmax(answer["start_logits"]), torch.argmax(answer["end_logits"])
    return context[start:end]