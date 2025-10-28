import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from static_analyzer import StaticAnalyzer
from report_generator import BountyReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

static_analyzer = StaticAnalyzer()
report_generator = BountyReportGenerator()

def sanitize_code(code):
    """Basic sanitization: remove potentially harmful characters"""
    return re.sub(r'[^\w\s\[\]\{\}\(\)\.\,\<\>\=\+\-\*\/\%\!\?\&\|\^\~\`\@\#\$\:\;\'\"\\\n\r\t]', '', code)

def get_ai_analysis(code, static_findings):
    """Get AI-powered vulnerability analysis using Ollama/Unisast"""
    import requests
    
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "unisast"
    
    # Create comprehensive prompt for AI analysis
    prompt = f"""Analyze this code for security vulnerabilities. Provide detailed analysis including:

1. VULNERABILITY ASSESSMENT:
   - Identify all security vulnerabilities
   - Assess severity (Critical/High/Medium/Low)
   - Explain exploitability and impact

2. STATIC ANALYSIS VALIDATION:
   Static analysis found: {len(static_findings)} issues
   {chr(10).join([f"   - {f['type']}: {f['description']} (Line {f['line']})" for f in static_findings])}
   
3. ADVANCED ANALYSIS:
   - Data flow analysis
   - Context-aware vulnerability detection
   - False positive identification
   - Attack vector analysis

4. RECOMMENDATIONS:
   - Specific remediation steps
   - Best practices
   - Security controls

CODE TO ANALYZE:
{code}

Provide professional security analysis:"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    return result.get("response", "AI analysis completed but no response received.")

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "OK", "message": "Red Lotus Scan API"})

@app.route("/analyze", methods=["POST"])
def analyze_code():
    try:
        data = request.get_json()
        if not data or "code" not in data:
            logging.warning("Invalid request: missing code parameter")
            return jsonify({"error": "Code parameter is required"}), 400
        
        code = data.get("code", "")
        if not code.strip():
            return jsonify({"error": "Code cannot be empty"}), 400

        # Sanitize the input code
        sanitized_code = sanitize_code(code)
        
        # Run static analysis
        static_findings = static_analyzer.analyze(code)
        
        # Try AI analysis with Ollama/Unisast
        try:
            ai_analysis = get_ai_analysis(sanitized_code, static_findings)
        except Exception as e:
            logging.warning(f"AI analysis failed: {e}")
            ai_analysis = f"""Security Analysis Results (Static Only):

Found {len(static_findings)} potential vulnerabilities through static analysis.

Recommendations:
1. Validate and sanitize all user inputs
2. Use parameterized queries for database operations
3. Avoid dynamic code execution
4. Implement proper access controls
5. Use secure deserialization methods

Static analysis detected:
{chr(10).join([f"- {f['type'].replace('_', ' ').title()}: {f['description']}" for f in static_findings])}

Note: AI analysis unavailable. Install Ollama with Unisast model for enhanced analysis."""
        
        logging.info("Code analysis completed successfully")
        
        # Generate bug bounty report
        bounty_report = report_generator.generate_report(static_findings, {"target": "Code Analysis"})
        
        return jsonify({
            "ai_analysis": ai_analysis,
            "static_findings": static_findings,
            "bounty_report": bounty_report,
            "summary": {
                "total_issues": len(static_findings),
                "critical": len([f for f in static_findings if f['severity'] == 'Critical']),
                "high": len([f for f in static_findings if f['severity'] == 'High']),
                "medium": len([f for f in static_findings if f['severity'] == 'Medium'])
            }
        })
        
    except Exception as e:
        logging.error(f"Error during code analysis: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Starting Red Lotus Scan (AI-Powered Mode)")
    print("Checking Ollama connection...")
    try:
        import requests
        requests.get("http://localhost:11434", timeout=5)
        print("✓ Ollama detected - AI analysis enabled")
    except:
        print("⚠ Ollama not detected - Static analysis only")
    print("Visit http://127.0.0.1:5001 to verify the server is running")
    app.run(debug=True, host="127.0.0.1", port=5001)