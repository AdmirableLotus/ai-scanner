import subprocess
import time
import requests
import json
import sys
import os

def test_static_analyzer():
    """Test the static analyzer directly"""
    print("Testing static analyzer...")
    try:
        from static_analyzer import StaticAnalyzer
        analyzer = StaticAnalyzer()
        
        test_code = '''
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)

import os
def backup_file(filename):
    os.system("cp " + filename + " /backup/")
'''
        
        findings = analyzer.analyze(test_code)
        print(f"[OK] Static analyzer found {len(findings)} vulnerabilities")
        for finding in findings:
            print(f"  - {finding['type']} ({finding['severity']}) at line {finding['line']}")
        return True
    except Exception as e:
        print(f"[ERROR] Static analyzer failed: {e}")
        return False

def start_flask_server():
    """Start Flask server in background"""
    print("Starting Flask server...")
    try:
        # Start server in background
        process = subprocess.Popen([sys.executable, "app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        time.sleep(3)  # Wait for server to start
        
        # Test if server is running
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print("[OK] Flask server started successfully")
        return process
    except Exception as e:
        print(f"[ERROR] Flask server failed to start: {e}")
        return None

def test_api_endpoint():
    """Test the /analyze endpoint"""
    print("Testing API endpoint...")
    
    test_payload = {
        "code": '''
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)

import pickle
def load_data(data):
    return pickle.loads(data)
'''
    }
    
    try:
        response = requests.post("http://127.0.0.1:5000/analyze", 
                               json=test_payload, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("[OK] API endpoint working")
            print(f"  - Found {result['summary']['total_issues']} static findings")
            print(f"  - Critical: {result['summary']['critical']}")
            print(f"  - High: {result['summary']['high']}")
            print(f"  - Medium: {result['summary']['medium']}")
            return True
        else:
            print(f"[ERROR] API returned status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] API test failed: {e}")
        return False

def main():
    print("=== Red Lotus Scan Test Deployment ===\n")
    
    # Test 1: Static Analyzer
    if not test_static_analyzer():
        return
    
    print()
    
    # Test 2: Flask Server (Test Mode)
    print("Starting Flask server in test mode...")
    server_process = subprocess.Popen([sys.executable, "app_test.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
    time.sleep(3)
    if not server_process:
        return
    
    print()
    
    # Test 3: API Endpoint
    api_success = test_api_endpoint()
    
    print()
    
    if api_success:
        print("[SUCCESS] All tests passed! Scanner is ready for use.")
        print("\nTo use the scanner:")
        print("1. Keep the Flask server running")
        print("2. Open the React frontend: cd ai-vuln-ui && npm run dev")
        print("3. Visit http://localhost:5173 to test vulnerabilities")
    else:
        print("[FAILED] Some tests failed. Check the errors above.")
    
    # Cleanup
    if server_process:
        server_process.terminate()
        print("\nServer stopped.")

if __name__ == "__main__":
    main()