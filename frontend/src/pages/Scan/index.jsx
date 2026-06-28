import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useScrollReveal } from "../../hooks/useScrollReveal";
import "./Scan.css";

function ScanPage() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const headerReveal = useScrollReveal({ threshold: 0.1 });
  const uploadReveal = useScrollReveal({ threshold: 0.1, delay: 200 });
  const instructionsReveal = useScrollReveal({ threshold: 0.1, delay: 400 });

  const handleFile = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      const imageUrl = URL.createObjectURL(selectedFile);
      setImage(imageUrl);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setUploading(true);
    setProgress(0);

    // Simulate progress animation
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) {
          clearInterval(interval);
          return 95;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    setTimeout(() => {
      clearInterval(interval);
      setProgress(100);
      setTimeout(() => {
        setUploading(false);
        navigate("/results");
      }, 500);
    }, 2500);
  };

  return (
    <div className="page">
      <div className="container">
        <div
          className={`scan-page-header reveal ${headerReveal.isVisible ? "visible" : ""}`}
          ref={headerReveal.ref}
        >
          <h1>Upload CT Scan</h1>
          <p>Upload a CT scan image for AI-powered analysis</p>
        </div>

        <div className="scan-layout">
          {/* Upload Area */}
          <div
            className={`upload-section reveal-left ${uploadReveal.isVisible ? "visible" : ""}`}
            ref={uploadReveal.ref}
          >
            <div
              className={`upload-zone ${dragActive ? "drag-active" : ""} ${image ? "has-image" : ""}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => fileInputRef.current?.click()}
              role="button"
              tabIndex={0}
              aria-label="Upload CT scan image"
            >
              {image ? (
                <div className="preview-container">
                  <img src={image} alt="CT Scan Preview" className="scan-preview" />
                  <div className="preview-overlay">
                    <span>Click to change</span>
                  </div>
                </div>
              ) : (
                <div className="upload-placeholder">
                  <div className="upload-icon">📤</div>
                  <h3>Drop your CT scan here</h3>
                  <p>or click to browse files</p>
                  <span className="upload-formats">
                    Supports: PNG, JPG, DICOM, NIfTI
                  </span>
                </div>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*,.dcm,.nii,.nii.gz"
                onChange={(e) => handleFile(e.target.files[0])}
                className="file-input-hidden"
                aria-hidden="true"
              />
            </div>

            {file && (
              <div className="file-info fade-in">
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>
            )}

            {/* Progress Bar */}
            {uploading && (
              <div className="progress-wrapper fade-in">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <span className="progress-text">{Math.round(progress)}%</span>
              </div>
            )}

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={!file || uploading}
            >
              {uploading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                "🔍 Analyze Scan"
              )}
            </button>
          </div>

          {/* Instructions Panel */}
          <div
            className={`instructions-panel reveal-right ${instructionsReveal.isVisible ? "visible" : ""}`}
            ref={instructionsReveal.ref}
          >
            <h3>Instructions</h3>
            <ul className="instruction-list">
              <li>
                <span className="step-num">1</span>
                <div>
                  <strong>Upload Image</strong>
                  <p>Drag and drop or click to select a CT scan image</p>
                </div>
              </li>
              <li>
                <span className="step-num">2</span>
                <div>
                  <strong>Run Analysis</strong>
                  <p>Click "Analyze Scan" to start AI inference</p>
                </div>
              </li>
              <li>
                <span className="step-num">3</span>
                <div>
                  <strong>View Results</strong>
                  <p>Get instant predictions with confidence scores</p>
                </div>
              </li>
            </ul>

            <div className="supported-conditions">
              <h4>Detectable Conditions</h4>
              <div className="condition-tags">
                <span className="tag">Pneumonia</span>
                <span className="tag">Tuberculosis</span>
                <span className="tag">Lung Cancer</span>
                <span className="tag">COVID-19</span>
                <span className="tag">Fibrosis</span>
                <span className="tag">Normal</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScanPage;
