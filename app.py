import webview
import threading
from flask import Flask, render_template, request, Response, jsonify
import pyautogui
from pynput.keyboard import Controller, Key
import time
import json
import os

app = Flask(__name__)

# Embedded version info (prevents manual editing after exe build)
APP_VERSION = "2.0.1"
APP_VERSION_NAME = "Material UI Edition - Dark Mode Default"
APP_RELEASE_DATE = "2025-12-24"

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
    """Return current version information (embedded, not from file)"""
    return jsonify({
        'current_version': APP_VERSION,
        'version_name': APP_VERSION_NAME,
        'release_date': APP_RELEASE_DATE,
        'features': [
            'Bangla Language Support',
            'Material Design 3 UI',
            'Dark Mode (Default)',
            'Settings Persistence',
            'Live Text Highlighting',
            'Clipboard Protection'
        ]
    })

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Load user settings from file"""
    settings_file = 'user_settings.json'
    default_settings = {
        'darkMode': True,  # Dark mode enabled by default
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
    """Version info is now embedded in code - always returns True"""
    print(f"TypingBot v{APP_VERSION} - {APP_VERSION_NAME}")
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
        f'TypingBot v{APP_VERSION} - Bypass Text Pasting',
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

