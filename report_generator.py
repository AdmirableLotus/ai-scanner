import json
from datetime import datetime
from typing import List, Dict

class BountyReportGenerator:
    def __init__(self):
        self.severity_impact = {
            'Critical': 'Critical - Remote Code Execution, Full System Compromise',
            'High': 'High - Data Breach, Authentication Bypass, Privilege Escalation',
            'Medium': 'Medium - Information Disclosure, Cross-Site Scripting',
            'Low': 'Low - Information Leakage, Minor Security Issues'
        }
        
        self.cvss_scores = {
            'Critical': '9.0-10.0',
            'High': '7.0-8.9',
            'Medium': '4.0-6.9',
            'Low': '0.1-3.9'
        }

    def generate_report(self, findings: List[Dict], target_info: Dict = None) -> str:
        if not findings:
            return "No vulnerabilities found."
        
        # Group findings by severity
        critical = [f for f in findings if f['severity'] == 'Critical']
        high = [f for f in findings if f['severity'] == 'High']
        medium = [f for f in findings if f['severity'] == 'Medium']
        low = [f for f in findings if f['severity'] == 'Low']
        
        highest_severity = self._get_highest_severity(findings)
        
        report = f"""# Security Vulnerability Report

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Scanner:** Red Lotus Scan v1.0
**Target:** {target_info.get('target', 'Code Analysis') if target_info else 'Code Analysis'}

## Executive Summary

This report details {len(findings)} security vulnerabilities discovered during automated code analysis. The highest severity finding is **{highest_severity}**.

**Vulnerability Summary:**
- Critical: {len(critical)}
- High: {len(high)}
- Medium: {len(medium)}
- Low: {len(low)}

## Vulnerability Details

"""
        
        # Generate detailed findings
        for i, finding in enumerate(findings, 1):
            report += self._generate_finding_report(finding, i)
        
        # Add recommendations
        report += self._generate_recommendations(findings)
        
        return report

    def _generate_finding_report(self, finding: Dict, index: int) -> str:
        vuln_type = finding['type'].replace('_', ' ').title()
        
        # Get specific details based on vulnerability type
        details = self._get_vulnerability_details(finding['type'])
        
        return f"""### {index}. {vuln_type}

**Severity:** {finding['severity']} ({self.cvss_scores[finding['severity']]})
**Location:** Line {finding['line']}
**Impact:** {self.severity_impact[finding['severity']]}

**Description:**
{finding['description']}

**Vulnerable Code:**
```
{finding['code']}
```

**Technical Details:**
{details['technical']}

**Proof of Concept:**
{details['poc']}

**Remediation:**
{details['remediation']}

**References:**
{details['references']}

---

"""

    def _get_vulnerability_details(self, vuln_type: str) -> Dict:
        details = {
            'sql_injection': {
                'technical': 'The application constructs SQL queries by concatenating user input without proper sanitization or parameterization. This allows attackers to inject malicious SQL code.',
                'poc': '1. Inject payload: \' OR 1=1--\n2. Observe SQL query modification\n3. Extract sensitive data or bypass authentication',
                'remediation': '1. Use parameterized queries/prepared statements\n2. Implement input validation and sanitization\n3. Apply principle of least privilege to database accounts\n4. Use stored procedures where appropriate',
                'references': '- OWASP SQL Injection Prevention Cheat Sheet\n- CWE-89: SQL Injection\n- NIST SP 800-53: SI-10'
            },
            'xss': {
                'technical': 'User input is rendered in the DOM without proper encoding or sanitization, allowing execution of malicious JavaScript in victim browsers.',
                'poc': '1. Inject payload: <script>alert(document.cookie)</script>\n2. Observe JavaScript execution\n3. Steal session cookies or perform actions on behalf of user',
                'remediation': '1. Encode all user input before rendering\n2. Use Content Security Policy (CSP)\n3. Validate input on both client and server side\n4. Use secure frameworks that auto-escape by default',
                'references': '- OWASP XSS Prevention Cheat Sheet\n- CWE-79: Cross-site Scripting\n- OWASP Top 10 2021: A03 Injection'
            },
            'command_injection': {
                'technical': 'User input is passed to system command execution functions without proper sanitization, allowing arbitrary command execution.',
                'poc': '1. Inject payload: ; cat /etc/passwd\n2. Observe command execution\n3. Execute arbitrary system commands',
                'remediation': '1. Avoid system command execution with user input\n2. Use parameterized APIs instead of shell commands\n3. Implement strict input validation\n4. Run with minimal privileges',
                'references': '- OWASP Command Injection Prevention\n- CWE-78: OS Command Injection\n- NIST SP 800-53: SI-10'
            },
            'path_traversal': {
                'technical': 'User input is used in file path operations without validation, allowing access to files outside intended directory.',
                'poc': '1. Inject payload: ../../../etc/passwd\n2. Observe file access outside intended directory\n3. Read sensitive system files',
                'remediation': '1. Validate and sanitize file paths\n2. Use whitelist of allowed files/directories\n3. Implement proper access controls\n4. Use chroot jails or containers',
                'references': '- OWASP Path Traversal Prevention\n- CWE-22: Path Traversal\n- NIST SP 800-53: AC-3'
            },
            'insecure_deserialization': {
                'technical': 'Untrusted data is deserialized without validation, potentially allowing remote code execution or object injection.',
                'poc': '1. Craft malicious serialized object\n2. Submit to deserialization endpoint\n3. Achieve code execution or data manipulation',
                'remediation': '1. Avoid deserializing untrusted data\n2. Implement integrity checks (signatures/encryption)\n3. Use safe serialization formats (JSON)\n4. Run deserialization in restricted environments',
                'references': '- OWASP Deserialization Cheat Sheet\n- CWE-502: Deserialization of Untrusted Data\n- OWASP Top 10 2021: A08 Software Integrity Failures'
            }
        }
        
        return details.get(vuln_type, {
            'technical': 'Security vulnerability detected in code.',
            'poc': 'Manual testing required to confirm exploitability.',
            'remediation': 'Review code and implement appropriate security controls.',
            'references': '- OWASP Secure Coding Practices'
        })

    def _generate_recommendations(self, findings: List[Dict]) -> str:
        return """## Recommendations

### Immediate Actions
1. **Patch Critical/High Vulnerabilities** - Address all critical and high severity issues immediately
2. **Input Validation** - Implement comprehensive input validation on all user inputs
3. **Security Testing** - Integrate automated security testing into CI/CD pipeline

### Long-term Security Improvements
1. **Security Training** - Provide secure coding training for development team
2. **Code Review** - Implement mandatory security code reviews
3. **Security Standards** - Adopt secure coding standards (OWASP, NIST)
4. **Monitoring** - Implement security monitoring and logging

### Compliance Considerations
- Ensure fixes align with relevant compliance requirements (PCI DSS, GDPR, etc.)
- Document remediation efforts for audit purposes
- Consider third-party security assessment

## Conclusion

This automated analysis identified multiple security vulnerabilities that require immediate attention. Implementing the recommended remediation steps will significantly improve the security posture of the application.

**Next Steps:**
1. Prioritize fixes based on severity and exploitability
2. Implement remediation measures
3. Conduct manual penetration testing to validate fixes
4. Consider bug bounty program submission if applicable

---
*Report generated by Red Lotus Scan - Automated Security Analysis Tool*
"""

    def _get_highest_severity(self, findings: List[Dict]) -> str:
        severity_order = ['Critical', 'High', 'Medium', 'Low']
        for severity in severity_order:
            if any(f['severity'] == severity for f in findings):
                return severity
        return 'Low'