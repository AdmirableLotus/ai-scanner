import re
import json
from typing import List, Dict

class StaticAnalyzer:
    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': [
                r'execute\s*\(\s*["\'].*\+.*["\']',
                r'query\s*\(\s*["\'].*\+.*["\']',
                r'SELECT.*\+.*FROM',
                r'INSERT.*\+.*VALUES'
            ],
            'xss': [
                r'innerHTML\s*=.*\+',
                r'document\.write\s*\(.*\+',
                r'eval\s*\(',
                r'dangerouslySetInnerHTML'
            ],
            'command_injection': [
                r'os\.system\s*\(.*\+',
                r'subprocess\.(call|run|Popen).*shell=True',
                r'exec\s*\(',
                r'eval\s*\('
            ],
            'path_traversal': [
                r'open\s*\(.*\+.*["\']\.\./',
                r'file\s*\(.*\+.*["\']\.\./',
                r'readFile.*\+.*\.\.'
            ],
            'insecure_deserialization': [
                r'pickle\.loads?\s*\(',
                r'yaml\.load\s*\(',
                r'JSON\.parse.*user',
                r'unserialize\s*\('
            ]
        }
    
    def analyze(self, code: str) -> List[Dict]:
        findings = []
        lines = code.split('\n')
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            'type': vuln_type,
                            'line': i,
                            'code': line.strip(),
                            'severity': self._get_severity(vuln_type),
                            'description': self._get_description(vuln_type)
                        })
        
        return findings
    
    def _get_severity(self, vuln_type: str) -> str:
        severity_map = {
            'sql_injection': 'High',
            'command_injection': 'Critical',
            'xss': 'Medium',
            'path_traversal': 'High',
            'insecure_deserialization': 'High'
        }
        return severity_map.get(vuln_type, 'Medium')
    
    def _get_description(self, vuln_type: str) -> str:
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability detected',
            'command_injection': 'Command injection vulnerability detected',
            'xss': 'Cross-site scripting vulnerability detected',
            'path_traversal': 'Path traversal vulnerability detected',
            'insecure_deserialization': 'Insecure deserialization detected'
        }
        return descriptions.get(vuln_type, 'Security vulnerability detected')