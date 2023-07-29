from flask import Flask, request, jsonify
from utils import ocr, embeddings, database

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = ocr.process_image(file)
    embedded_text = embeddings.create_embedding(text)
    chunks, chunk_embeddings = embeddings.chunk_and_embed(text)
    
    ids = database.store_in_db(chunks, chunk_embeddings)
    
    status = {
        'status': 200,  
        'message': 'Upload successful',  
    }

    return jsonify(status)

if __name__ == "__main__":
    app.run()
