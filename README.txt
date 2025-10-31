================================================================
                    URL TESTER APPLICATION
================================================================

HIGH-PERFORMANCE CONCURRENT URL TESTING TOOL

HOW IT WORKS:
- Uses multi-threaded concurrent requests (20 parallel threads)
- Sends requests in parallel without waiting for slow responses
- Example: If 19 URLs respond in 1sec and 1 takes 30sec, the slow 
  one doesn't block the others - threads continuously pick up new 
  work as they finish
- Result: ~10-20x faster than sequential testing
- Perfect for testing thousands of URLs efficiently

================================================================

QUICK START:

1. Double-click "url_tester.exe"

2. Choose your testing mode:
   - Option 1: Test defined URL list
   - Option 2: Test URLs from sitemap(s)

3. Results will be saved to a new Excel file with timestamp

================================================================

MODE 1: DEFINED URL LIST (urls_to_test.xlsx)

Edit "urls_to_test.xlsx":

| root                    | url        |
|-------------------------|------------|
| https://yoursite.com    | /home      |
|                         | /about     |
|                         | /contact   |

- Root URL: Enter once in the first row
- URL paths: Can be relative (/page) or full URLs

================================================================

MODE 2: SITEMAP PARSING (sitemaps.xlsx)

Edit "sitemaps.xlsx":

| sitemap_url                           |
|---------------------------------------|
| https://yoursite.com/sitemap.xml      |
| https://yoursite.com/sitemap_news.xml |

- List EXACTLY which sitemap URLs you want to test (one per row)
- App will fetch and test all URLs from those specific sitemaps
- NO AUTOMATIC CRAWLING: If a sitemap contains links to other 
  sitemaps (sitemap index), it will be SKIPPED
- Why? Sitemaps can be messy with deep nesting - you control 
  exactly what gets tested by listing specific sitemap URLs
- You have full control - no surprises!

================================================================

RESULTS:

- All URLs with status 200 (OK) are considered successful
- Any errors (300, 400, 500, timeouts, etc.) are saved to:
  test_results_YYYYMMDD_HHMMSS.xlsx
- Progress shows real-time request rate (requests/second)
- Final summary includes total time and average speed

================================================================

PERFORMANCE:

- Max concurrent requests: 20 threads
- Threads work independently - slow responses don't block fast ones
- Typical speed: 10-20 requests/second (depends on server response)
- Example: 10,000 URLs can be tested in ~10-15 minutes

================================================================

FILES INCLUDED:

- url_tester.exe        : The application
- urls_to_test.xlsx     : For defined URL list mode
- sitemaps.xlsx         : For sitemap parsing mode
- README.txt            : This file

================================================================

