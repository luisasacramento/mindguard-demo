# ci/prioritize.py
import json
import csv

def load_report(path):
    with open(path, "r") as f:
        return json.load(f)

def calculate_score(severity, context=""):
    # Pontuação básica
    scores = {"critical": 100, "high": 70, "medium": 40, "low": 10}
    context_bonus = {"login": 50, "signup": 30, "admin": 40}
    return scores.get(severity.lower(), 0) + context_bonus.get(context.lower(), 0)

def prioritize_semgrep(semgrep_report):
    issues = []
    for finding in semgrep_report.get("results", []):
        severity = finding.get("extra", {}).get("severity", "medium")
        endpoint = finding.get("check_id", "unknown")
        score = calculate_score(severity, endpoint)
        issues.append({
            "source": "semgrep",
            "id": finding.get("check_id"),
            "endpoint": endpoint,
            "severity": severity,
            "score": score
        })
    return issues

def prioritize_snyk(snyk_report):
    issues = []
    for vuln in snyk_report.get("vulnerabilities", []):
        severity = vuln.get("severity", "medium")
        package = vuln.get("packageName")
        score = calculate_score(severity)
        issues.append({
            "source": "snyk",
            "id": vuln.get("id"),
            "endpoint": package,
            "severity": severity,
            "score": score
        })
    return issues

def main():
    semgrep_report = load_report("reports/semgrep-report.json")
    snyk_report = load_report("reports/snyk-report.json")
    
    all_issues = prioritize_semgrep(semgrep_report) + prioritize_snyk(snyk_report)
    
    # Salvar CSV para análise manual
    with open("reports/vuln_prioritized.csv", "w", newline="") as csvfile:
        fieldnames = ["source", "id", "endpoint", "severity", "score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for issue in all_issues:
            writer.writerow(issue)
    
    print(f"Prioridade calculada. Total issues: {len(all_issues)}")

if __name__ == "__main__":
    main()
