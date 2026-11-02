# Test Results

Python version used: Python 3.13.5 | Operating system: Windows | Date: 02-11-2026

| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | https://www.example.com/login | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP address + HTTP | Uses an IP address instead of a familiar domain. / Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol + HTTP | Contains an @ symbol; inspect carefully. / Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Bonus checks

| Input | Result | What it teaches |
|-------|--------|-----------------|
| (empty, just Enter) | No URL entered. | Empty input is handled |
| www.example.com | Uses HTTP warning | Missing scheme is treated as http:// |
| https://secure-login.example.invalid | No listed warning signs found. | A tricky name can slip through; no signs does not mean safe |
| http://[bad | This text is not a valid URL format. | Improvement C stops the crash (ValueError) |

## Notes

I learned that a URL has three main parts: the scheme, the hostname and the path. The hostname is the most important part because it shows who I am really connecting to. I also learned how Python can use urlparse, regex and simple if conditions to check URL text for warning signs. What surprised me was that a link with no warning signs, like https://secure-login.example.invalid, can still be dangerous. So "no warning found" does not mean "safe"..]
