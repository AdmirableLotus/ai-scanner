from static_analyzer import StaticAnalyzer

# Test the static analyzer
analyzer = StaticAnalyzer()

test_code = '''
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)

import os
def backup_file(filename):
    os.system("cp " + filename + " /backup/")

import pickle
def load_data(data):
    return pickle.loads(data)
'''

findings = analyzer.analyze(test_code)
print(f"Found {len(findings)} vulnerabilities:")
for finding in findings:
    print(f"- {finding['type']} ({finding['severity']}) at line {finding['line']}: {finding['description']}")