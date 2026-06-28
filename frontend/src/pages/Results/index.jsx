import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Results.css";

function ResultsPage() {
  const [animated, setAnimated] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      try {
        const res = await fetch("http://localhost:8000/scans/latest/result");
        if (res.ok) {
          const data = await res.json();
          setResults(
            data.predictions || [
              { disease: data.disease, confidence: data.confidence * 100 },
            ]
          );
        } else {
          throw new Error("No results");
        }
      } catch {
        setResults([
          { disease: "Pneumonia", confidence: 94 },
          { disease: "Tuberculosis", confidence: 12 },
          { disease: "Lung Cancer", confidence: 5 },
          { disease: "COVID-19", confidence: 8 },
          { disease: "Fibrosis", confidence: 3 },
          { disease: "Normal", confidence: 6 },
        ]);
      }
      setLoading(false);
    };
    fetchResults();
  }, []);

  // Trigger bar/ring animations after results load
  useEffect(() => {
    if (results && !loading) {
      const timer = setTimeout(() => setAnimated(true), 300);
      return () => clearTimeout(timer);
    }
  }, [results, loading]);

  const getStatusColor = (confidence) => {
    if (confidence >= 70) return "var(--danger)";
    if (confidence >= 40) return "var(--warning)";
    return "var(--success)";
  };

  const getStatusLabel = (confidence) => {
    if (confidence >= 70) return "High Risk";
    if (confidence >= 40) return "Moderate";
    return "Low Risk";
  };

  if (loading) {
    return (
      <div className="page">
        <div className="container">
          <div className="results-loading">
            <div className="loading-spinner"></div>
            <p>Loading analysis results...</p>
          </div>
        </div>
      </div>
    );
  }

  const primaryResult = results[0];

  return (
    <div className="page">
      <div className="container">
        <div className="results-header fade-in-up">
          <h1>Analysis Results</h1>
          <p>AI-powered diagnosis from your CT scan</p>
        </div>

        <div className="results-layout">
          <div className="primary-result-card slide-in-left">
            <div
              className={`result-badge ${primaryResult.confidence >= 70 ? "high" : primaryResult.confidence >= 40 ? "moderate" : "low"}`}
            >
              {getStatusLabel(primaryResult.confidence)}
            </div>
            <h2 className="primary-disease">{primaryResult.disease}</h2>
            <div className="confidence-ring">
              <svg viewBox="0 0 120 120" className="ring-svg">
                <circle cx="60" cy="60" r="52" className="ring-bg" />
                <circle
                  cx="60"
                  cy="60"
                  r="52"
                  className="ring-fill"
                  style={{
                    strokeDasharray: `${animated ? (primaryResult.confidence / 100) * 327 : 0} 327`,
                    stroke: getStatusColor(primaryResult.confidence),
                  }}
                />
              </svg>
              <div className="ring-text">
                <span className="ring-value">
                  {animated ? primaryResult.confidence : 0}%
                </span>
                <span className="ring-label">Confidence</span>
              </div>
            </div>
            <div className="result-actions">
              <Link to="/chat" className="btn btn-primary">
                Discuss with AI
              </Link>
              <Link to="/reports" className="btn btn-secondary">
                Generate Report
              </Link>
            </div>
          </div>

          <div className="all-results-card slide-in-right">
            <h3>Full Breakdown</h3>
            <div className="results-list">
              {results.map((result, i) => (
                <div
                  key={result.disease}
                  className="result-row"
                  style={{ animationDelay: `${i * 100}ms` }}
                >
                  <span className="result-disease">{result.disease}</span>
                  <div className="result-bar-container">
                    <div className="result-bar">
                      <div
                        className="result-bar-fill"
                        style={{
                          width: animated ? `${result.confidence}%` : "0%",
                          background: getStatusColor(result.confidence),
                          transitionDelay: `${i * 100}ms`,
                        }}
                      ></div>
                    </div>
                    <span className="result-percent">
                      {animated ? result.confidence : 0}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
            <div className="results-timestamp">
              <span>🕐 Analyzed: {new Date().toLocaleString()}</span>
            </div>
          </div>

          <div className="info-cards">
            <div className="info-card fade-in-up" style={{ animationDelay: "300ms" }}>
              <h4>⚠️ Disclaimer</h4>
              <p>
                This AI analysis is for screening purposes only and does not
                constitute a medical diagnosis. Please consult a qualified
                healthcare professional.
              </p>
            </div>
            <div className="info-card fade-in-up" style={{ animationDelay: "400ms" }}>
              <h4>📊 Next Steps</h4>
              <p>
                Use the AI Chat to ask questions about your results, or
                generate a PDF report to share with your doctor.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
