#!/usr/bin/env python3
"""
GeoReady MCP Server (Model Context Protocol — JSON-RPC 2.0 over stdio)
======================================================================
Zero-dependency MCP server allowing Claude Desktop, Claude Code, Cursor, Windsurf,
and Cline to audit any website's 2026 Generative Engine Optimization (GEO) score
across 8 deterministic benchmarks via https://geoready.aitruelabs.com/api/scan.

Interactive Web Scanner, Competitor Battlecards & Agency Suite: https://geoready.aitruelabs.com
"""

import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict

API_BASE = "https://geoready.aitruelabs.com/api/scan"
UPGRADE_URL = "https://geoready.aitruelabs.com/#pricing"
SSL_CTX = ssl._create_unverified_context()

TOOLS_SPEC = [
    {
        "name": "audit_website_geo_readiness",
        "description": (
            "Runs a live 8-point Generative Engine Optimization (GEO) & ChatGPT Shopping "
            "audit on any public website URL: checks AI crawler access, /llms.txt, "
            "Accept: text/markdown token bloat, Content-Signal headers, and JSON-LD schema. "
            "Returns full 8-point diagnostics + AI-ready robots.txt for free, and unlocks "
            "unredacted llms.txt, llms-full.txt, Cloudflare Edge Markdown Worker, and "
            "Shopify/HTML JSON-LD when GEOREADY_LICENSE_KEY is configured."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public website domain or URL to inspect (e.g. 'https://example.com').",
                },
                "license_key": {
                    "type": "string",
                    "description": "Optional GeoReady Pro Order ID (ord_...), Checkout ID (ch_...), or Billing Email (overrides GEOREADY_LICENSE_KEY env var).",
                },
            },
            "required": ["url"],
        },
    }
]


def call_live_scan(target_url: str, arg_license_key: str = "") -> Dict[str, Any]:
    q = f"{API_BASE}?url={urllib.parse.quote(target_url)}"
    headers = {"User-Agent": "GeoReadyMCP/1.1"}
    lic = (arg_license_key or os.environ.get("GEOREADY_LICENSE_KEY") or "").strip()
    if lic:
        headers["x-geoready-license"] = lic

    req = urllib.request.Request(q, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))

    if isinstance(data, dict) and not data.get("proUnlocked"):
        data["upgradeNotice"] = (
            f"Free Tier Active: Full 8-point GEO scorecard + AI-ready robots.txt included. "
            f"Paid remediation files (llmsTxt, llmsFullTxt, cloudflareBundle, jsonLdSnippet) "
            f"show a 5-line customized preview. Unlock the Single-Store Fix Pack ($29 One-Time) "
            f"or Agency Pro ($79/mo) at {UPGRADE_URL} and set env GEOREADY_LICENSE_KEY."
        )
    return data


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
                "serverInfo": {"name": "geoready-auditor", "version": "1.1.0"},
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
            res = call_live_scan(
                str(args.get("url") or ""),
                str(args.get("license_key") or ""),
            )
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
