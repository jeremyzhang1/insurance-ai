import React, { useState } from 'react';
import axios from 'axios';
import { Document, Page } from 'react-pdf';
import Chat from './Chat';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [startChat, setStartChat] = useState(false);
  const [file, setFile] = useState();
  const [uploadedFile, setUploadedFile] = useState();
  const [error, setError] = useState();
  const [pdfPreview, setPdfPreview] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    const url = 'http://localhost:5000/upload';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    axios
      .post(url, formData, config)
      .then((response) => {
        console.log(response.data);
        if (response.status === 200) {
          setUploadedFile(response.data.file);
          setStartChat(true);
          if (file.type === 'application/pdf') {
            const reader = new FileReader();
            reader.onload = () => {
              setPdfPreview(reader.result);
            };
            reader.readAsDataURL(file);
          }
        } else {
          setError('Failed to upload file.');
        }
      })
      .catch((error) => {
        console.error('Error uploading file: ', error);
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <h1>PDF File Upload</h1>
        </div>

        <div className="form-container">
            <form onSubmit={handleSubmit}>
                <label>Choose a file to upload:</label>
                <input type="file" onChange={handleChange} />
                <button type="submit">Upload</button>
            </form>

          {loading && <div className="loading">Loading...</div>}
          {pdfPreview && (
            <div className="preview-container">
              <Document
                file={pdfPreview} 
                onLoadSuccess={onDocumentLoadSuccess}
                onLoadError={(error) => setError(error)}
              >
                <Page pageNumber={pageNumber} />
              </Document>
              <div className="pagination">
                <p>
                  Page {pageNumber} of {numPages}
                </p>
                <button
                  disabled={pageNumber <= 1}
                  onClick={() => setPageNumber((prevPage) => prevPage - 1)}
                >
                  Previous
                </button>
                <button
                  disabled={pageNumber >= numPages}
                  onClick={() => setPageNumber((prevPage) => prevPage + 1)}
                >
                  Next
                </button>
              </div>
            </div>
          )}

          {error && <div className="error">Error uploading file: {error.message}</div>}
          {startChat && <Chat />}
        </div>
      </div>
    </div>
  );
}

export default App;
