#!/usr/bin/env python3
"""
GeoReady MCP Server (Model Context Protocol — JSON-RPC 2.0 over stdio)
======================================================================
Zero-dependency MCP server allowing Claude Desktop, Cursor, Windsurf, and Cline
to audit any website's 2026 Generative Engine Optimization (GEO) score and
generate ready-to-deploy `robots.txt`, `llms.txt`, `Content-Signal` headers,
and JSON-LD structured data.

Interactive Web Scanner & Sitemap Pro Suite: https://geoready.aitruelabs.com
"""

import json
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict

API_BASE = "https://geoready.aitruelabs.com/api/scan"
SSL_CTX = ssl._create_unverified_context()

TOOLS_SPEC = [
    {
        "name": "audit_website_geo_readiness",
        "description": (
            "Runs a live 8-point Generative Engine Optimization (GEO) & ChatGPT Shopping "
            "audit on any public website URL: checks AI crawler access, /llms.txt, "
            "Accept: text/markdown token bloat, Content-Signal headers, and JSON-LD schema, "
            "and returns ready-to-deploy remediation snippets."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public website domain or URL to inspect (e.g. 'https://example.com').",
                }
            },
            "required": ["url"],
        },
    }
]


def call_live_scan(target_url: str) -> Dict[str, Any]:
    q = f"{API_BASE}?url={urllib.parse.quote(target_url)}"
    req = urllib.request.Request(q, headers={"User-Agent": "GeoReadyMCP/1.0"})
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def handle_rpc(req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        proto = ((req.get("params") or {}).get("protocolVersion")) or "2024-11-05"
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": proto if proto in ("2024-11-05", "2025-03-26") else "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "geoready-auditor", "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_SPEC}}
    if method == "tools/call":
        params = req.get("params") or {}
        args = params.get("arguments") or {}
        if params.get("name") != "audit_website_geo_readiness":
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Unknown tool"}}
        try:
            res = call_live_scan(str(args.get("url") or ""))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]},
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"error": str(exc)})}]},
            }

    if req_id is None:
        return {}
    return {"jsonrpc": "2.0", "id": req_id, "result": {}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle_rpc(req)
        if resp:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
