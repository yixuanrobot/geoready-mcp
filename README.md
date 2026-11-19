# 🛰️ GeoReady MCP Server (`geoready-mcp`)

**Zero-dependency Model Context Protocol (MCP) server for 2026 Generative Engine Optimization (GEO), ChatGPT Shopping Schema & AI Agent Readiness auditing.**

Let **Claude Desktop**, **Claude Code**, **Cursor**, and **Windsurf** inspect any live website across 8 deterministic GEO benchmarks and generate ready-to-deploy `robots.txt`, `/llms.txt`, `Content-Signal` HTTP headers, and `JSON-LD` structured data.

> 🌐 **Interactive Web Scanner & Multi-Page Sitemap Batch Suite**: **[https://geoready.aitruelabs.com](https://geoready.aitruelabs.com)**

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
      ]
    }
  }
}
```

## What `audit_website_geo_readiness` Checks (0–100 Score)

1. **AI Crawler Access & `robots.txt`** (`OAI-SearchBot`, `GPTBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `Google-Extended` + firewall challenge detection)
2. **`/llms.txt` & `/llms-full.txt` Specification** (detects broken SPA HTML fallbacks)
3. **`Accept: text/markdown` Negotiation & Token Bloat %**
4. **JSON-LD Knowledge Graph & ChatGPT Shopping Offers** (`Organization`, `Product`/`SoftwareApplication`, `FAQPage`)
5. **2026 `Content-Signal` HTTP Headers** (`ai-train=yes, search=yes, ai-input=yes`)
6. **Citation Metadata & Semantic Headings**
7. **Structured Table & Quantifiable Fact Density**
8. **XML Sitemap Discovery**

---

## License

MIT © [AI True Labs](https://aitruelabs.com) (`support@aitruelabs.com`)
