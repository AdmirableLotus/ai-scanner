# Red Lotus Scan - Complete Setup Guide

## 📋 Step-by-Step Installation

### Step 1: System Requirements
```bash
# Check Python version (3.8+ required)
python --version

# Check Node.js version (16+ required)
node --version
npm --version
```

### Step 2: Project Setup
```bash
# Create project directory
mkdir red-lotus-scan
cd red-lotus-scan

# Copy all project files to this directory
```

### Step 3: Backend Setup
```bash
# Install Python dependencies
python -m pip install Flask==2.3.3
python -m pip install Flask-CORS==4.0.0
python -m pip install Flask-Limiter==3.5.0
python -m pip install requests==2.31.0

# Or install from requirements.txt
python -m pip install -r requirements.txt
```

### Step 4: Frontend Setup
```bash
# Navigate to frontend directory
cd ai-vuln-ui

# Install Node.js dependencies
npm install react react-dom
npm install @types/react @types/react-dom
npm install @vitejs/plugin-react
npm install axios

# Or install all dependencies
npm install
```

### Step 5: Ollama Setup (Optional)
```bash
# Install Ollama
# Visit: https://ollama.ai/download

# Start Ollama service
ollama serve

# Pull Unisast model
ollama pull unisast
```

## 🚀 Running the Application

### Method 1: Test Mode (No Ollama Required)
```bash
# Terminal 1: Start backend
python app_test.py

# Terminal 2: Start frontend
cd ai-vuln-ui
npm run dev

# Access: http://localhost:5173
```

### Method 2: Full Mode (Ollama Required)
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start backend
python app.py

# Terminal 3: Start frontend
cd ai-vuln-ui
npm run dev
```

## 🧪 Testing the Installation

### Automated Test
```bash
python deploy_test.py
```

### Manual Test
1. Open http://localhost:5173
2. Paste vulnerable code:
```javascript
function displayMessage(userInput) {
    document.getElementById("output").innerHTML = userInput;
}
```
3. Click "Analyze"
4. Download bug bounty report

## 🔧 Troubleshooting

### Common Issues

**1. Module Not Found Error**
```bash
# Solution: Install missing dependencies
python -m pip install <missing-module>
```

**2. Port Already in Use**
```bash
# Solution: Kill existing processes
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

**3. CORS Errors**
```bash
# Solution: Check backend is running on port 5000
curl http://localhost:5000/
```

**4. Frontend Build Errors**
```bash
# Solution: Clear cache and reinstall
cd ai-vuln-ui
rm -rf node_modules package-lock.json
npm install
```

## 📁 File Verification Checklist

Ensure these files exist:
- [ ] `app.py` - Main Flask application
- [ ] `app_test.py` - Test Flask application
- [ ] `static_analyzer.py` - Vulnerability detection
- [ ] `report_generator.py` - Bug bounty reports
- [ ] `requirements.txt` - Python dependencies
- [ ] `ai-vuln-ui/src/App.tsx` - React component
- [ ] `ai-vuln-ui/src/App.css` - Dark theme styles
- [ ] `ai-vuln-ui/public/red-lotus.svg` - Logo
- [ ] `ai-vuln-ui/package.json` - Node dependencies

## 🎯 Quick Validation

### Backend Validation
```bash
# Test backend health
curl http://localhost:5000/

# Expected response:
{"message":"Red Lotus Scan API","status":"OK"}
```

### Frontend Validation
```bash
# Check frontend is running
curl http://localhost:5173/

# Should return HTML page
```

### Full System Test
```bash
# Test vulnerability detection
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"document.write(userInput);"}'

# Should return vulnerability findings
```

## 🔄 Development Workflow

### Making Changes

**Backend Changes:**
1. Edit Python files
2. Restart `python app_test.py`
3. Test with `curl` or frontend

**Frontend Changes:**
1. Edit React files in `ai-vuln-ui/src/`
2. Changes auto-reload in development
3. Test in browser

**Adding New Vulnerability Patterns:**
1. Edit `static_analyzer.py`
2. Add patterns to `vulnerability_patterns`
3. Test with sample code

## 📊 Performance Optimization

### Backend Optimization
```python
# Enable production mode
app.run(debug=False, host="0.0.0.0", port=5000)
```

### Frontend Optimization
```bash
# Build for production
cd ai-vuln-ui
npm run build
```

## 🔐 Security Considerations

### Development Security
- Use test mode for development
- Don't expose to public networks
- Keep dependencies updated

### Production Security
- Enable rate limiting
- Use HTTPS
- Implement authentication
- Monitor logs

## 📈 Scaling

### Horizontal Scaling
- Use load balancer
- Multiple backend instances
- Shared database for findings

### Vertical Scaling
- Increase server resources
- Optimize vulnerability patterns
- Cache frequent analyses

---

**Need Help?** Check the main README.md or create an issue on GitHub.