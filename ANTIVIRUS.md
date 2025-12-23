# Antivirus False Positive Prevention

This file explains how to prevent antivirus false positives for TypingBot.exe

## Why Antivirus Software Flags PyInstaller Exe Files

PyInstaller bundles Python apps into standalone executables. Some antivirus software may flag these as suspicious because:

1. **Self-extracting behavior**: PyInstaller unpacks itself at runtime
2. **Keyboard automation**: Our app uses pynput for typing simulation
3. **Unsigned executables**: We haven't digitally signed the exe

## Solutions to Prevent False Positives

### For Developers (Building the Exe)

1. **Add Antivirus Exclusion** (Before building):
   ```powershell
   # Add folder to Windows Defender exclusion list
   Add-MpPreference -ExclusionPath "c:\Users\jitus\Desktop\My Apps\Typing\typing-bot-bypass-paste\dist"
   ```

2. **Digital Code Signing** (Optional but recommended):
   - Purchase a code signing certificate from trusted CA
   - Sign the exe using `signtool.exe`
   - Note: This costs money but prevents most false positives

3. **UPX Compression** (Alternative):
   ```bash
   # Install UPX
   # Then rebuild with --upx-dir flag
   pyinstaller --upx-dir=path/to/upx ...
   ```

### For End Users (Running the Exe)

1. **Windows Defender SmartScreen**:
   - If you see "Windows protected your PC"
   - Click "More info"
   - Click "Run anyway"

2. **Add to Exclusions**:
   ```powershell
   # Run PowerShell as Administrator
   Add-MpPreference -ExclusionPath "path\to\TypingBot.exe"
   ```

3. **Submit to Microsoft**:
   - If flagged as malware, submit as false positive:
   - https://www.microsoft.com/en-us/wdsi/filesubmission

## Build Verification

After building, verify the exe is clean:

1. **VirusTotal Scan**:
   - Upload to https://www.virustotal.com
   - Check detection rate (should be 0/70 or very low)

2. **Local Scan**:
   ```powershell
   # Scan with Windows Defender
   & "C:\Program Files\Windows Defender\MpCmdRun.exe" -Scan -ScanType 3 -File "dist\TypingBot.exe"
   ```

## What TypingBot Does (Transparency)

TypingBot is NOT malware. Here's what it does:

✅ **DOES**:
- Types text character by character using pynput
- Saves user settings to JSON files
- Creates a local web server (Flask) for UI
- Displays a desktop window (pywebview)

❌ **DOES NOT**:
- Access internet (except localhost for UI)
- Read files outside its directory
- Steal passwords or personal data
- Modify system settings
- Run in background without user knowledge

## Source Code Transparency

The complete source code is available on GitHub. Users can:
- Review all code before running
- Build from source themselves
- Report security concerns via GitHub Issues

**GitHub Repository**: https://github.com/AprajitSarkar/typing-bot-bypass-paste
