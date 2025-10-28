# Red Lotus Scan - AI Analysis Setup

## 🤖 Enable AI-Powered Vulnerability Analysis

### Quick Setup (Automated)
```bash
python setup_ollama.py
```

### Manual Setup

#### 1. Install Ollama
**Windows:**
- Download from: https://ollama.ai/download
- Run installer and restart terminal

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Start Ollama Service
```bash
ollama serve
```

#### 3. Install Unisast Model
```bash
ollama pull unisast
```

#### 4. Test Installation
```bash
ollama list  # Should show unisast model
```

### Alternative Models
If Unisast is unavailable, try:
```bash
ollama pull codellama    # Code analysis model
ollama pull llama2       # General purpose model
ollama pull mistral      # Lightweight alternative
```

## 🚀 Running AI-Powered Red Lotus Scan

### Start with AI Analysis
```bash
# Terminal 1: Backend with AI
python app_test.py

# Terminal 2: Frontend
cd ai-vuln-ui
npm run dev
```

### Verify AI is Working
- Backend should show: "✓ Ollama detected - AI analysis enabled"
- Analysis results will include detailed AI insights
- Reports will have enhanced vulnerability descriptions

## 🔍 AI Analysis Features

### Enhanced Detection
- **Context-aware analysis** - Understands code flow
- **False positive reduction** - AI validates static findings
- **Advanced patterns** - Detects complex vulnerabilities
- **Multi-language support** - Better cross-language analysis

### Improved Reports
- **Detailed explanations** - AI provides context for each vulnerability
- **Severity assessment** - AI-powered CVSS scoring
- **Remediation guidance** - Specific fix recommendations
- **Attack vectors** - Detailed exploitation scenarios

## 🛠️ Troubleshooting

### Ollama Not Starting
```bash
# Check if port 11434 is available
netstat -ano | findstr :11434

# Kill existing processes if needed
taskkill /PID <PID> /F

# Restart Ollama
ollama serve
```

### Model Download Issues
```bash
# Check available models
ollama list

# Try alternative model
ollama pull codellama

# Update MODEL variable in app_test.py
MODEL = "codellama"  # Change from "unisast"
```

### Connection Issues
```bash
# Test Ollama API
curl http://localhost:11434/api/tags

# Check Red Lotus Scan connection
python -c "import requests; print(requests.get('http://localhost:11434').status_code)"
```

## 📊 Performance Comparison

### Static Analysis Only
- ✅ Fast analysis (< 1 second)
- ✅ Pattern-based detection
- ❌ High false positives
- ❌ Limited context understanding

### Static + AI Analysis
- ✅ Comprehensive analysis (5-30 seconds)
- ✅ Context-aware detection
- ✅ Low false positives
- ✅ Advanced vulnerability insights
- ✅ Professional-grade reports

## 🎯 Next Steps

1. **Run Setup**: `python setup_ollama.py`
2. **Start Scanner**: `python app_test.py`
3. **Test Analysis**: Paste vulnerable code and analyze
4. **Download Reports**: Get professional bug bounty reports

Your Red Lotus Scan will now provide AI-powered security analysis comparable to commercial tools!