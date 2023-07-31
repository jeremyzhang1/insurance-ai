from flask import Flask, request, jsonify
from utils import ocr, embeddings, database
import logging
from flask_cors import CORS
import openai
import os
import pinecone
import numpy as np
from config import OPENAI_API_KEY


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
def search_pinecone(query_embedding, top_k=3):
    index = pinecone.Index("insurancedocuments")
    results = index.query(vector=query_embedding, top_k=top_k, include_values=True)
    #print(results)
    if results and 'matches' in results and results['matches']:
        values = results['matches'][0]['values']
        if isinstance(values, np.ndarray):
            return values.tolist()
        return values
    return None

def query_gpt3(prompt, context=""):
    response = openai.Completion.create(
      engine="text-davinci-003",
      #prompt=f"using this context {context} \n\n answer this question {prompt}",
        prompt=f"in the tone of a medical professional answer using this answer {context} \n\n ",

      max_tokens=150  
    )
    return response.choices[0].text.strip()

def guess(prompt):
    
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Answer this question succinctly and in the tone of a medical professional come up with a estimate but be confident about it {prompt}",
      max_tokens=150  
    )
    return response.choices[0].text.strip()

@app.route('/next', methods=['POST'])
def next_endpoint():

    try:

        data = request.json
        prompt = data['prompt']
        print(guess(prompt))
        embedded_prompt = embeddings.create_embedding(guess(prompt))
        #print(type(embedded_prompt))
        results = search_pinecone(embedded_prompt.tolist(), 3)
            
        context = results[0] if results else ""
            
        answer = query_gpt3(prompt, context)
            
        return jsonify({'status': 200, 'answer': answer}), 200

    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        
        if not allowed_file(file.filename):
             return jsonify({'status': 400, 'message': 'Invalid file type'}), 400

        text = ocr.process_image(file)
        #embedded_text = embeddings.create_embedding(text)
        chunks, chunk_embeddings = embeddings.chunk_and_embed(text)
        #print("Chunks:", chunks)
        #print("Chunk Embeddings:", chunk_embeddings)
    
        ids = database.store_in_db(chunks, chunk_embeddings)
        
        logging.info(f"Successfully processed and stored chunks with ids: {ids}")

        return jsonify({'status': 200, 'message': 'Upload successful'}), 200
    except Exception as e:
        logging.error(f"Error during processing: {str(e)}")
        return jsonify({'status': 500, 'message': 'Internal Server Error'}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()