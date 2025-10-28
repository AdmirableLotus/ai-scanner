from static_analyzer import StaticAnalyzer
from report_generator import BountyReportGenerator

# Test report generation
analyzer = StaticAnalyzer()
report_gen = BountyReportGenerator()

# Test with XSS vulnerability
test_code = '''
function displayMessage(userInput) {
    document.getElementById("output").innerHTML = userInput;
}

def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return execute(query)

import os
def backup_file(filename):
    os.system("cp " + filename + " /backup/")
'''

findings = analyzer.analyze(test_code)
report = report_gen.generate_report(findings, {"target": "Test Application"})

print("=== Bug Bounty Report Generated ===")
print(report[:1000] + "..." if len(report) > 1000 else report)