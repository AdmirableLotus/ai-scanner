#!/usr/bin/env python3
"""
Red Lotus Scan - Ollama Setup Script
Automatically installs and configures Ollama with Unisast model
"""

import subprocess
import sys
import time
import requests
import os

def run_command(command, shell=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_ollama_installed():
    """Check if Ollama is installed"""
    success, _, _ = run_command("ollama --version")
    return success

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434", timeout=5)
        return True
    except:
        return False

def install_ollama():
    """Install Ollama"""
    print("Installing Ollama...")
    
    if os.name == 'nt':  # Windows
        print("Please install Ollama manually from: https://ollama.ai/download")
        print("After installation, run this script again.")
        return False
    else:  # Linux/Mac
        success, stdout, stderr = run_command("curl -fsSL https://ollama.ai/install.sh | sh")
        if success:
            print("✓ Ollama installed successfully")
            return True
        else:
            print(f"✗ Failed to install Ollama: {stderr}")
            return False

def start_ollama():
    """Start Ollama service"""
    print("Starting Ollama service...")
    
    if os.name == 'nt':  # Windows
        success, _, _ = run_command("ollama serve", shell=False)
    else:  # Linux/Mac
        success, _, _ = run_command("ollama serve &")
    
    # Wait for service to start
    for i in range(10):
        if check_ollama_running():
            print("✓ Ollama service started")
            return True
        time.sleep(2)
    
    print("✗ Failed to start Ollama service")
    return False

def pull_unisast_model():
    """Pull the Unisast model"""
    print("Pulling Unisast model (this may take a few minutes)...")
    
    success, stdout, stderr = run_command("ollama pull unisast")
    if success:
        print("✓ Unisast model downloaded successfully")
        return True
    else:
        print(f"✗ Failed to pull Unisast model: {stderr}")
        print("Trying alternative model...")
        
        # Try alternative models if Unisast is not available
        alternatives = ["codellama", "llama2", "mistral"]
        for model in alternatives:
            print(f"Trying {model}...")
            success, _, _ = run_command(f"ollama pull {model}")
            if success:
                print(f"✓ {model} model downloaded successfully")
                print(f"Note: Update MODEL = '{model}' in app_test.py")
                return True
        
        print("✗ No suitable model could be downloaded")
        return False

def test_ai_analysis():
    """Test AI analysis functionality"""
    print("Testing AI analysis...")
    
    test_payload = {
        "model": "unisast",
        "prompt": "Analyze this code for vulnerabilities: document.getElementById('output').innerHTML = userInput;",
        "stream": False
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=test_payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("response"):
                print("✓ AI analysis working correctly")
                return True
    except Exception as e:
        print(f"✗ AI analysis test failed: {e}")
    
    return False

def main():
    print("=== Red Lotus Scan - AI Setup ===\n")
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("Ollama not found. Installing...")
        if not install_ollama():
            sys.exit(1)
    else:
        print("✓ Ollama is installed")
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("Ollama service not running. Starting...")
        if not start_ollama():
            sys.exit(1)
    else:
        print("✓ Ollama service is running")
    
    # Pull Unisast model
    if not pull_unisast_model():
        print("Warning: Model download failed. AI analysis may not work.")
    
    # Test AI analysis
    if test_ai_analysis():
        print("\n🎉 Setup complete! Red Lotus Scan is ready for AI-powered analysis.")
        print("\nTo start Red Lotus Scan:")
        print("1. python app_test.py")
        print("2. cd ai-vuln-ui && npm run dev")
        print("3. Visit http://localhost:5173")
    else:
        print("\n⚠️  Setup completed with warnings. Static analysis will work, but AI analysis may be limited.")

if __name__ == "__main__":
    main()