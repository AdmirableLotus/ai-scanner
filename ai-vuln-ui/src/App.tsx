import { useState } from "react";
import axios from "axios";
import "./App.css";

interface Finding {
  type: string;
  line: number;
  code: string;
  severity: string;
  description: string;
}

interface AnalysisResult {
  ai_analysis: string;
  static_findings: Finding[];
  summary: {
    total_issues: number;
    critical: number;
    high: number;
    medium: number;
  };
}

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", { code });
      setResult(response.data);
    } catch (err: any) {
      setError("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical': return '#dc3545';
      case 'High': return '#fd7e14';
      case 'Medium': return '#ffc107';
      default: return '#6c757d';
    }
  };

  return (
    <div className="container">
      <h1>Red Lotus Scan</h1>
      <textarea
        placeholder="Paste your code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <button onClick={analyze} disabled={loading || !code.trim()}>
        {loading ? "Scanning..." : "Analyze"}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {result && (
        <div className="results">
          <div className="summary">
            <h3>Summary</h3>
            <div className="stats">
              <span className="stat critical">Critical: {result.summary.critical}</span>
              <span className="stat high">High: {result.summary.high}</span>
              <span className="stat medium">Medium: {result.summary.medium}</span>
              <span className="stat total">Total: {result.summary.total_issues}</span>
            </div>
          </div>
          
          {result.static_findings.length > 0 && (
            <div className="findings">
              <h3>Static Analysis Findings</h3>
              {result.static_findings.map((finding, index) => (
                <div key={index} className="finding" style={{borderLeft: `4px solid ${getSeverityColor(finding.severity)}`}}>
                  <div className="finding-header">
                    <span className="severity" style={{color: getSeverityColor(finding.severity)}}>
                      {finding.severity}
                    </span>
                    <span className="type">{finding.type.replace('_', ' ').toUpperCase()}</span>
                    <span className="line">Line {finding.line}</span>
                  </div>
                  <div className="description">{finding.description}</div>
                  <code className="code-snippet">{finding.code}</code>
                </div>
              ))}
            </div>
          )}
          
          <div className="ai-analysis">
            <h3>AI Analysis</h3>
            <pre className="output">{result.ai_analysis}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;