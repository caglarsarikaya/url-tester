# VS Code Debug Guide

## 🐛 Quick Start

Press **F5** or click the **Run and Debug** icon (left sidebar) to see debug configurations.

---

## 📋 Available Debug Configurations

### 1. **Run URL Tester - Defined List Mode**
- Tests URLs from `urls_to_test.xlsx`
- Just press F5 and choose option 1
- Use breakpoints to step through code

### 2. **Run URL Tester - Sitemap Mode**
- Tests URLs from `sitemaps.xlsx`
- Just press F5 and choose option 2

### 3. **Debug Current File**
- Debugs whatever file you have open
- Useful for testing individual modules

### 4. **Debug with External Libraries**
- Steps into requests/openpyxl code
- Use when debugging library-related issues
- `justMyCode: false` allows stepping into dependencies

### 5. **Test URL Provider - Defined List**
- Debug URL provider in isolation
- Test Excel reading logic

### 6. **Test URL Provider - Sitemap**
- Debug sitemap parsing in isolation
- Test XML parsing logic

---

## 🔧 Quick Tasks (Ctrl+Shift+P → "Run Task")

### Run Tasks
- **Run URL Tester** - Run without debugging
- **Build Executable** - Build with PyInstaller
- **Clean Build Artifacts** - Remove build folders
- **Install Dependencies** - Install from requirements.txt
- **Install Build Tools** - Install PyInstaller
- **Validate Python Syntax** - Check all files for syntax errors

---

## 🎯 Debugging Tips

### Set Breakpoints
1. Click left margin next to line number (red dot appears)
2. Press F5 to start debugging
3. Execution pauses at breakpoint

### Debug Controls
- **F5** - Continue
- **F10** - Step Over (next line)
- **F11** - Step Into (enter function)
- **Shift+F11** - Step Out (exit function)
- **Ctrl+Shift+F5** - Restart
- **Shift+F5** - Stop

### Watch Variables
- **Variables** panel shows local variables
- **Watch** panel for custom expressions
- Hover over variables to see values

### Debug Console
- Type expressions to evaluate
- Test function calls
- Check variable values

---

## 🔍 Common Debug Scenarios

### Scenario 1: Excel File Not Reading Correctly
```
1. Set breakpoint in src/excel_handler.py line 40
2. Run "Debug Current File"
3. Inspect 'rows' variable
4. Check column headers
```

### Scenario 2: URLs Not Being Tested
```
1. Set breakpoint in src/url_tester.py line 80
2. Run debug configuration
3. Check url_requests list
4. Verify full_url construction
```

### Scenario 3: Report Not Generated
```
1. Set breakpoint in src/report_generator.py line 30
2. Run debug configuration
3. Inspect results list
4. Check if results is empty
```

### Scenario 4: Sitemap Parsing Issues
```
1. Set breakpoint in src/url_providers.py line 100
2. Run "Test URL Provider - Sitemap"
3. Step through _parse_sitemap()
4. Inspect XML response
```

---

## 🧪 Testing Individual Components

### Test Excel Reader
```python
# Open src/excel_handler.py
# Add at bottom:
if __name__ == "__main__":
    reader = ExcelReader('urls_to_test.xlsx')
    rows = reader.read_rows(['root', 'url'])
    print(f"Read {len(rows)} rows")
    for row in rows:
        print(row)

# Press F5 with "Debug Current File" selected
```

### Test URL Provider
```python
# Open src/url_providers.py
# Add at bottom:
if __name__ == "__main__":
    provider = DefinedListProvider('urls_to_test.xlsx')
    urls = provider.get_urls()
    print(f"Got {len(urls)} URLs")
    for url in urls[:5]:  # First 5
        print(url.get_full_url())
```

---

## ⚙️ Settings Configured

### Python Analysis
- Type checking: basic
- Auto imports: enabled
- Extra paths include `src/` folder

### File Exclusions
- `__pycache__` hidden
- `build/` and `dist/` hidden
- `.pyc` files hidden

### Terminal
- `PYTHONPATH` automatically set to workspace folder
- Allows importing from `src/` module

---

## 🚀 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Start Debugging | F5 |
| Run Without Debug | Ctrl+F5 |
| Toggle Breakpoint | F9 |
| Step Over | F10 |
| Step Into | F11 |
| Step Out | Shift+F11 |
| Continue | F5 |
| Stop | Shift+F5 |
| Debug Console | Ctrl+Shift+Y |

---

## 💡 Pro Tips

1. **Use Conditional Breakpoints**
   - Right-click breakpoint → Edit Breakpoint
   - Add condition: `url == 'https://example.com'`

2. **Log Points (Don't Stop Execution)**
   - Right-click line → Add Logpoint
   - Message: `URL: {url}, Status: {status}`

3. **Exception Breakpoints**
   - Debug panel → Breakpoints → Check "Raised Exceptions"
   - Stops on any exception

4. **Multi-threading Debug**
   - Use "Debug with External Libraries" config
   - Check threads in "Call Stack" panel

5. **Quick Variable Inspection**
   - Hover over variable
   - Or add to Watch panel for persistent monitoring

---

## 📚 Common Issues

### "Module not found"
- Check `PYTHONPATH` in terminal
- Run task: "Install Dependencies"

### Breakpoints not hitting
- Check if file is saved
- Verify correct debug config selected
- Check if `justMyCode: true` is limiting scope

### Can't see library code
- Use "Debug with External Libraries" config
- This sets `justMyCode: false`

---

Need help? Check VS Code Python debugging docs:
https://code.visualstudio.com/docs/python/debugging

