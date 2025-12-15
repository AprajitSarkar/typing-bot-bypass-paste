# TypingBot - Bypass Paste, Bypass Text Pasting

<div align="center">

![TypingBot](https://img.shields.io/badge/TypingBot-v1.0-6750A4?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Automate text typing with customizable speed - Perfect for bypassing paste restrictions**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots)

</div>

---

## 🌟 Features

- **⚡ Variable Typing Speed**: Adjust from 1 to 500 words per second (WPS)
- **🎨 Material 3 Design**: Modern, beautiful UI with rounded corners and smooth animations
- **🔄 Auto-Type**: Automated character-by-character typing to bypass paste restrictions
- **⏱️ Countdown Timer**: 3-second countdown to position your cursor
- **🛑 Stop Anytime**: Instantly stop typing with the stop button
- **📌 Always on Top**: Floating window stays visible while you work
- **🎯 Drag & Drop**: Draggable interface for easy positioning
- **📱 Lightweight**: Minimal resource usage, runs smoothly

## 🚀 Use Cases

- Bypass websites that disable paste functionality
- Automate form filling with natural typing speed
- Test typing-based applications
- Simulate human typing behavior
- Educational demonstrations
- Content entry automation

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Windows/Linux/macOS

### Step 1: Clone the Repository

```bash
git clone https://github.com/AprajitSarkar/typing-bot-bypass-paste.git
cd typing-bot-bypass-paste
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python floating_typing_bot.py
```

Or use the batch file (Windows):

```bash
run_bot.bat
```

### Step 4: Build Standalone EXE (Optional)

To create a standalone executable:

```bash
build.bat
```

This batch file will:
1. Check Python installation
2. Verify all dependencies
3. Install PyInstaller if needed
4. Build the EXE file

The EXE will be created in the `dist` folder as `TypingBot.exe`

## 📖 Usage

1. **Enter Text**: Type or paste the text you want to auto-type in the text field
2. **Set Speed**: Adjust the slider (1-500 WPS) to your desired typing speed
   - 1 WPS = Slow, human-like typing
   - 100 WPS = Fast typing (default)
   - 500 WPS = Ultra-fast typing
3. **Start Typing**: Press Enter or click "Start" button
4. **Position Cursor**: During the 3-second countdown, click where you want the text typed
5. **Auto-Type**: The bot will automatically type your text at the specified speed
6. **Stop Anytime**: Click the "Stop" button to interrupt typing

## 🎯 Speed Guide

| WPS | Characters/Second | Description |
|-----|-------------------|-------------|
| 1 | 6 | Very slow, deliberate typing |
| 10 | 60 | Slow, human-like speed |
| 50 | 300 | Moderate typing speed |
| 100 | 600 | Fast typing (default) |
| 200 | 1200 | Very fast typing |
| 500 | 3000 | Ultra-fast, maximum speed |

*Note: 1 word ≈ 6 characters (5 letters + 1 space)*

## 🖼️ Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)
*Modern Material 3 design with rounded corners*

### Countdown Timer
![Countdown](screenshots/countdown.png)
*Transparent countdown popup at bottom center*

## 🛠️ Technical Details

### Dependencies

```
pyautogui>=0.9.53
pillow>=8.3.2
pynput>=1.7.6
```

### How It Works

1. **Speed Calculation**: Converts WPS (Words Per Second) to character delay
   - Formula: `delay = 1.0 / (WPS × 6)`
2. **Character Typing**: Uses `pyautogui` for keyboard simulation
3. **Special Characters**: Handles newlines, tabs, and spaces correctly
4. **Thread Safety**: Runs typing in separate thread to keep UI responsive

## 🎨 Material 3 Design

The UI follows Google's Material 3 design guidelines:
- **Primary Color**: Purple (#6750A4)
- **Surface Color**: Light background (#FEF7FF)
- **Rounded Corners**: 18px radius on buttons and popups
- **Transparency**: 95% opacity on popups
- **Typography**: Segoe UI font family

## 🔧 Configuration

You can modify the typing behavior by editing the source code:

```python
# Default typing speed (WPS)
self.typing_speed = tk.DoubleVar(value=100.0)

# Speed range (min, max)
speed_scale = ttk.Scale(from_=1, to=500, ...)

# Countdown duration (seconds)
for i in range(3, 0, -1):  # Change 3 to desired countdown time
```

## 🐛 Troubleshooting

### Issue: Bot types too fast/slow
- **Solution**: Adjust the speed slider before starting

### Issue: Text doesn't appear
- **Solution**: Ensure the cursor is in an editable text field

### Issue: Special characters not working
- **Solution**: The bot handles most special characters, but some may require manual typing

### Issue: Window not on top
- **Solution**: The window is set to always stay on top by default

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Developed by Jitu Sarkar**

- 📷 Instagram: [@jitusarkar21](https://instagram.com/jitusarkar21)
- 🐙 GitHub: [@AprajitSarkar](https://github.com/AprajitSarkar)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐️!

## 🔑 Keywords

typingbot, bypass paste, bypass text pasting, auto typer, text automation, typing automation, paste bypass, form filler, keyboard automation, pyautogui, python typing bot, automated typing, typing simulator, text entry automation

---

<div align="center">

**Made with ❤️ by Jitu Sarkar**

[⬆ Back to Top](#typingbot---bypass-paste-bypass-text-pasting)

</div>