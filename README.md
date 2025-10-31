# URL Tester Application

> High-performance concurrent URL testing tool for QA teams

##  Quick Start

Run the application:
```bash
python main.py
```

Choose your testing mode:
- **Option 1:** Test defined URL list
- **Option 2:** Test URLs from sitemap(s)

Results saved to: `test_results_YYYYMMDD_HHMMSS.xlsx`

---

##  Mode 1: Defined URL List

Edit `urls_to_test.xlsx`:

| root                    | url        |
|-------------------------|------------|
| https://yoursite.com    | /home      |
|                         | /about     |
|                         | /contact   |

- **Root URL:** Enter once in the first row
- **URL paths:** Can be relative (`/page`) or full URLs
- Application combines root + path and tests each URL

---

##  Mode 2: Sitemap Parsing

Edit `sitemaps.xlsx`:

| sitemap_url                           | root (optional)           |
|---------------------------------------|---------------------------|
| https://yoursite.com/sitemap.xml      |                           |
| https://prod.com/sitemap.xml          | https://dev.example.com   |

**Key Features:**
- List specific sitemap URLs to test (one per row)
- **Optional root column:** Test production sitemaps on dev environment
- **No nested crawling:** Sitemap indices are skipped - you control exactly what gets tested

**Example:** Production sitemap has `https://prod.com/page1`, but you set root to `https://dev.example.com` → tests `https://dev.example.com/page1`

---

##  Results

- Only **non-200** responses are reported (errors, redirects, timeouts)
- Report includes: source URL, tested URL, status code, error message, timestamp
- Real-time progress with requests/second rate

---

##  Performance

- **100 concurrent threads** - threads continuously pick up work as they finish
- **5 second timeout** per request
- **Example speeds:**
  - 10,000 URLs → ~2-3 minutes
- Fast URLs don't wait for slow ones

---


##  Key Design Patterns

1. **Strategy Pattern** - Different URL providers (Excel, Sitemap)
2. **Service Layer** - Business logic separated from infrastructure
3. **Dependency Inversion** - Application depends on abstractions, not implementations

**Result:** Clean, extensible code that follows SOLID principles

---

##  Building Executable

### Quick Build (Windows)
```bash
build.bat
```

This creates `url_tester.exe` (~8-15 MB with UPX compression)

### Size Optimization
The build configuration excludes unnecessary modules and uses compression:
- ✅ Only bundles required dependencies (requests, openpyxl)
- ✅ Excludes heavy libraries (numpy, pandas, tkinter, etc.)
- ✅ Uses UPX compression (install from https://upx.github.io/)
- ✅ Strips debug symbols

**Expected sizes:**
- Without UPX: ~15-25 MB
- With UPX: ~8-15 MB

See `BUILD_INSTRUCTIONS.md` for details.