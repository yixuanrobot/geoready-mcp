#!/usr/bin/env python3
"""
AI True Labs — AI Shopping & GMC Schema Auditor MCP Server
(Model Context Protocol — JSON-RPC 2.0 over stdio, zero external dependencies)
==============================================================================
Lets Claude Desktop, Claude Code, Cursor, Windsurf, and Cline run live
Shopify ChatGPT Shopping (ACP) & Google Merchant Center (GMC) revenue audits
via https://geoready.aitruelabs.com/api/scan:
  - Live OAI-SearchBot/1.0 & PerplexityBot/1.0 HTTP 403 / Cloudflare WAF probe
  - Full-document (up to 5MB) JSON-LD Product/Offer parity vs /products.json
  - GMC OfferShippingDetails & hasMerchantReturnPolicy misrepresentation checks
  - Shopify variant GTIN (8/12/13/14-digit) & SKU completeness
  - First-50-Token product spec density & HTML token bloat %
  - 5-file verified remediation pack (Shopify-safe robots.txt.liquid free;
    zero-JS shoppingSchemaSnippet, wafPlaybook, llmsCatalog, edgeMarkdownWorker unlocked via license)

Web Suite & Agency White-Label PDFs: https://geoready.aitruelabs.com
Studio: https://aitruelabs.com | support@aitruelabs.com
"""

import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict

API_BASE = "https://geoready.aitruelabs.com/api/scan"
WEB_BASE = "https://geoready.aitruelabs.com"
UPGRADE_URL = "https://geoready.aitruelabs.com/#pricing"
SSL_CTX = ssl._create_unverified_context()

TOOLS_SPEC = [
    {
        "name": "audit_website_geo_readiness",
        "description": (
            "AI True Labs — AI Shopping & GMC Schema Auditor. Runs a live 6-pillar "
            "Shopify ChatGPT Shopping (ACP) & Google Merchant Center (GMC) audit on any "
            "public storefront, Shopify product page (/products/...), or website URL: "
            "1) Live OAI-SearchBot/1.0 & PerplexityBot/1.0 HTTP 403/WAF probes, "
            "2) Full-document (up to 5MB) JSON-LD Product/Offer price parity vs live /products.json + "
            "OfferShippingDetails & hasMerchantReturnPolicy GMC checks, "
            "3) Shopify variant GTIN (8/12/13/14-digit) & SKU completeness, "
            "4) First-50-Token spec density & HTML token bloat, "
            "5) Shopify-safe robots.txt.liquid & /llms.txt hygiene, "
            "6) Semantic citability. Returns the complete 0-100 scorecard, ecommerceAudit diagnostics, "
            "and Shopify-safe robots.txt for free; unlocks all 5 verified fix-pack files when "
            "GEOREADY_LICENSE_KEY (or AITRUELABS_LICENSE_KEY) is set."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": (
                        "Public Shopify product URL (e.g. 'https://www.allbirds.com/products/mens-tree-runners') "
                        "or website URL to audit."
                    ),
                },
                "license_key": {
                    "type": "string",
                    "description": (
                        "Optional AI True Labs License Key, Creem Order ID (ord_...), Checkout ID (ch_...), "
                        "or Billing Email (overrides GEOREADY_LICENSE_KEY / AITRUELABS_LICENSE_KEY env vars)."
                    ),
                },
            },
            "required": ["url"],
        },
    }
]


def _build_audit_summary(data: Dict[str, Any], target_url: str) -> Dict[str, Any]:
    checks = data.get("checks") or []
    ecom = data.get("ecommerceAudit") or {}
    extracted = data.get("extracted") or {}

    crawler_check = next((c for c in checks if c.get("id") == "ai_crawler_access"), {})
    schema_check = next((c for c in checks if c.get("id") in ("shopping_schema_gmc", "json_ld_graph")), {})
    gtin_check = next((c for c in checks if c.get("id") == "gtin_sku_feed_parity"), {})
    token_check = next((c for c in checks if c.get("id") in ("first_50_token_density", "markdown_negotiation")), {})

    probes = ecom.get("crawlerProbes") or {}
    catalog = ecom.get("catalogFeed") or {}
    parity = ecom.get("schemaParity") or {}
    tok_eff = ecom.get("tokenEfficiency") or {}

    return {
        "auditor": "AI True Labs — AI Shopping & GMC Schema Auditor",
        "scannedUrl": data.get("scannedUrl") or target_url,
        "hostname": data.get("hostname") or "",
        "brandName": extracted.get("brandName") or data.get("hostname") or "",
        "isShopify": bool(data.get("isShopify") or ecom.get("isShopify")),
        "totalScore": data.get("totalScore"),
        "grade": data.get("grade"),
        "botBlocked": bool(data.get("botBlocked") or ecom.get("botBlocked")),
        "interstitialDetected": bool(data.get("interstitialDetected") or ecom.get("interstitialDetected")),
        "oaiSearchBotStatus": crawler_check.get("oaiStatus", (probes.get("oaiSearchBot") or {}).get("status")),
        "perplexityBotStatus": crawler_check.get("perplexityStatus", (probes.get("perplexityBot") or {}).get("status")),
        "gmcMisrepresentationRisk": parity.get("gmcMisrepresentationRisk", schema_check.get("gmcMisrepresentationRisk")),
        "priceParityStatus": parity.get("priceParityStatus", schema_check.get("priceParityStatus")),
        "hasShippingDetails": parity.get("hasShippingDetails", schema_check.get("hasShippingDetails")),
        "hasMerchantReturnPolicy": parity.get("hasMerchantReturnPolicy", schema_check.get("hasMerchantReturnPolicy")),
        "totalVariantsAudited": catalog.get("totalVariantsAudited", gtin_check.get("totalVariantsAudited")),
        "variantsMissingGtin": catalog.get("variantsMissingGtin", gtin_check.get("variantsMissingGtin")),
        "gtinCompletenessPct": catalog.get("gtinCompletenessPct", gtin_check.get("gtinCompletenessPct")),
        "tokenBloatPct": tok_eff.get("bloatPct", token_check.get("bloatPct")),
        "first50HasPriceOrSpec": tok_eff.get("first50HasPriceOrSpec", token_check.get("first50HasPriceOrSpec")),
        "criticalBlockers": ecom.get("criticalBlockers") or [],
        "proUnlocked": bool(data.get("proUnlocked")),
        "licenseTier": data.get("licenseTier") or ("pro" if data.get("proUnlocked") else "free"),
        "interactiveReportUrl": f"{WEB_BASE}/?scan={urllib.parse.quote(target_url, safe='')}",
    }


def call_live_scan(target_url: str, arg_license_key: str = "") -> Dict[str, Any]:
    q = f"{API_BASE}?url={urllib.parse.quote(target_url, safe='')}"
    headers = {"User-Agent": "AITrueLabs-MCP/1.2"}
    lic = (
        arg_license_key
        or os.environ.get("GEOREADY_LICENSE_KEY")
        or os.environ.get("AITRUELABS_LICENSE_KEY")
        or ""
    ).strip()
    if lic:
        headers["x-geoready-license"] = lic
    if os.environ.get("AITRUELABS_QA_SKIP") == "1":
        headers["x-qa-skip"] = "1"

    req = urllib.request.Request(q, headers=headers)
    with urllib.request.urlopen(req, timeout=25, context=SSL_CTX) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))

    if isinstance(data, dict) and not data.get("error"):
        data["auditSummary"] = _build_audit_summary(data, target_url)
        if data.get("domainMismatch"):
            data["upgradeNotice"] = (
                f"Single-Store License Domain Lock: {data.get('domainMismatchMessage') or 'License is bound to another store.'} "
                f"Upgrade to Starter ($39/mo) or Agency White-Label ($79/mo) at {UPGRADE_URL}."
            )
        elif not data.get("proUnlocked"):
            data["upgradeNotice"] = (
                "Free Tier Active: Full 6-pillar AI Shopping & GMC scorecard, live OAI-SearchBot/PerplexityBot "
                "probes, Shopify GTIN/price parity diagnostics, and Shopify-safe robots.txt included. "
                "Paid fix-pack files (shoppingSchemaSnippet, wafPlaybook, llmsCatalog, edgeMarkdownWorker) "
                "show a customized preview. Unlock the Single-Store Fix Pack ($29 One-Time), Starter ($39/mo), "
                f"or Agency White-Label ($79/mo) at {UPGRADE_URL} and set env GEOREADY_LICENSE_KEY."
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
                "serverInfo": {"name": "aitruelabs-shopping-auditor", "version": "1.2.0"},
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
