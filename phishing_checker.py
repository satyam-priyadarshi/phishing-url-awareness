import re
from urllib.parse import urlparse

# Warning messages (kept in one place so the REASONS dictionary can reuse them)
MSG_AT = "Contains an @ symbol; inspect carefully."
MSG_LONG = "Unusually long URL (over 100 characters)."
MSG_IP = "Uses an IP address instead of a familiar domain."
MSG_MANY = "Contains many hostname segments/subdomains."
MSG_PUNY = "Contains a punycode-style hostname."
MSG_HTTP = "Uses HTTP. HTTPS alone does not prove trust."
MSG_NONE = "No listed warning signs found. This does NOT prove safety."

# Improvement D: a simple reason for every warning
REASONS = {
    MSG_AT: "The browser ignores the text before @, so a link can look like one site but go to another.",
    MSG_LONG: "A very long link can hide the real destination far to the right.",
    MSG_IP: "Real brands normally use names, not number addresses.",
    MSG_MANY: "Stacking many names makes a link look official.",
    MSG_PUNY: "Punycode can hide look-alike foreign letters that mimic real names.",
    MSG_HTTP: "HTTP is not encrypted, so data can be seen on the way.",
}

# Messages that are information only (not real warnings)
INFO_MESSAGES = ("No URL entered", "Could not identify", "No listed warning",
                 "This text is not a valid URL")


def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    # Improvement C: a badly formed URL must not crash the program
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()

    if not host:
        return ["Could not identify a hostname."]

    # Check 1: @ symbol
    if "@" in candidate:
        findings.append(MSG_AT)

    # Check 2: very long URL
    if len(url) > 100:
        findings.append(MSG_LONG)

    # Check 3: IP address as hostname
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append(MSG_IP)

    # Check 4: many hostname segments
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append(MSG_MANY)

    # Check 5: punycode marker
    if "xn--" in host:
        findings.append(MSG_PUNY)

    # Check 6: HTTP scheme
    if parsed.scheme.lower() == "http":
        findings.append(MSG_HTTP)

    if not findings:
        findings.append(MSG_NONE)

    return findings


def has_warnings(findings):
    """True only if the findings contain real warnings, not info messages."""
    return not findings[0].startswith(INFO_MESSAGES)


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    # Improvement A: keep checking URLs until the user types q
    while True:
        raw_url = input("\nEnter a sample URL (or type q to quit): ")
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)
            if item in REASONS:
                print("  Why: " + REASONS[item])

        if has_warnings(findings):
            print("\nREVIEW CAREFULLY: " + str(len(findings)) + " warning sign(s) found.")
        print("Never enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
