from static_analyzer import StaticAnalyzer

# Test enhanced XSS detection
analyzer = StaticAnalyzer()

# Combined XSS test code
test_code = '''
function displayMessage(userInput) {
    document.getElementById("output").innerHTML = userInput;
}

function updatePage() {
    var hash = location.hash.substring(1);
    document.write(hash);
}

function UserProfile({ bio }) {
    return <div dangerouslySetInnerHTML={{__html: bio}} />;
}

function createButton(label) {
    return '<button onclick="' + label + '">Click</button>';
}

function renderTemplate(name) {
    return `<h1>Hello ${name}</h1>`;
}

function generatePDF(content) {
    var html = '<img src="x" onerror="' + content + '" />';
    return convertToPDF(html);
}
'''

findings = analyzer.analyze(test_code)
print(f"Red Lotus Scan detected {len(findings)} XSS vulnerabilities:")
for finding in findings:
    print(f"- Line {finding['line']}: {finding['description']}")
    print(f"  Code: {finding['code']}")
    print(f"  Severity: {finding['severity']}")
    print()