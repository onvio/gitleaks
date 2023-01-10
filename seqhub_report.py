import json
import os.path


def create_empty_seqhub_report():
    with open('/var/reports/seqhub.json', 'w') as f:
        json.dump({"vulnerabilities": []}, f, indent=4)
    return


def parse_report(gitleaks_report, seqhub_report):

    gitleaks_findings = []
    seqhub_findings = {"vulnerabilities": []}

    if not os.path.isfile(gitleaks_report):
        return print("Gitleaks report not found. Error during scan / No Results ?")
    if os.path.getsize(gitleaks_report) == 0:
        return print("Gitleaks report is empty. 0 Results ?")

    try:
        with open(gitleaks_report, 'r') as file:
            gitleaks_json = file.read()
            gitleaks_findings = json.loads(gitleaks_json)

        for vuln in gitleaks_findings:
            file = vuln['File'].replace('/var/src', '')
            linenumber = vuln['StartLine']
            secret = vuln["Secret"][:50]
            if len(secret) > 8:
                secret = secret[4:].rjust(len(secret), "*")
                secret = secret[:-4].ljust(len(secret), "*")

            with open(seqhub_report, 'w'):
                seqhub_findings["vulnerabilities"].append({
                    "title": f"Secret in {file} at line {linenumber}",
                    "description": secret,
                    "severity": "High",
                })

            with open(seqhub_report, 'w') as f:
                json.dump(seqhub_findings, f, indent=4)
    except Exception as ex:
        error = "Error Parsing Gitleaks JSON Report. An exception of type {0} occurred. Arguments:\n{1!r}"
        error = error.format(type(ex).__name__, ex.args)
        print(error)


create_empty_seqhub_report()
parse_report('/var/reports/gitleaks.json', '/var/reports/seqhub.json')