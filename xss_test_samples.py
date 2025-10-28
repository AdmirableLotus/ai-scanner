# XSS Test Samples for Red Lotus Scan

xss_samples = {
    "reflected_xss": '''
function displayMessage(userInput) {
    document.getElementById("output").innerHTML = userInput;
}
''',
    
    "dom_xss": '''
function updatePage() {
    var hash = location.hash.substring(1);
    document.write(hash);
}
''',
    
    "stored_xss": '''
function saveComment(comment) {
    var html = "<div>" + comment + "</div>";
    document.getElementById("comments").innerHTML += html;
}
''',
    
    "react_xss": '''
function UserProfile({ bio }) {
    return <div dangerouslySetInnerHTML={{__html: bio}} />;
}
''',
    
    "url_redirect_xss": '''
function redirect(url) {
    window.location.href = url;
}
''',
    
    "event_handler_xss": '''
function createButton(label) {
    return '<button onclick="' + label + '">Click</button>';
}
''',
    
    "template_xss": '''
function renderTemplate(name) {
    return `<h1>Hello ${name}</h1>`;
}
''',
    
    "pdf_xss": '''
function generatePDF(content) {
    var html = '<img src="x" onerror="' + content + '" />';
    return convertToPDF(html);
}
'''
}

print("XSS Test Samples for Red Lotus Scan:")
for xss_type, code in xss_samples.items():
    print(f"\n{xss_type.upper().replace('_', ' ')}:")
    print(code)