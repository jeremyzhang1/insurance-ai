import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import Chat from './Chat';
import './App.css';
import Recommendations from './Reccomend';

import workerSrc from 'pdfjs-dist/build/pdf.worker.entry.js';
pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

function App() {
  const [loading, setLoading] = useState(false);
  const [startChat, setStartChat] = useState(false);
  const [file, setFile] = useState();
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function handleChange(event) {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  }

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setStartChat(false); 
    setTimeout(() => {
      setLoading(false);
      setStartChat(true);
    }, 2000); 
  }

  return (
    <div className="App">
      <div className="sidebar">
        <div className="header">
          <h1>ReidAssure Insurance</h1>
        </div>
      
        <div className="form-container">
          <form onSubmit={handleSubmit}>
            <label>Choose a file to upload:</label>
            <input type="file" onChange={handleChange} />
            <button type="submit">Upload</button>
          </form>
          {loading && <div className="loading">Loading...</div>}
        </div>
        {/* Recommendations section */}
        {startChat && (
        <div className="recommendations-container">
          <Recommendations />
        </div>
        )}
      </div>

      <div className="container">
        {file && (
          <div className="preview-container">
            <Document
              file={file}
              onLoadSuccess={onDocumentLoadSuccess}
              error={<div>Error loading PDF.</div>}
              loading={<div>Loading PDF...</div>}
            >
              <Page
                pageNumber={pageNumber}
                className="pdf-page"
                renderTextLayer={false}
                ignoreClass="react-pdf__Page__annotations"
                scale = ".65"
              />
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

        {startChat && <Chat />}
      </div>
    </div>
  );
}
export default App;
