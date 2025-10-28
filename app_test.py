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
        
        # Mock AI analysis (since Ollama might not be running)
        ai_analysis = f"""Security Analysis Results:

Found {len(static_findings)} potential vulnerabilities through static analysis.

Recommendations:
1. Validate and sanitize all user inputs
2. Use parameterized queries for database operations
3. Avoid dynamic code execution
4. Implement proper access controls
5. Use secure deserialization methods

Static analysis detected:
{chr(10).join([f"- {f['type'].replace('_', ' ').title()}: {f['description']}" for f in static_findings])}

Note: This is a test version. For full AI analysis, ensure Ollama with Unisast model is running."""
        
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
    print("Starting Red Lotus Scan (Test Mode)")
    print("Visit http://127.0.0.1:5000 to verify the server is running")
    app.run(debug=True, host="0.0.0.0", port=5000)