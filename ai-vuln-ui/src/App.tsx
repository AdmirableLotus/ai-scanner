import { useState, useRef } from "react";
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
  bounty_report: string;
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
  const lotusRef = useRef<HTMLDivElement>(null);
  const rippleRef = useRef<HTMLDivElement>(null);

  const analyze = async () => {
    // Trigger lotus bloom animation
    if (lotusRef.current) {
      lotusRef.current.classList.remove('pulse');
      void lotusRef.current.offsetWidth; // restart animation
      lotusRef.current.classList.add('pulse');
    }
    
    // Trigger ripple animation
    if (rippleRef.current) {
      rippleRef.current.classList.remove('active');
      void rippleRef.current.offsetWidth; // restart animation
      rippleRef.current.classList.add('active');
    }
    
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await axios.post("http://127.0.0.1:5001/analyze", { code });
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
    <>
      {/* Glowing Red Lotus with Ripple */}
      <div className="lotus-bg" ref={lotusRef}>
        <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
          <g fill="rgba(255,0,0,0.12)" stroke="#ff3333" strokeWidth="2.5" strokeLinejoin="round">
            {/* Inner petals */}
            <path d="M256 200
                     C220 260, 220 340, 256 380
                     C292 340, 292 260, 256 200Z" />
            <path d="M256 210
                     C200 250, 190 340, 240 380
                     C200 320, 210 250, 256 210Z" />
            <path d="M256 210
                     C312 250, 322 340, 272 380
                     C312 320, 302 250, 256 210Z" />
            
            {/* Middle petals */}
            <path d="M256 190
                     C180 240, 170 360, 230 390
                     C180 320, 190 240, 256 190Z" />
            <path d="M256 190
                     C332 240, 342 360, 282 390
                     C332 320, 322 240, 256 190Z" />
            
            {/* Outer petals */}
            <path d="M256 170
                     C140 260, 160 400, 240 410
                     C150 330, 160 230, 256 170Z" />
            <path d="M256 170
                     C372 260, 352 400, 272 410
                     C362 330, 352 230, 256 170Z" />
            
            {/* Base leaves */}
            <path d="M180 370
                     C256 420, 332 370, 256 400
                     C210 380, 200 380, 180 370Z" />
          </g>
        </svg>
        
        {/* Ripple layer */}
        <div className="lotus-ripple" ref={rippleRef}></div>
      </div>
      
      {/* Scanning beam overlay */}
      <div className="scan-beam" aria-hidden="true"></div>
      
      <div className="container">
        <h1>Red Lotus Scan</h1>
        <textarea
          placeholder="Paste your code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
        <div className="controls">
          <button onClick={analyze} disabled={loading || !code.trim()} className={loading ? 'scanning' : ''}>
            {loading ? (
              <>
                <span className="scan-text">Scanning</span>
                <span className="dots">...</span>
              </>
            ) : "Analyze"}
          </button>
        </div>
      
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
          
          <div className="bounty-report">
            <h3>Bug Bounty Report</h3>
            <button 
              className="download-btn"
              onClick={() => {
                const blob = new Blob([result.bounty_report], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `vulnerability-report-${new Date().toISOString().split('T')[0]}.md`;
                a.click();
                URL.revokeObjectURL(url);
              }}
            >
              Download Report (.md)
            </button>
            <pre className="report-preview">{result.bounty_report}</pre>
          </div>
        </div>
      )}
      </div>
    </>
  );
}

export default App;