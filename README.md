# 🚀 **Insurance DocuMentor**

Welcome to **Insurance DocuMentor**, a state-of-the-art web application that transforms the way users interact with their insurance documents. By leveraging advanced OCR, local embedding bases, and LLMs **Insurance DocuMentor** not only serves as a insurance benefit comprehension tool but provides enlightening recommendations in an accessible chat format.

## 🌟 **Features**:

- **📜 Document Processing Wizard**: Effortlessly upload your insurance documents in PDF format, and watch as the magic unfolds!
  
- **🔍 Dynamic Information Retrieval**: Gone are the days of endless searching. Our app meticulously extracts and processes content, putting information at your fingertips.

- **💬 AI-Driven Interactive Chat**: Ever wished for a knowledgeable assistant? Engage with our AI chatbot, which draws from the document's essence to deliver precise answers to your queries. 

## 🛠 **Tech Stack**:

### 🔧 Backend:
  - **Flask (Python)**:
    - OCR Processing with PyTesseract
    - Finetuned Named Entity Recognition and Topic Modeling
    - Integration with the Pinecone cloud database 
    - Synchronized with GPT-3
    - Concurrency with ThreadPoolExecutor
  
### 🎨 Frontend:
  - **React (JavaScript)**:
    -  MUI, responsive user interface

## 🚀 **Getting Started**:


1. **🌍 Environment Setup and Configuration**:

   Navigate to your `backend_directory` and create a file named `config.py`. This file will hold various configuration keys and settings that the backend relies on.

   Add the following content to `config.py`:
   
   ```python
   OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
   PINECONE_API_KEY = "YOUR_PINECONE_API_KEY_HERE"
   PINECONE_ENVIRONMENT = "YOUR_PINECONE_ENVIRONMENT_HERE"
   INDEX_NAME = "YOUR_INDEX_NAME_HERE"

2. **🔧 Boot Up the Backend**:
    ```bash
    cd backend_directory
    pip install -r requirements.txt
    python app.py
    ```

3. **🎨 Light Up the Frontend**:
    ```bash
    cd frontend_directory
    npm install
    npm start
    ```

3. 🎉 **Celebrate**: Simply navigate to `http://localhost:3000` in your favorite browser and bask in the brilliance of **Insurance DocuMentor**!

## 📖 **Usage**:

1. **📤 Upload & Unfold**: Hit that upload button and select your document. Witness as the application meticulously dissects and comprehends the content.
   
2. **🤖 Chat & Discover**: Propel your knowledge by engaging with our AI chatbot. Seek answers, and you shall receive, grounded in the very essence of your document.

## 💡 **Contributing**:

Your brilliance can make **Insurance DocuMentor** even brighter! 🌞
- 🍴 Fork away!
- 📝 For sweeping changes, do us a favor and open an issue first.
- 💼 Submit those pull requests and be part of something spectacular.

## 📜 **License**:

Distributed under the [MIT License](LICENSE). Because amazing projects deserve an equally awesome license!

**Insurance DocuMentor** - Lighting the path to document enlightenment. 🌟
