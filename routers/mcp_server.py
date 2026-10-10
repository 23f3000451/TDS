# routers/mcp_server.py
import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

REGISTERED_EMAIL = "23f3000451@ds.study.iitm.ac.in"

mcp = FastMCP("Exam Challenge Server")


@mcp.tool()
def solve_challenge() -> str:
    """Solves the exam challenge: first 16 hex of SHA-256(challenge:email)."""
    headers = get_http_headers()
    challenge = headers.get("x-exam-challenge", "")

    if not challenge:
        return "Error: X-Exam-Challenge header missing"

    digest = hashlib.sha256(
        f"{challenge}:{REGISTERED_EMAIL}".encode("utf-8")
    ).hexdigest()
    return digest[:16]


# ASGI sub-app to mount in main.py
# mcp_app = mcp.http_app()

mcp_app = mcp.http_app(path="/")
