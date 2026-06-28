import { useState } from "react";
import { useScrollReveal } from "../../hooks/useScrollReveal";
import "./Reports.css";

function ReportsPage() {
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [includeChat, setIncludeChat] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);

  const formReveal = useScrollReveal({ threshold: 0.1, delay: 100 });
  const listReveal = useScrollReveal({ threshold: 0.1, delay: 300 });

  const handleGenerate = () => {
    setGenerating(true);
    setGenerated(false);
    setTimeout(() => {
      setGenerating(false);
      setGenerated(true);
      setTimeout(() => setGenerated(false), 3000);
    }, 2000);
  };

  const previousReports = [
    { id: 1, date: "2026-06-28", disease: "Pneumonia", confidence: 94 },
    { id: 2, date: "2026-06-25", disease: "Normal", confidence: 87 },
    { id: 3, date: "2026-06-20", disease: "Tuberculosis", confidence: 76 },
  ];

  return (
    <div className="page">
      <div className="container">
        <div className="reports-header">
          <h1>Reports</h1>
          <p>Generate and manage your diagnostic reports</p>
        </div>

        <div className="reports-layout">
          <div
            className={`report-form-card reveal-left ${formReveal.isVisible ? "visible" : ""}`}
            ref={formReveal.ref}
          >
            <h3>Generate New Report</h3>
            <p className="form-desc">
              Create a comprehensive PDF report of your latest scan analysis.
            </p>

            <div className="form-group">
              <label htmlFor="patientName">Patient Name</label>
              <input
                id="patientName"
                type="text"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                placeholder="Enter patient name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="patientAge">Age</label>
              <input
                id="patientAge"
                type="number"
                value={patientAge}
                onChange={(e) => setPatientAge(e.target.value)}
                placeholder="Enter age"
              />
            </div>

            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={includeChat}
                  onChange={(e) => setIncludeChat(e.target.checked)}
                />
                <span>Include chat history in report</span>
              </label>
            </div>

            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={generating}
            >
              {generating ? (
                <>
                  <span className="spinner"></span>
                  Generating...
                </>
              ) : (
                "📄 Generate PDF Report"
              )}
            </button>

            {generated && (
              <div className="success-message">
                ✅ Report generated successfully!
              </div>
            )}
          </div>

          <div
            className={`previous-reports-card reveal-right ${listReveal.isVisible ? "visible" : ""}`}
            ref={listReveal.ref}
          >
            <h3>Previous Reports</h3>
            <div className="reports-list">
              {previousReports.map((report, i) => (
                <div
                  key={report.id}
                  className="report-item"
                  style={{ animationDelay: `${i * 100}ms` }}
                >
                  <div className="report-info">
                    <span className="report-disease">{report.disease}</span>
                    <span className="report-date">{report.date}</span>
                  </div>
                  <div className="report-meta">
                    <span className="report-confidence">
                      {report.confidence}% confidence
                    </span>
                    <button
                      className="download-btn"
                      aria-label={`Download report for ${report.disease}`}
                    >
                      ⬇️ Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReportsPage;
