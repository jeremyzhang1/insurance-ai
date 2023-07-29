from flask import Flask, request, jsonify
from utils import ocr, embeddings, database
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

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
