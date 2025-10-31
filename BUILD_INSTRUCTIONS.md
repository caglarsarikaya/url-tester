# Build Instructions for Executable

## Quick Build

### Windows
```bash
build.bat
```

### Linux/Mac
```bash
chmod +x build.sh
./build.sh
```

---

## Size Optimization

The `build_config.spec` already includes optimizations:

### ✅ Included by Default
- **Strip debug symbols** (`strip=True`)
- **One-file bundle** (single executable)
- **Excludes unnecessary modules** (tkinter, numpy, pandas, etc.)


---


## Troubleshooting

### "Module not found" error
Add missing module to `hiddenimports` in `build_config.spec`:
```python
hiddenimports=[
    'missing_module_name',
],
```

## Build Configuration

The `build_config.spec` file controls:
- **What to include** (source files, data files)
- **What to exclude** (unnecessary modules)
- **Compression** (UPX, strip)
- **Output name** and format

Edit `build_config.spec` to customize the build.

---

## Distributing

After building, distribute:
- `url_tester.exe` (or `url_tester`)
- `urls_to_test.xlsx`
- `sitemaps.xlsx`

The executable is **standalone** - no Python installation needed on target machine!

