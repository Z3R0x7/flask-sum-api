# flask-sum-api

![CI](https://github.com/Z3R0x7/flask-sum-api/actions/workflows/ci.yml/badge.svg)

A secure REST API that performs a **sequential sum** — each number is accumulated one operation at a time, no shortcuts. Built with Flask, protected via API key authentication, containerized with Docker.

---

## Setup

```bash
git clone https://github.com/Z3R0x7/flask-sum-api.git
cd flask-sum-api
pip3 install -r requirements.txt
```

---

## Running the Server

> ⚠️ Port 5000 is reserved by macOS AirPlay. Always use **port 8080**.

```bash
API_KEY=test123 python3 -m flask --app app.main run --port 8080
```

The server starts at `http://localhost:8080` and stays running until you press `Ctrl+C`.

**The API key for this project is `test123`** — pass it in every request as the `X-API-KEY` header.

---

## Running Tests

Open a new terminal window (the server does not need to be running for tests):

```bash
python3 -m pytest tests/ -v
```

Expected output: **13 passed**

---

## Live Demo

With the server running, open a second terminal and run:

```bash
python3 demo.py
```

This fires 7 requests covering all scenarios — success, wrong key, bad data — and prints color-coded results.

---

## Checking Your Files

Before pushing to GitHub, run:

```bash
python3 check.py
```

This verifies all required files exist, confirms `.env` is not present, and flags any junk like `__pycache__` or `.DS_Store`.

---

## API Reference

### `GET /health`
No auth required. Confirms the server is alive.

```bash
curl http://localhost:8080/health
```
```json
{ "status": "ok" }
```

---

### `POST /sum`

| Header | Value |
|--------|-------|
| `X-API-KEY` | `test123` |
| `Content-Type` | `application/json` |

**Successful request (200)**
```bash
curl -X POST http://localhost:8080/sum \
  -H "X-API-KEY: test123" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [5, 10, 15]}'
```
```json
{
  "result": 30,
  "operations_performed": 3,
  "message": "Each number was added one at a time, sequentially, no shortcuts. Kind of like how I'd handle every task in this club — methodically. Just saying. 👀"
}
```

**Missing or wrong API key (401)**
```bash
curl -X POST http://localhost:8080/sum \
  -H "X-API-KEY: wrongkey" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [5, 10, 15]}'
```
```json
{ "error": "Unauthorized. Provide a valid X-API-KEY header." }
```

**Non-numeric data (422)**
```bash
curl -X POST http://localhost:8080/sum \
  -H "X-API-KEY: test123" \
  -H "Content-Type: application/json" \
  -d '{"numbers": [1, "two", 3]}'
```
```json
{ "error": "All elements must be integers or floats." }
```

---

## Docker

```bash
docker build -t sum-api .
docker run -p 8080:5000 -e API_KEY=test123 sum-api
```

---

## Security Considerations

- API key loaded from environment variable — never hardcoded
- Key passed via header, not URL — prevents credential leaking in server logs
- `silent=True` on JSON parsing — avoids exposing internals on malformed input
- Strict type validation before any computation
- Distinct HTTP codes: `401` auth failure, `400` bad structure, `422` bad data
- `.env` in `.gitignore` — credentials never committed to version control

---

## Project Structure

```
flask-sum-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .github/workflows/
│   └── ci.yml
├── conftest.py
├── pytest.ini
├── check.py
├── demo.py
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```