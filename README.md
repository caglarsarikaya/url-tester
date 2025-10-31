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

Configure performance settings:
- **Press Enter** to use defaults, or **enter value and press Enter** to customize

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

##  Performance Configuration

The application asks for three settings at startup (press Enter for defaults):

### 1. **Concurrent Threads** [default: 50]
- **What it does:** Number of URLs tested simultaneously
- **Higher value (100+):** Faster testing but may trigger rate limiting
- **Lower value (10-20):** Slower but more reliable for protected sites
- **Example:** Use 20 threads to avoid timeouts

### 2. **Request Timeout (milliseconds)** [default: 10000ms = 10s]
- **What it does:** Maximum wait time for each URL response
- **Higher value (15000ms):** Better for slow servers
- **Lower value (5000ms):** Faster overall but may cause false timeout errors
- **Example:** Getting timeouts? Increase to 15000ms

### 3. **Delay Between Requests (milliseconds)** [default: 100ms]
- **What it does:** Pause between each request (rate limiting)
- **Higher value (200ms):** More polite, prevents server overload
- **Lower value (0ms):** Maximum speed but may trigger rate limiting
- **Example:** Server blocking you? Increase to 150-200ms

### ⚠️ Important Notes
- **Increasing threads OR decreasing delay = Higher chance of timeouts**
- **Too aggressive settings may trigger server rate limiting**
- **Better to test slower with accurate results than fast with false errors**

### 📊 Recommended Presets

| Scenario | Threads | Timeout | Delay |
|----------|---------|---------|-------|
| Fast servers | 100 | 5000ms | 0ms |
| Balanced (default) | 50 | 10000ms | 100ms |
| CDN sites | 20 | 15000ms | 150ms |
| Protected servers | 10 | 20000ms | 200ms |

### Example Speeds
- **10,000 URLs** → 2-10 minutes (depends on settings)
- **100,000 URLs** → 20-60 minutes (depends on settings)

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