# AI True Labs — AI Shopping & GMC Schema Auditor MCP Server (`geoready-mcp` v1.2.0)

**Zero-dependency Model Context Protocol (MCP) server by [AI True Labs](https://aitruelabs.com) for Shopify ChatGPT Shopping (ACP), Google Merchant Center (GMC) JSON-LD parity, variant GTIN completeness, and live `OAI-SearchBot` / `PerplexityBot` HTTP 403 WAF auditing.**

Let **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf**, and **Cline** audit any live Shopify product page (`/products/...`), storefront, or website across 6 deterministic revenue-blocker benchmarks and generate verified zero-JS Shopify Liquid & Cloudflare WAF fix packs.

> **Interactive Web Auditor, Competitor Battlecards & Agency White-Label Client Pitch PDFs:** **[https://geoready.aitruelabs.com](https://geoready.aitruelabs.com)**

---

## Quick Start (`uvx` — Zero Install)

Add to your `claude_desktop_config.json` or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aitruelabs-shopping-auditor": {
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

- **Free Tier (`GEOREADY_LICENSE_KEY` empty):** Unlimited live 6-pillar AI Shopping & GMC scorecards (`0–100` score + grade + `auditSummary` + full `ecommerceAudit`), live `OAI-SearchBot` / `PerplexityBot` HTTP status, Shopify `/products.json` price & GTIN parity diagnostics, and a Shopify-safe `templates/robots.txt.liquid` (`{% for group in robots.default_groups %}`).
- **Pro Fix-Pack Unlock (`$29` One-Time Single-Store, `$39/mo` Multi-Store Starter, or `$79/mo` Agency White-Label):** Paste your AI True Labs / Creem License Key, Order ID (`ord_...`), Checkout ID (`ch_...`), or Billing Email into `GEOREADY_LICENSE_KEY` (or `AITRUELABS_LICENSE_KEY`) to unlock all 5 verified remediation files directly inside Cursor / Claude Code:
  1. `robotsTxt` — Shopify-safe `templates/robots.txt.liquid` or standard `robots.txt`
  2. `shoppingSchemaSnippet` — Zero-JS `snippets/aitruelabs-shopping-schema.liquid` with `OfferShippingDetails`, `hasMerchantReturnPolicy`, and conditional `gtin8/12/13/14`
  3. `wafPlaybook` — Cloudflare WAF `cf.client.bot` Custom Rule to stop `403` AI crawler blocks
  4. `llmsCatalog` — Shopify `templates/llms.txt.liquid` (`{% layout none %}`) + live catalog loop
  5. `edgeMarkdownWorker` — Standalone ESM Cloudflare Worker (`export default { async fetch }`) for advanced/headless setups

## What `audit_website_geo_readiness` Checks (6 Pillars, 0–100 Score)

1. **Live AI Crawler Access (`ai_crawler_access`, 20 pts)** — Parallel `OAI-SearchBot/1.0` and `PerplexityBot/1.0` probes detecting HTTP `403`/`503` Cloudflare WAF blocks and Shopify geo-interstitials, plus `/robots.txt` rules.
2. **Shopping Schema & GMC Parity (`shopping_schema_gmc`, 25 pts)** — Full-document (up to 5MB) JSON-LD extraction verifying `Product`/`Offer`, live price parity vs Shopify `/products.json`, `OfferShippingDetails`, and `hasMerchantReturnPolicy` (GMC `Misrepresentation` blockers).
3. **Variant GTIN & SKU Feed Parity (`gtin_sku_feed_parity`, 15 pts)** — Live Shopify `/products.json` & `/products/<handle>.json` inspection measuring exact variant GTIN (8/12/13/14-digit numeric) and SKU completeness.
4. **First-50-Token Spec Density & HTML Bloat (`first_50_token_density`, 15 pts)** — Checks whether product price/specs appear inside the first 50 clean text tokens, measures HTML token waste %, and checks `Accept: text/markdown` & `Content-Signal`.
5. **Shopify `robots.txt.liquid` & Native `/llms.txt` Hygiene (`robots_and_llms_hygiene`, 15 pts)** — Validates Shopify `robots.default_groups`, sitemap directives, and `/llms.txt` validity.
6. **Semantic Citability (`semantic_citability`, 10 pts)** — Single-`<h1>` check, canonical tag, and structured spec `<table>` density.

---

## License

MIT © [AI True Labs](https://aitruelabs.com) (`support@aitruelabs.com`)
