import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
import webbrowser

class RoundedButton(tk.Canvas):
    """Custom rounded button widget"""
    def __init__(self, parent, text, command, bg_color, fg_color, hover_color, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.text = text
        
        self.config(bg=parent['bg'])
        self.bind('<Button-1>', self.on_click)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
        # Initial draw
        self.draw_button(self.bg_color)
        
        # Schedule a redraw after widget is fully displayed to fix text centering
        self.after(10, lambda: self.draw_button(self.bg_color))
        
    def draw_button(self, color):
        self.delete('all')
        # Get actual canvas dimensions
        self.update_idletasks()
        width = self.winfo_width() if self.winfo_width() > 1 else 100
        height = self.winfo_height() if self.winfo_height() > 1 else 40
        radius = 18
        
        # Draw rounded rectangle
        self.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill=color, outline='')
        self.create_arc(width-radius*2, 0, width, radius*2, start=0, extent=90, fill=color, outline='')
        self.create_arc(0, height-radius*2, radius*2, height, start=180, extent=90, fill=color, outline='')
        self.create_arc(width-radius*2, height-radius*2, width, height, start=270, extent=90, fill=color, outline='')
        self.create_rectangle(radius, 0, width-radius, height, fill=color, outline='')
        self.create_rectangle(0, radius, width, height-radius, fill=color, outline='')
        
        # Draw text centered
        self.create_text(width/2, height/2, text=self.text, fill=self.fg_color, font=('Segoe UI', 10, 'bold'), anchor='center')
        
    def on_click(self, event):
        if self.command:
            self.command()
            
    def on_enter(self, event):
        self.draw_button(self.hover_color)
        
    def on_leave(self, event):
        self.draw_button(self.bg_color)

class TypingPreview(tk.Frame):
    """Live typing preview widget showing past, current, and upcoming characters"""
    def __init__(self, parent, colors, **kwargs):
        super().__init__(parent, bg=colors['surface_variant'], **kwargs)
        self.colors = colors
        
        # Create labels for preview
        preview_container = tk.Frame(self, bg=colors['surface_variant'])
        preview_container.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Past characters (medium grey)
        self.past_label = tk.Label(preview_container, text="", 
                                   bg=colors['surface_variant'], 
                                   fg='#757575',  # Medium grey
                                   font=('Consolas', 11))
        self.past_label.pack(side='left')
        
        # Current character (bright green)
        self.current_label = tk.Label(preview_container, text="",
                                      bg=colors['surface_variant'],
                                      fg='#66BB6A',  # Bright green
                                      font=('Consolas', 13, 'bold'))
        self.current_label.pack(side='left', padx=2)
        
        # Upcoming characters (bright yellow/orange)
        self.upcoming_label = tk.Label(preview_container, text="",
                                      bg=colors['surface_variant'],
                                      fg='#FFA726',  # Bright orange
                                      font=('Consolas', 11))
        self.upcoming_label.pack(side='left')
        
    def update_preview(self, text, current_index):
        """Update the preview with current typing position"""
        if not text or current_index < 0:
            self.past_label.config(text="")
            self.current_label.config(text="")
            self.upcoming_label.config(text="")
            return
        
        # Get past character (1 char before current)
        past = text[current_index-1] if current_index > 0 else ""
        if past == '\n':
            past = "↵"
        elif past == '\t':
            past = "→"
        
        # Get current character
        current = text[current_index] if current_index < len(text) else ""
        if current == '\n':
            current = "↵"
        elif current == '\t':
            current = "→"
        elif current == ' ':
            current = "␣"
        
        # Get next 3 characters
        upcoming = text[current_index+1:current_index+4] if current_index < len(text) else ""
        upcoming = upcoming.replace('\n', '↵').replace('\t', '→').replace(' ', '␣')
        
        self.past_label.config(text=past)
        self.current_label.config(text=current)
        self.upcoming_label.config(text=upcoming)
        
    def clear_preview(self):
        """Clear all preview labels"""
        self.past_label.config(text="")
        self.current_label.config(text="")
        self.upcoming_label.config(text="")

class TimeRemaining(tk.Frame):
    """Widget showing estimated time remaining to complete typing"""
    def __init__(self, parent, colors, **kwargs):
        super().__init__(parent, bg=colors['surface_variant'], **kwargs)
        self.colors = colors
        
        # Time display label - centered with larger font
        self.time_label = tk.Label(self, text="--m--s",
                                   bg=colors['surface_variant'],
                                   fg=colors['on_surface'],
                                   font=('Segoe UI', 11, 'bold'),
                                   anchor='center', justify='center')
        self.time_label.pack(expand=True, fill='both')
        
    def update_time(self, seconds_remaining):
        """Update the time display"""
        minutes = int(seconds_remaining // 60)
        secs = int(seconds_remaining % 60)
        self.time_label.config(text=f"{minutes:02d}m{secs:02d}s")
        
    def clear_time(self):
        """Clear the time display"""
        self.time_label.config(text="--m--s")

class FloatingTypingBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TypingBot - Bypass Text Pasting")
        self.root.attributes('-topmost', True)
        self.root.resizable(True, True)  # Make window resizable
        
        # Material 3 Colors
        self.colors = {
            'primary': '#6750A4',
            'primary_container': '#EADDFF',
            'secondary': '#625B71',
            'tertiary': '#7D5260',
            'surface': '#FEF7FF',
            'surface_variant': '#E7E0EC',
            'background': '#FEF7FF',
            'error': '#B3261E',
            'on_primary': '#FFFFFF',
            'on_surface': '#1C1B1F',
            'outline': '#79747E',
            'success': '#2E7D32'
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # Variables
        self.typing_speed = tk.DoubleVar(value=100.0)
        self.is_typing = False
        self.is_paused = False
        self.typing_thread = None
        self.countdown_window = None
        self.current_char_index = 0
        self.typing_text = ""
        
        # Make window draggable
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Bind ESC key to stop typing
        self.root.bind('<Escape>', self.on_escape_key)
        
        # Set minimum window size
        self.root.minsize(400, 450)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['surface'])
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title bar for dragging
        title_bar = tk.Frame(main_frame, bg=self.colors['primary'], cursor='fleur', height=50)
        title_bar.pack(fill='x', pady=(0, 10))
        title_bar.pack_propagate(False)
        title_bar.bind('<Button-1>', self.start_drag)
        title_bar.bind('<B1-Motion>', self.on_drag)
        
        # Title
        title_label = tk.Label(title_bar, text="⌨️ TypingBot", 
                              bg=self.colors['primary'], fg=self.colors['on_primary'],
                              font=('Segoe UI', 14, 'bold'))
        title_label.pack(side='left', padx=15, pady=10)
        
        # Close button
        close_btn = tk.Button(title_bar, text='✕', bg=self.colors['error'], 
                             fg='white', font=('Segoe UI', 14, 'bold'), 
                             bd=0, command=self.root.destroy, cursor='hand2')
        close_btn.pack(side='right', padx=5, pady=5, ipadx=10, ipady=2)
        
        # Text input section
        tk.Label(main_frame, text="Text to Type:", bg=self.colors['surface'],
                fg=self.colors['on_surface'], font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 5))
        
        self.text_entry = tk.Text(main_frame, height=4, wrap=tk.WORD,
                                 bg=self.colors['surface_variant'], fg=self.colors['on_surface'],
                                 font=('Segoe UI', 10), bd=0, relief='flat')
        self.text_entry.pack(fill='both', expand=True, pady=(0, 10))
        self.text_entry.bind('<Return>', lambda e: self.start_countdown())
        self.text_entry.bind('<KeyRelease>', self.update_paste_clear_button)
        
        # Configure text tags for live highlighting
        self.text_entry.tag_configure('typed', foreground='#9E9E9E')  # Light grey for typed text
        self.text_entry.tag_configure('current', foreground='#4CAF50', font=('Segoe UI', 10, 'bold'))  # Bright green for current
        self.text_entry.tag_configure('upcoming', foreground='#FFA726')  # Orange/yellow for upcoming
        
        # Speed control
        speed_frame = tk.Frame(main_frame, bg=self.colors['surface'])
        speed_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(speed_frame, text="Speed:", bg=self.colors['surface'],
                fg=self.colors['on_surface'], font=('Segoe UI', 10, 'bold')).pack(side='left')
        
        speed_scale = ttk.Scale(speed_frame, from_=1, to=500, orient='horizontal',
                               variable=self.typing_speed, length=150)
        speed_scale.pack(side='left', padx=10, fill='x', expand=True)
        
        speed_display = tk.Label(speed_frame, text="",
                                bg=self.colors['primary_container'], 
                                fg=self.colors['primary'],
                                font=('Segoe UI', 10, 'bold'), width=5, padx=5, pady=2)
        speed_display.pack(side='left', padx=5)
        
        # Update speed display when slider changes
        def update_speed_display(*args):
            speed_display.config(text=f"{int(self.typing_speed.get())}")
        self.typing_speed.trace('w', update_speed_display)
        update_speed_display()  # Set initial value
        
        tk.Label(speed_frame, text="WPS", bg=self.colors['surface'],
                fg=self.colors['outline'], font=('Segoe UI', 9)).pack(side='left')
        
        # Button container with live preview
        control_frame = tk.Frame(main_frame, bg=self.colors['surface'])
        control_frame.pack(fill='x', pady=(0, 10))
        
        # Left buttons (Paste + Start)
        left_buttons = tk.Frame(control_frame, bg=self.colors['surface'])
        left_buttons.pack(side='left', fill='x', expand=True)
        
        self.paste_clear_btn = RoundedButton(left_buttons, "📋 Paste", self.paste_or_clear,
                                            self.colors['secondary'], self.colors['on_primary'],
                                            '#524963', width=80, height=40)
        self.paste_clear_btn.pack(side='left', padx=(0, 5))
        self.paste_clear_btn.is_paste = True
        
        
        self.start_btn = RoundedButton(left_buttons, "▶ Start", self.start_countdown,
                                      self.colors['primary'], self.colors['on_primary'],
                                      '#5046A3', width=70, height=40)
        self.start_btn.pack(side='left', padx=(0, 5))
        
        # Pause button
        self.pause_btn = RoundedButton(left_buttons, "⏸ Pause", self.toggle_pause,
                                       self.colors['tertiary'], self.colors['on_primary'],
                                       '#6A4653', width=70, height=40)
        self.pause_btn.pack(side='left')
        self.pause_btn.config(state='disabled')
        
        # Center: Live typing preview
        self.preview_widget = TypingPreview(control_frame, self.colors, height=40, width=130)
        self.preview_widget.pack(side='left', padx=5, fill='x', expand=True)
        
        # Right button (Stop)
        self.stop_btn = RoundedButton(control_frame, "⏹ Stop", self.stop_typing,
                                     self.colors['error'], 'white',
                                     '#8B0000', width=80, height=40)
        self.stop_btn.pack(side='right')
        self.stop_btn.config(state='disabled')
        
        # Instructions
        instructions = tk.Label(main_frame,
                               text="📝 Type/Paste text → Set speed → Press Start → Position cursor",
                               bg=self.colors['primary_container'], 
                               fg=self.colors['on_surface'],
                               font=('Segoe UI', 9), padx=10, pady=8)
        instructions.pack(fill='x', pady=(0, 10))
        
        # Developer credits
        credits_frame = tk.Frame(main_frame, bg=self.colors['surface'])
        credits_frame.pack(fill='x')
        
        tk.Label(credits_frame, text="Developed by", bg=self.colors['surface'],
                fg=self.colors['outline'], font=('Segoe UI', 8)).pack(side='left')
        
        insta_link = tk.Label(credits_frame, text="Aprajit", 
                             bg=self.colors['surface'], fg=self.colors['primary'],
                             font=('Segoe UI', 8, 'bold'), cursor='hand2')
        insta_link.pack(side='left')
        insta_link.bind('<Button-1>', lambda e: webbrowser.open('https://instagram.com/jitusarkar21'))
        
        tk.Label(credits_frame, text=" | ", bg=self.colors['surface'],
                fg=self.colors['outline'], font=('Segoe UI', 8)).pack(side='left')
        
        github_link = tk.Label(credits_frame, text="GitHub: AprajitSarkar", 
                              bg=self.colors['surface'], fg=self.colors['primary'],
                              font=('Segoe UI', 8, 'bold'), cursor='hand2')
        github_link.pack(side='left')
        github_link.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/AprajitSarkar/typing-bot-bypass-paste'))
        
    def start_drag(self, event):
        self.dragging = True
        self.offset_x = event.x
        self.offset_y = event.y
    
    def on_drag(self, event):
        if self.dragging:
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f'+{x}+{y}')
    
    def on_escape_key(self, event):
        if self.is_typing:
            self.is_typing = False
            self.show_notification("⏹ Typing stopped (ESC)", self.colors['error'])
    
    def update_paste_clear_button(self, event=None):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            if self.paste_clear_btn.is_paste:
                self.paste_clear_btn.is_paste = False
                self.paste_clear_btn.text = "🗑️ Clear"
                self.paste_clear_btn.draw_button(self.paste_clear_btn.bg_color)
        else:
            if not self.paste_clear_btn.is_paste:
                self.paste_clear_btn.is_paste = True
                self.paste_clear_btn.text = "📋 Paste"
                self.paste_clear_btn.draw_button(self.paste_clear_btn.bg_color)
    
    def paste_or_clear(self):
        if self.paste_clear_btn.is_paste:
            self.paste_from_clipboard()
        else:
            self.clear_text()
    
    def paste_from_clipboard(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert("1.0", clipboard_text)
            self.update_paste_clear_button()
            self.show_notification("📋 Pasted from clipboard", self.colors['success'])
        except:
            self.show_notification("⚠️ Clipboard is empty", self.colors['error'])
    
    def clear_text(self):
        self.text_entry.delete("1.0", tk.END)
        self.update_paste_clear_button()
        self.show_notification("🗑️ Text cleared", self.colors['success'])
    
    def update_text_highlighting(self, current_index):
        """Update text field colors to show typing progress"""
        # Remove all existing tags
        self.text_entry.tag_remove('typed', '1.0', tk.END)
        self.text_entry.tag_remove('current', '1.0', tk.END)
        self.text_entry.tag_remove('upcoming', '1.0', tk.END)
        
        if current_index < 0:
            return
        
        # Apply typed tag (grey) to all text before current position
        if current_index > 0:
            self.text_entry.tag_add('typed', '1.0', f'1.{current_index}')
        
        # Apply current tag (bright green) to current character
        text_length = len(self.text_entry.get('1.0', tk.END).strip())
        if current_index < text_length:
            self.text_entry.tag_add('current', f'1.{current_index}', f'1.{current_index + 1}')
        
        # Apply upcoming tag (yellow) to remaining text
        if current_index + 1 < text_length:
            self.text_entry.tag_add('upcoming', f'1.{current_index + 1}', tk.END)
    
    def clear_text_highlighting(self):
        """Clear all text highlighting"""
        self.text_entry.tag_remove('typed', '1.0', tk.END)
        self.text_entry.tag_remove('current', '1.0', tk.END)
        self.text_entry.tag_remove('upcoming', '1.0', tk.END)
    
    def start_countdown(self):
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        self.text_entry.config(state='disabled')
        threading.Thread(target=self.countdown_and_type, daemon=True).start()
        
    def countdown_and_type(self):
        self.root.withdraw()
        self.create_countdown_window()
        
        # Get text before typing
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            self.show_notification("⚠️ No text entered", self.colors['error'])
            self.cleanup_countdown()
            self.root.deiconify()
            self.root.after(0, self.typing_finished)
            return
        
        for i in range(3, 0, -1):
            if not self.is_typing:
                self.update_countdown(i)
                time.sleep(1)
            else:
                break
                
        self.cleanup_countdown()
        self.root.deiconify()
        
        self.is_typing = True
        self.typing_text = text
        self.current_char_index = 0
        x, y = pyautogui.position()
        self.typing_thread = threading.Thread(target=self.type_text, args=(text, x, y), daemon=True)
        self.typing_thread.start()
        
    def create_countdown_window(self):
        self.countdown_window = tk.Toplevel(self.root)
        self.countdown_window.attributes('-topmost', True)
        self.countdown_window.overrideredirect(True)
        self.countdown_window.attributes('-alpha', 0.95)
        self.countdown_window.configure(bg=self.colors['primary'])
        
        self.countdown_window.update_idletasks()
        width = 250
        height = 120
        screen_width = self.countdown_window.winfo_screenwidth()
        screen_height = self.countdown_window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = screen_height - height - 100
        self.countdown_window.geometry(f'{width}x{height}+{x}+{y}')
        
        frame = tk.Frame(self.countdown_window, bg=self.colors['primary'])
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(frame, text="Position your cursor", bg=self.colors['primary'],
                fg=self.colors['on_primary'], font=('Segoe UI', 11)).pack(pady=(10, 5))
        
        self.countdown_label = tk.Label(frame, text="3", bg=self.colors['primary'],
                                       fg=self.colors['on_primary'], 
                                       font=('Segoe UI', 36, 'bold'))
        self.countdown_label.pack(expand=True)
        
    def update_countdown(self, count):
        if self.countdown_window:
            self.countdown_label.config(text=str(count))
            self.countdown_window.update()
            
    def cleanup_countdown(self):
        if self.countdown_window:
            self.countdown_window.destroy()
            self.countdown_window = None
        
    def show_notification(self, message, color=None):
        if color is None:
            color = self.colors['success']
            
        popup = tk.Toplevel(self.root)
        popup.attributes('-topmost', True)
        popup.overrideredirect(True)
        popup.attributes('-alpha', 0.95)
        popup.configure(bg=color)
        
        label = tk.Label(popup, text=message, bg=color, fg='white',
                        font=('Segoe UI', 12, 'bold'), padx=30, pady=15)
        label.pack()
        
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = screen_height - height - 100
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        popup.after(2000, popup.destroy)
    
    def type_text(self, text, x, y):
        pyautogui.click(x, y)
        time.sleep(0.1)
        
        # Get current typing speed (Words Per Second)
        wps = float(self.typing_speed.get())
        
        # Ensure minimum speed of 1 WPS
        if wps < 1:
            wps = 1
        
        # Calculate delay per character
        if wps >= 500:
            # Maximum speed: ultra-fast with nearly zero delay
            delay = 0.000000001  # 1 nanosecond - essentially instant
        else:
            # Normal speed calculation
            # 1 word = ~6 characters (5 letters + 1 space)
            chars_per_second = wps * 6.0
            delay = 1.0 / chars_per_second
        
        for i, char in enumerate(text):
            if not self.is_typing:
                self.root.after(0, lambda: self.show_notification("⏹ Typing stopped"))
                break
            
            # Wait while paused
            while self.is_paused and self.is_typing:
                time.sleep(0.1)
            
            if not self.is_typing:
                break
            
            # Update text highlighting in real-time
            self.current_char_index = i
            self.root.after(0, lambda idx=i: (
                self.update_text_highlighting(idx),
                self.preview_widget.update_preview(self.typing_text, idx)
            ))
            
            if char == '\n':
                pyautogui.press('enter')
            elif char == '\t':
                pyautogui.press('tab')
            elif char == ' ':
                pyautogui.press('space')
            else:
                pyautogui.typewrite(char, interval=0)
            
            time.sleep(delay)
        
        # Clear highlighting and preview when done
        self.root.after(0, self.clear_text_highlighting)
        self.root.after(0, self.preview_widget.clear_preview)
        self.root.after(0, self.typing_finished)
        
    def toggle_pause(self):
        """Toggle pause/resume during typing"""
        if not self.is_typing:
            return
        
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            # Paused
            self.pause_btn.text = "▶ Resume"
            self.pause_btn.draw_button(self.pause_btn.bg_color)
            self.show_notification("⏸ Typing paused", self.colors['primary'])
        else:
            # Resumed
            self.pause_btn.text = "⏸ Pause"
            self.pause_btn.draw_button(self.pause_btn.bg_color)
            self.show_notification("▶ Typing resumed", self.colors['success'])
    
    def stop_typing(self):
        self.is_typing = False
        if self.typing_thread and self.typing_thread.is_alive():
            self.typing_thread.join(timeout=1)
        self.typing_finished()
        
    def typing_finished(self):
        self.is_typing = False
        self.is_paused = False
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
        self.pause_btn.text = "⏸ Pause"
        self.pause_btn.draw_button(self.pause_btn.bg_color)
        self.stop_btn.config(state='disabled')
        self.text_entry.config(state='normal')
        self.clear_text_highlighting()
        self.preview_widget.clear_preview()
        self.cleanup_countdown()
        
    def run(self):
        # Set initial window size
        self.root.geometry('500x550')
        # Position at top-right
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - 520
        y = 20
        self.root.geometry(f'+{x}+{y}')
        self.root.mainloop()

if __name__ == "__main__":
    app = FloatingTypingBot()
    app.run()