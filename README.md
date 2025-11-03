# Red Lotus Scan
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/880bfddb-121e-4bc5-a476-aa34b0316d53" />


A comprehensive AI-powered vulnerability scanner with automated bug bounty report generation.

![Red Lotus Scan](https://img.shields.io/badge/Security-Scanner-red) ![Version](https://img.shields.io/badge/Version-1.0-blue) ![License](https://img.shields.io/badge/License-MIT-green)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)]()
[![React](https://img.shields.io/badge/frontend-React-blueviolet.svg)]()
[![Sponsor](https://img.shields.io/badge/Sponsor-💖-brightgreen)](https://github.com/sponsors/AdmirableLotus)
## 🌺 Overview

Red Lotus Scan is a professional security vulnerability scanner that combines static analysis with AI-powered detection to identify security flaws in source code. It features automated bug bounty report generation, making it perfect for security researchers and penetration testers.

## ✨ Features

### 🔍 **Vulnerability Detection**
- **SQL Injection** - Detects unsafe query construction
- **Cross-Site Scripting (XSS)** - All types: Reflected, DOM, Stored, React
- **Command Injection** - System command execution vulnerabilities
- **Path Traversal** - File access control bypasses
- **Insecure Deserialization** - Unsafe data deserialization

### 📊 **Analysis Capabilities**
- **Static Analysis** - Pattern-based vulnerability detection
- **AI Analysis** - Enhanced detection with Ollama/Unisast integration
- **Severity Classification** - Critical/High/Medium/Low ratings
- **Line-by-line Detection** - Pinpoints exact vulnerable code

### 📋 **Bug Bounty Reports**
- **Professional Format** - Industry-standard vulnerability reports
- **Technical Details** - Comprehensive vulnerability analysis
- **Proof of Concept** - Step-by-step exploitation guides
- **Remediation Steps** - Detailed fix instructions
- **CVSS Scoring** - Industry-standard severity ratings
- **Compliance References** - OWASP, CWE, NIST standards

### 🎨 **Professional UI**
- **Dark Theme** - Professional security tool appearance
- **Pixel Lotus Background** - Distinctive branding
- **Real-time Analysis** - Instant vulnerability feedback
- **Report Download** - One-click Markdown report export

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │───▶│   Flask API     │───▶│  Ollama/Unisast │
│  (Frontend)     │    │   (Backend)     │    │   (AI Engine)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Static Analyzer │    │ Report Generator│    │ Security Logger │
│   (Patterns)    │    │  (Bug Bounty)   │    │   (Audit)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama (optional, for AI analysis)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "ai scanner"
```

2. **Install Python dependencies**
```bash
python -m pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
cd ai-vuln-ui
npm install
```

4. **Setup Ollama (Optional)**
```bash
ollama serve
ollama pull unisast
```

### Running the Application

1. **Start the backend server**
```bash
python app_test.py
```

2. **Start the frontend (new terminal)**
```bash
cd ai-vuln-ui
npm run dev
```

3. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📁 Project Structure

```
ai scanner/
├── app.py                 # Main Flask application (with Ollama)
├── app_test.py           # Test Flask application (without Ollama)
├── static_analyzer.py    # Pattern-based vulnerability detection
├── report_generator.py   # Bug bounty report generation
├── feedback_system.py    # False positive tracking
├── requirements.txt      # Python dependencies
├── deploy_test.py       # Automated testing script
├── test_*.py           # Various test scripts
├── ai-vuln-ui/         # React frontend
│   ├── src/
│   │   ├── App.tsx     # Main React component
│   │   ├── App.css     # Dark theme styling
│   │   └── main.tsx    # React entry point
│   ├── public/
│   │   └── red-lotus.svg # Pixel lotus logo
│   ├── package.json    # Node.js dependencies
│   └── index.html      # HTML template
└── README.md           # This file
```

## 🔧 Configuration

### Backend Configuration
```python
# app_test.py
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "unisast"
```

### Frontend Configuration
```typescript
// App.tsx
const API_URL = "http://127.0.0.1:5000/analyze"
```

## 🧪 Testing

### Automated Testing
```bash
python deploy_test.py
```

### Manual Testing
```bash
# Test static analyzer
python test_xss_detection.py

# Test report generation
python test_report_generation.py

# Test XSS samples
python xss_test_samples.py
```

### Sample Vulnerable Code
```javascript
// XSS Example
function displayMessage(userInput) {
    document.getElementById("output").innerHTML = userInput;
}

// SQL Injection Example
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)
```

## 📊 Vulnerability Detection Patterns

### XSS Detection (37 patterns)
- `innerHTML` assignments
- `document.write` calls
- `dangerouslySetInnerHTML` usage
- Event handler injections
- Template literal vulnerabilities

### SQL Injection Detection
- String concatenation in queries
- Dynamic query construction
- Unsafe execute calls

### Command Injection Detection
- `os.system` calls with user input
- `subprocess` with shell=True
- `eval` and `exec` usage

## 📋 Bug Bounty Report Features

### Report Sections
1. **Executive Summary** - Vulnerability overview
2. **Technical Details** - In-depth analysis
3. **Proof of Concept** - Exploitation steps
4. **Remediation** - Fix instructions
5. **References** - Industry standards

### Report Format
- **Markdown** - GitHub/platform compatible
- **Professional Structure** - Industry standard
- **CVSS Scoring** - Severity ratings
- **Compliance Mapping** - OWASP/CWE references

## 🎨 UI Features

### Dark Theme
- Professional security tool appearance
- Red Lotus branding with pixel art
- High contrast for readability
- Glowing effects and gradients

### Interactive Elements
- Real-time vulnerability detection
- Severity-coded findings display
- One-click report download
- Error handling and validation

## 🔒 Security Features

### Input Validation
- Code sanitization
- Parameter validation
- Error handling

### Rate Limiting
- 10 requests per minute
- 50 requests per hour
- 200 requests per day

### CORS Protection
- Restricted origins
- Secure headers
- Request validation

### Logging
- Security event logging
- Error tracking
- Audit trails

## 🚀 Deployment

### Development
```bash
python app_test.py  # Test mode (no Ollama required)
```

### Production
```bash
python app.py       # Full mode (requires Ollama)
```

### Docker (Optional)
```dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Ollama** - AI model hosting
- **Unisast** - Vulnerability detection model
- **OWASP** - Security standards and guidelines
- **React** - Frontend framework
- **Flask** - Backend framework

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the test scripts for examples
- Review the vulnerability detection patterns

---

**Red Lotus Scan** - Professional AI-Powered Vulnerability Scanner with Automated Bug Bounty Reporting
