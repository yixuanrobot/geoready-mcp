# 🛰️ GeoReady MCP Server (`geoready-mcp`)

**Zero-dependency Model Context Protocol (MCP) server for 2026 Generative Engine Optimization (GEO), ChatGPT Shopping Schema & AI Agent Readiness auditing.**

Let **Claude Desktop**, **Claude Code**, **Cursor**, and **Windsurf** inspect any live website across 8 deterministic GEO benchmarks and generate ready-to-deploy `robots.txt`, `/llms.txt`, `/llms-full.txt`, Cloudflare Edge `Accept: text/markdown` Workers, and Shopify/HTML `JSON-LD` structured data.

> 🌐 **Interactive Web Scanner, Competitor Battlecards & Agency White-Label PDFs**: **[https://geoready.aitruelabs.com](https://geoready.aitruelabs.com)**

---

## Quick Start (`uvx` — Zero Install)

Add to your `claude_desktop_config.json` or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "geoready-auditor": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yixuanrobot/geoready-mcp",
        "geoready-mcp"
      ],
      "env": {
        "GEOREADY_LICENSE_KEY": ""
      }
    }
  }
}
```

- **Free Tier (`GEOREADY_LICENSE_KEY` empty)**: Unlimited live 8-point GEO diagnostics (0–100 score + letter grade), full AI-ready `robots.txt`, and 5-line customized remediation previews.
- **Pro Fix-Pack Unlock (`$29 One-Time` or `$79/mo Agency`)**: Paste your Creem Order ID (`ord_...`), Checkout ID (`ch_...`), or Billing Email into `GEOREADY_LICENSE_KEY` to unlock full unredacted `/llms.txt`, `/llms-full.txt`, Cloudflare Edge `Accept: text/markdown` Worker (`_middleware.js` + `_headers`), and Shopify Liquid + HTML `JSON-LD` kits directly inside Cursor / Claude Code.

## What `audit_website_geo_readiness` Checks (0–100 Score)

1. **AI Crawler Access & `robots.txt`** (`OAI-SearchBot`, `GPTBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `Google-Extended` + firewall HTTP 403 challenge detection)
2. **`/llms.txt` & `/llms-full.txt` Specification** (detects broken SPA HTML fallbacks)
3. **`Accept: text/markdown` Negotiation & Token Bloat %**
4. **JSON-LD Knowledge Graph & ChatGPT Shopping Offers** (`Organization`, `Product`/`SoftwareApplication`, `FAQPage`)
5. **2026 `Content-Signal` HTTP Headers** (`ai-train=no, search=yes, ai-input=yes`)
6. **Citation Metadata & Semantic Headings**
7. **Structured Table & Quantifiable Fact Density**
8. **XML Sitemap Discovery**

---

## License

MIT © [AI True Labs](https://aitruelabs.com) (`support@aitruelabs.com`)
