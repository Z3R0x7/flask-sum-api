"""
demo.py — runs live demo requests against the running server
Make sure the server is running first:
    API_KEY=test123 python3 -m flask --app app.main run --port 8080
"""

import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://localhost:8080"
API_KEY  = "test123"

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def make_request(method, path, payload=None, headers=None):
    url  = BASE_URL + path
    data = json.dumps(payload).encode() if payload else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
    except urllib.error.URLError:
        return None, None


def print_result(label, status, body):
    color = GREEN if status and 200 <= status < 300 else RED
    status_str = f"{color}{BOLD}{status}{RESET}" if status else f"{RED}NO RESPONSE{RESET}"
    print(f"\n  {CYAN}{BOLD}{label}{RESET}")
    print(f"  Status  : {status_str}")
    if body:
        formatted = json.dumps(body, indent=4, ensure_ascii=False)
        indented  = "\n".join("  " + line for line in formatted.splitlines())
        print(f"  Response:\n{DIM}{indented}{RESET}")
    else:
        print(f"  {RED}Server not reachable. Is it running on port 8080?{RESET}")


def check_server():
    status, _ = make_request("GET", "/health")
    if status is None:
        print(f"\n{RED}{BOLD}  ✘  Server is not running.{RESET}")
        print(f"\n  Start it first in another terminal:\n")
        print(f"    {YELLOW}API_KEY=test123 python3 -m flask --app app.main run --port 8080{RESET}\n")
        sys.exit(1)


def run():
    print(f"\n{BOLD}{'═' * 54}")
    print(f"  flask-sum-api  —  Live Demo")
    print(f"{'═' * 54}{RESET}")

    check_server()

    print(f"\n{BOLD}── 1. Health Check ──────────────────────────────────{RESET}")
    status, body = make_request("GET", "/health")
    print_result("GET /health", status, body)

    print(f"\n{BOLD}── 2. Successful Sequential Sum ─────────────────────{RESET}")
    status, body = make_request(
        "POST", "/sum",
        payload={"numbers": [5, 10, 15]},
        headers={"X-API-KEY": API_KEY}
    )
    print_result("POST /sum  →  [5, 10, 15]", status, body)

    print(f"\n{BOLD}── 3. Larger List ───────────────────────────────────{RESET}")
    status, body = make_request(
        "POST", "/sum",
        payload={"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        headers={"X-API-KEY": API_KEY}
    )
    print_result("POST /sum  →  [1 .. 10]", status, body)

    print(f"\n{BOLD}── 4. Missing API Key  (expect 401) ─────────────────{RESET}")
    status, body = make_request("POST", "/sum", payload={"numbers": [1, 2, 3]})
    print_result("POST /sum  →  no X-API-KEY", status, body)

    print(f"\n{BOLD}── 5. Wrong API Key  (expect 401) ───────────────────{RESET}")
    status, body = make_request(
        "POST", "/sum",
        payload={"numbers": [1, 2, 3]},
        headers={"X-API-KEY": "wrongkey"}
    )
    print_result("POST /sum  →  X-API-KEY: wrongkey", status, body)

    print(f"\n{BOLD}── 6. Non-numeric Input  (expect 422) ───────────────{RESET}")
    status, body = make_request(
        "POST", "/sum",
        payload={"numbers": [1, "two", 3]},
        headers={"X-API-KEY": API_KEY}
    )
    print_result('POST /sum  →  [1, "two", 3]', status, body)

    print(f"\n{BOLD}── 7. Empty List  (expect 422) ──────────────────────{RESET}")
    status, body = make_request(
        "POST", "/sum",
        payload={"numbers": []},
        headers={"X-API-KEY": API_KEY}
    )
    print_result("POST /sum  →  []", status, body)

    print(f"\n{BOLD}{'═' * 54}")
    print(f"  Demo complete.")
    print(f"{'═' * 54}{RESET}\n")


if __name__ == "__main__":
    run()