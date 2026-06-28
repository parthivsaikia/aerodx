import { Link } from "react-router-dom";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-grid">
          <div className="footer-brand">
            <h3>🫁 AeroDx</h3>
            <p>
              AI-powered lung disease detection from CT scans.
              Fast, accurate, and accessible diagnostics.
            </p>
          </div>

          <div className="footer-links">
            <h4>Navigation</h4>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/scan">Upload Scan</Link></li>
              <li><Link to="/results">Results</Link></li>
              <li><Link to="/chat">AI Chat</Link></li>
            </ul>
          </div>

          <div className="footer-links">
            <h4>Resources</h4>
            <ul>
              <li><Link to="/reports">Reports</Link></li>
              <li><Link to="/about">About</Link></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; 2026 AeroDx. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
