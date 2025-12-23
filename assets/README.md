# TypingBot Releases

This folder contains pre-built, standalone executables for TypingBot.

## Latest Release: v2.0.1

**File**: `TypingBot_v2.0.1.exe` (65.7 MB)
**Release Date**: 2025-12-24

### What's New in v2.0.1
- ✅ **Dark Mode by Default** - Enhanced user experience
- ✅ **Non-Editable Version** - Version embedded in code (prevents tampering)
- ✅ **Full Feature Set**:
  - Bangla language support (automatic detection)
  - Material Design 3 UI
  - Settings persistence (dark mode, speed, last text)
  - Live text highlighting
  - Clipboard protection
  - Window position memory

### Download & Install

1. **Download**: Click on `TypingBot_v2.0.1.exe`
2. **Antivirus Warning**: See [ANTIVIRUS.md](../ANTIVIRUS.md) if flagged
3. **Run**: Double-click to launch
4. **No Installation Required**: Fully portable

### System Requirements
- Windows 7/8/10/11
- 100 MB free disk space
- No Python installation needed

### First Run
If Windows SmartScreen appears:
1. Click "More info"
2. Click "Run anyway"

### Antivirus False Positives
Some antivirus software may flag PyInstaller executables. TypingBot is **NOT** malware.

**Why it happens**:
- PyInstaller self-extracts at runtime
- Keyboard automation tools are often flagged
- Unsigned executable

**Solution**:
- Add to antivirus exclusions
- Scan on [VirusTotal.com](https://www.virustotal.com)
- Review full source code on GitHub

**Full guide**: [ANTIVIRUS.md](../ANTIVIRUS.md)

### Version History

| Version | Release Date | Changes |
|---------|-------------|---------|
| v2.0.1 | 2025-12-24 | Dark mode default, embedded version |
| v2.0.0 | 2025-12-24 | Settings persistence, version control |
| v1.0.0 | Initial | Basic typing functionality |

### Support

- **Issues**: [GitHub Issues](https://github.com/AprajitSarkar/typing-bot-bypass-paste/issues)
- **Source**: [GitHub Repository](https://github.com/AprajitSarkar/typing-bot-bypass-paste)
- **Developer**: [@jitusarkar21](https://instagram.com/jitusarkar21)

### Building from Source

If you prefer to build the exe yourself:

```bash
# Clone repository
git clone https://github.com/AprajitSarkar/typing-bot-bypass-paste.git
cd typing-bot-bypass-paste

# Install dependencies
pip install -r requirements.txt

# Build exe
python -m PyInstaller --clean --onefile --windowed --name "TypingBot_v2.0.1" --add-data "templates;templates" --add-data "static;static" --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32 app.py
```

The exe will be in `dist/TypingBot_v2.0.1.exe`
