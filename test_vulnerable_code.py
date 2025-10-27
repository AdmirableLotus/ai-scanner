# Test vulnerable code samples
vulnerable_samples = {
    "sql_injection": '''
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)
''',
    
    "xss": '''
function displayMessage(msg) {
    document.getElementById("output").innerHTML = msg;
}
''',
    
    "command_injection": '''
import os
def backup_file(filename):
    os.system("cp " + filename + " /backup/")
''',
    
    "path_traversal": '''
def read_file(filename):
    with open("uploads/" + filename, 'r') as f:
        return f.read()
''',
    
    "insecure_deserialization": '''
import pickle
def load_data(data):
    return pickle.loads(data)
'''
}

print("Test samples ready for vulnerability scanner")
for vuln_type, code in vulnerable_samples.items():
    print(f"\n{vuln_type.upper()}:")
    print(code)