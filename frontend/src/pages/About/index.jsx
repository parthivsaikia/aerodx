import { Link } from "react-router-dom";
import { useScrollReveal } from "../../hooks/useScrollReveal";
import "./About.css";

function AboutPage() {
  const headerReveal = useScrollReveal({ threshold: 0.1 });
  const missionReveal = useScrollReveal({ threshold: 0.15 });
  const workflowReveal = useScrollReveal({ threshold: 0.15 });
  const techReveal = useScrollReveal({ threshold: 0.15 });
  const disclaimerReveal = useScrollReveal({ threshold: 0.15 });

  return (
    <div className="page">
      <div className="container">
        <div
          className={`about-header reveal ${headerReveal.isVisible ? "visible" : ""}`}
          ref={headerReveal.ref}
        >
          <h1>About AeroDx</h1>
          <p>AI-powered lung disease detection for faster, smarter diagnostics</p>
        </div>

        <div className="about-content">
          <section
            className={`about-section reveal ${missionReveal.isVisible ? "visible" : ""}`}
            ref={missionReveal.ref}
          >
            <h2>Our Mission</h2>
            <p>
              AeroDx aims to democratize access to advanced lung disease
              screening by leveraging deep learning and medical imaging
              analysis. We believe early detection saves lives, and AI can
              make expert-level diagnostics accessible to everyone.
            </p>
          </section>

          <section
            className={`about-section reveal ${workflowReveal.isVisible ? "visible" : ""}`}
            ref={workflowReveal.ref}
          >
            <h2>How It Works</h2>
            <div className="workflow-steps">
              <div className="workflow-step">
                <div className="workflow-num">1</div>
                <div>
                  <h4>Upload</h4>
                  <p>Upload your CT scan in standard formats (PNG, JPG, DICOM, NIfTI).</p>
                </div>
              </div>
              <div className="workflow-step">
                <div className="workflow-num">2</div>
                <div>
                  <h4>Analyze</h4>
                  <p>Our ML model analyzes using CNNs trained on thousands of labeled images.</p>
                </div>
              </div>
              <div className="workflow-step">
                <div className="workflow-num">3</div>
                <div>
                  <h4>Consult</h4>
                  <p>Chat with our AI assistant to understand results and get insights.</p>
                </div>
              </div>
              <div className="workflow-step">
                <div className="workflow-num">4</div>
                <div>
                  <h4>Report</h4>
                  <p>Generate a comprehensive PDF report for your healthcare provider.</p>
                </div>
              </div>
            </div>
          </section>

          <section
            className={`about-section reveal ${techReveal.isVisible ? "visible" : ""}`}
            ref={techReveal.ref}
          >
            <h2>Technology Stack</h2>
            <div className="tech-grid">
              <div className="tech-card">
                <h4>🧠 Deep Learning</h4>
                <p>CNN-based model trained on large medical imaging datasets</p>
              </div>
              <div className="tech-card">
                <h4>⚡ FastAPI</h4>
                <p>High-performance Python backend with async support</p>
              </div>
              <div className="tech-card">
                <h4>⚛️ React</h4>
                <p>Modern, responsive frontend built with React 19</p>
              </div>
              <div className="tech-card">
                <h4>💬 NLP Chat</h4>
                <p>AI-powered medical assistant for result interpretation</p>
              </div>
            </div>
          </section>

          <section
            className={`about-section disclaimer-section reveal-scale ${disclaimerReveal.isVisible ? "visible" : ""}`}
            ref={disclaimerReveal.ref}
          >
            <h2>⚠️ Important Disclaimer</h2>
            <p>
              AeroDx is a screening tool designed to assist healthcare
              professionals. It does <strong>not</strong> provide medical
              diagnoses. Results should always be reviewed by a qualified
              physician. Never make treatment decisions based solely on AI analysis.
            </p>
          </section>

          <div className="about-cta">
            <h2>Ready to try AeroDx?</h2>
            <Link to="/scan" className="btn btn-primary btn-lg">
              Upload Your First Scan
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutPage;
