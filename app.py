import webview
import threading
from flask import Flask, render_template, request, Response, jsonify
import pyautogui
from pynput.keyboard import Controller, Key
import time
import json
import os

app = Flask(__name__)

# Global state
typing_state = {
    'is_typing': False,
    'is_paused': False
}

# Initialize keyboard controller
keyboard = Controller()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start-typing', methods=['POST'])
def start_typing():
    data = request.json
    text = data.get('text', '')
    speed = int(data.get('speed', 100))
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    def generate():
        global typing_state
        typing_state['is_typing'] = True
        typing_state['is_paused'] = False
        
        # Calculate delay
        wps = float(speed)
        if wps < 1:
            wps = 1
        
        if wps >= 500:
            delay = 0.000000001
        else:
            chars_per_second = wps * 6.0
            delay = 1.0 / chars_per_second
        
        # Type each character using pynput
        for i, char in enumerate(text):
            if not typing_state['is_typing']:
                break
            
            # Handle pause
            while typing_state['is_paused'] and typing_state['is_typing']:
                time.sleep(0.1)
            
            if not typing_state['is_typing']:
                break
            
            # Type character
            if char == '\n':
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            elif char == '\t':
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            elif char == ' ':
                keyboard.press(Key.space)
                keyboard.release(Key.space)
            else:
                try:
                    keyboard.type(char)
                except:
                    print(f"Could not type: {char}")
            
            time.sleep(delay)
            
            # Send progress update
            yield json.dumps({
                'index': i,
                'char': char,
                'total': len(text)
            }) + '\n'
        
        typing_state['is_typing'] = False
    
    return Response(generate(), mimetype='application/json')

@app.route('/api/toggle-pause', methods=['POST'])
def toggle_pause():
    global typing_state
    typing_state['is_paused'] = not typing_state['is_paused']
    return jsonify({'paused': typing_state['is_paused']})

@app.route('/api/stop-typing', methods=['POST'])
def stop_typing():
    global typing_state
    typing_state['is_typing'] = False
    typing_state['is_paused'] = False
    return jsonify({'stopped': True})

@app.route('/api/version', methods=['GET'])
def get_version():
    """Return current version information"""
    try:
        with open('version.json', 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        return jsonify(version_data)
    except:
        return jsonify({
            'current_version': '2.0.0',
            'version_name': 'Material UI Edition'
        })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Load user settings from file"""
    settings_file = 'user_settings.json'
    default_settings = {
        'darkMode': False,
        'speed': 100,
        'lastText': ''
    }
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        except:
            return jsonify(default_settings)
    else:
        return jsonify(default_settings)

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Save user settings to file"""
    settings_file = 'user_settings.json'
    
    try:
        data = request.json
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def check_version():
    """Check if the app version is up to date"""
    import os
    
    if not os.path.exists('version.json'):
        print("WARNING: version.json not found. Creating default version file...")
        default_version = {
            "current_version": "2.0.0",
            "version_name": "Material UI Edition",
            "release_date": "2025-12-24"
        }
        with open('version.json', 'w', encoding='utf-8') as f:
            json.dump(default_version, f, indent=4)
        return True
    
    try:
        with open('version.json', 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        current_version = version_data.get('current_version', '0.0.0')
        
        # Expected version
        expected_version = "2.0.0"
        
        if current_version != expected_version:
            print(f"\nVERSION MISMATCH!")
            print(f"Current version: {current_version}")
            print(f"Expected version: {expected_version}")
            print(f"\nPlease update TypingBot to version {expected_version}")
            print("Download the latest version and replace the old files.\n")
            
            # Show GUI dialog
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            result = messagebox.askokcancel(
                "Update Required",
                f"TypingBot version mismatch!\n\n"
                f"Current: {current_version}\n"
                f"Required: {expected_version}\n\n"
                f"Please update to the latest version.\n\n"
                f"Click OK to exit and update, or Cancel to continue anyway (not recommended)."
            )
            
            root.destroy()
            
            if result:  # User clicked OK to exit
                return False
            else:  # User clicked Cancel to continue
                print("WARNING: Continuing with outdated version. This may cause issues.\n")
                return True
        
        print(f"TypingBot v{current_version} - {version_data.get('version_name', 'Material UI Edition')}")
        return True
        
    except Exception as e:
        print(f"Error checking version: {e}")
        return True

def start_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    import json
    import os
    import sys
    
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Check version before starting
    if not check_version():
        print("Application terminated due to version mismatch.")
        sys.exit(1)
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Load saved window settings
    config_file = 'window_config.json'
    default_config = {'width': 600, 'height': 700, 'x': None, 'y': None}
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            config = default_config
    else:
        config = default_config
    
    print("Opening floating window...")
    
    # Create desktop window with Material UI
    window = webview.create_window(
        'TypingBot v2.0 - Bypass Text Pasting',
        'http://localhost:5000',
        width=config['width'],
        height=config['height'],
        x=config.get('x'),
        y=config.get('y'),
        resizable=True,
        on_top=True  # Always on top
    )
    
    def save_window_pos():
        # Save window position and size on close
        try:
            config = {
                'width': window.width,
                'height': window.height,
                'x': window.x,
                'y': window.y
            }
            with open(config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    window.events.closed += save_window_pos
    
    webview.start()

