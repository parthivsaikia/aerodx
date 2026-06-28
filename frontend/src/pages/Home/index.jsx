import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useCountUp } from "../../hooks/useCountUp";
import { useScrollReveal } from "../../hooks/useScrollReveal";
import "./Home.css";

function AnimatedStat({ end, suffix = "", label }) {
  const { count, ref } = useCountUp(end, 2000);
  return (
    <div className="stat-item" ref={ref}>
      <span className="stat-number">
        {count}
        {suffix}
      </span>
      <span className="stat-label">{label}</span>
    </div>
  );
}

function HomePage() {
  const [backendStatus, setBackendStatus] = useState(null);

  const heroReveal = useScrollReveal({ threshold: 0.1 });
  const featuresReveal = useScrollReveal({ threshold: 0.15 });
  const statsReveal = useScrollReveal({ threshold: 0.2 });
  const trustReveal = useScrollReveal({ threshold: 0.15 });
  const ctaReveal = useScrollReveal({ threshold: 0.2 });

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((res) => res.json())
      .then((data) => setBackendStatus(data))
      .catch(() => setBackendStatus(null));
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div
            className={`hero-content reveal ${heroReveal.isVisible ? "visible" : ""}`}
            ref={heroReveal.ref}
          >
            <div className="hero-text">
              <span className="hero-badge">AI-Powered Diagnostics</span>
              <h1>Detect Lung Diseases with AI Precision</h1>
              <p className="hero-description">
                AeroDx uses advanced deep learning to analyze CT scans and
                detect lung diseases like pneumonia, tuberculosis, and lung
                cancer with high accuracy in seconds.
              </p>
              <div className="hero-actions">
                <Link to="/scan" className="btn btn-primary">
                  Upload CT Scan
                </Link>
                <Link to="/about" className="btn btn-secondary">
                  Learn More
                </Link>
              </div>
              <div className="backend-status">
                <span
                  className={`status-dot ${backendStatus ? "online" : "offline"}`}
                ></span>
                <span className="status-text">
                  {backendStatus
                    ? `Model ${backendStatus.model_loaded ? "Ready" : "Loading"} • v${backendStatus.version}`
                    : "Backend Offline"}
                </span>
              </div>
            </div>
            <div className="hero-visual">
              <div className="hero-card">
                <div className="scan-icon">🫁</div>
                <div className="scan-pulse"></div>
                <div className="scan-pulse pulse-2"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <p className="section-subtitle">
            Three simple steps to get AI-powered lung diagnostics
          </p>
          <div
            className={`features-grid stagger-children ${featuresReveal.isVisible ? "visible" : ""}`}
            ref={featuresReveal.ref}
          >
            <div className="feature-card">
              <div className="feature-icon">📤</div>
              <h3>Upload Scan</h3>
              <p>Upload your CT scan image in PNG, JPG, DICOM, or NIfTI format</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Analysis</h3>
              <p>Our ML model analyzes the scan and detects potential diseases</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📋</div>
              <h3>Get Report</h3>
              <p>View results, chat with AI assistant, and download PDF reports</p>
            </div>
          </div>
        </div>
      </section>

      {/* Animated Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div
            className={`stats-grid stagger-children ${statsReveal.isVisible ? "visible" : ""}`}
            ref={statsReveal.ref}
          >
            <AnimatedStat end={94} suffix="%" label="Accuracy Rate" />
            <AnimatedStat end={5} suffix="s" label="Analysis Time" />
            <AnimatedStat end={6} suffix="+" label="Detectable Diseases" />
            <AnimatedStat end={24} suffix="/7" label="Availability" />
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="trust-section">
        <div className="container">
          <h2 className="section-title">Trusted Analysis</h2>
          <p className="section-subtitle">
            Built with validated medical imaging datasets and modern ML architecture
          </p>
          <div
            className={`trust-grid stagger-children ${trustReveal.isVisible ? "visible" : ""}`}
            ref={trustReveal.ref}
          >
            <div className="trust-card">
              <div className="trust-icon">🔬</div>
              <h4>Validated Dataset</h4>
              <p>Trained on thousands of labeled CT scans from research institutions</p>
            </div>
            <div className="trust-card">
              <div className="trust-icon">🔒</div>
              <h4>Secure Processing</h4>
              <p>Your scans are processed locally and never stored without consent</p>
            </div>
            <div className="trust-card">
              <div className="trust-icon">📈</div>
              <h4>Continuously Improving</h4>
              <p>Model performance is regularly evaluated and updated</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div
            className={`cta-card reveal-scale ${ctaReveal.isVisible ? "visible" : ""}`}
            ref={ctaReveal.ref}
          >
            <h2>Ready to Get Started?</h2>
            <p>Upload your first CT scan and experience AI-powered diagnostics.</p>
            <Link to="/scan" className="btn btn-primary btn-lg">
              Start Analysis
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
