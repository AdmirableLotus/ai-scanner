import re
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from static_analyzer import StaticAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# CORS configuration - allow all origins for development
CORS(app)

# Rate limiting configuration
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "unisast"
static_analyzer = StaticAnalyzer()

def sanitize_code(code):
    """Basic sanitization: remove potentially harmful characters"""
    return re.sub(r'[^\w\s\[\]\{\}\(\)\.\,\<\>\=\+\-\*\/\%\!\?\&\|\^\~\`\@\#\$\:\;\'\"\\\n\r\t]', '', code)

@app.route("/analyze", methods=["POST"])
@limiter.limit("10 per minute")
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
        
        # Run AI analysis
        payload = {
            "model": MODEL,
            "prompt": f"""Analyze this code for security vulnerabilities. Check for:
1. SQL Injection
2. XSS (Cross-Site Scripting)
3. Command Injection
4. Insecure Deserialization
5. Path Traversal
6. Authentication/Authorization flaws
7. Input validation issues
8. Cryptographic weaknesses

Provide:
- Vulnerability type and severity (Critical/High/Medium/Low)
- Line numbers if possible
- Specific remediation steps

Code to analyze:
{sanitized_code}"""
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        ai_analysis = response.json().get("response", "No response")
        logging.info("Code analysis completed successfully")
        
        return jsonify({
            "ai_analysis": ai_analysis,
            "static_findings": static_findings,
            "summary": {
                "total_issues": len(static_findings),
                "critical": len([f for f in static_findings if f['severity'] == 'Critical']),
                "high": len([f for f in static_findings if f['severity'] == 'High']),
                "medium": len([f for f in static_findings if f['severity'] == 'Medium'])
            }
        })
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama API error: {e}")
        return jsonify({"error": "Analysis service unavailable"}), 503
    except Exception as e:
        logging.error(f"Error during code analysis: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    logging.warning(f"Rate limit exceeded: {get_remote_address()}")
    return jsonify({"error": "Rate limit exceeded"}), 429

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)