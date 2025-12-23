// Material Design 3 TypingBot - Frontend Logic
class TypingBot {
    constructor() {
        this.isDarkMode = false;
        this.isTyping = false;
        this.isPaused = false;
        this.currentText = '';
        this.typingSpeed = 100;

        this.initializeElements();
        this.attachEventListeners();
        this.loadVersion(); // Load version info
    }

    initializeElements() {
        // Form elements
        this.textInput = document.getElementById('textInput');
        this.speedSlider = document.getElementById('speedSlider');
        this.speedValue = document.getElementById('speedValue');

        // Buttons
        this.pasteBtn = document.getElementById('pasteBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.darkModeToggle = document.getElementById('darkModeToggle');

        // Preview elements
        this.livePreview = document.getElementById('livePreview');
        this.prevChar = document.getElementById('prevChar');
        this.currentChar = document.getElementById('currentChar');
        this.nextChars = document.getElementById('nextChars');
        this.progressFill = document.getElementById('progressFill');

        // Modal elements
        this.countdownModal = document.getElementById('countdownModal');
        this.countdownNumber = document.getElementById('countdownNumber');
        this.notificationToast = document.getElementById('notificationToast');
    }

    attachEventListeners() {
        // Speed control
        this.speedSlider.addEventListener('input', () => {
            this.typingSpeed = this.speedSlider.value;
            this.speedValue.textContent = this.typingSpeed;
            this.saveSettings();
        });

        // Dark mode toggle
        this.darkModeToggle.addEventListener('click', () => this.toggleDarkMode());

        // Input buttons
        this.pasteBtn.addEventListener('click', () => this.pasteFromClipboard());
        this.clearBtn.addEventListener('click', () => this.clearText());

        // Control buttons
        this.startBtn.addEventListener('click', () => this.startTyping());
        this.pauseBtn.addEventListener('click', () => this.togglePause());
        this.stopBtn.addEventListener('click', () => this.stopTyping());

        // Save text on change
        this.textInput.addEventListener('input', () => {
            this.saveSettings();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isTyping) {
                this.stopTyping();
            }
        });
    }

    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        document.body.classList.toggle('dark-mode');

        const icon = this.darkModeToggle.querySelector('.material-symbols-outlined');
        icon.textContent = this.isDarkMode ? 'light_mode' : 'dark_mode';

        this.saveSettings();
        this.showNotification(this.isDarkMode ? '🌙 Dark mode enabled' : '☀️ Light mode enabled');
        this.saveSettings(); // Save to file
    }

    async loadSettings() {
        try {
            const response = await fetch('/api/settings');
            const settings = await response.json();

            this.typingSpeed = settings.speed || 100;
            this.isDarkMode = settings.darkMode || false;
            this.currentText = settings.lastText || '';
        } catch (error) {
            console.error('Failed to load settings:', error);
            // Use defaults
            this.typingSpeed = 100;
            this.isDarkMode = false;
            this.currentText = '';
        }
    }

    async saveSettings() {
        const settings = {
            speed: this.typingSpeed,
            darkMode: this.isDarkMode,
            lastText: this.textInput.value
        };

        try {
            await fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });
        } catch (error) {
            console.error('Failed to save settings:', error);
        }
    }

    applySettings() {
        this.speedSlider.value = this.typingSpeed;
        this.speedValue.textContent = this.typingSpeed;

        if (this.currentText) {
            this.textInput.value = this.currentText;
        }

        if (this.isDarkMode) {
            document.body.classList.add('dark-mode');
            const icon = this.darkModeToggle.querySelector('.material-symbols-outlined');
            icon.textContent = 'light_mode';
        }
    }

    saveSettings() {
        localStorage.setItem('typingSpeed', this.typingSpeed);
        localStorage.setItem('darkMode', this.isDarkMode);
        localStorage.setItem('lastText', this.textInput.value);
    }

    async pasteFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            this.textInput.value = text;
            this.saveSettings();
            this.showNotification('📋 Pasted from clipboard');
        } catch (err) {
            this.showNotification('⚠️ Cannot access clipboard', 'error');
        }
    }

    clearText() {
        this.textInput.value = '';
        this.saveSettings();
        this.showNotification('🗑️ Text cleared');
    }

    async startTyping() {
        const text = this.textInput.value.trim();

        if (!text) {
            this.showNotification('⚠️ Please enter some text', 'error');
            return;
        }

        this.currentText = text;
        await this.showCountdown();
        await this.performTyping();
    }

    async showCountdown() {
        return new Promise((resolve) => {
            this.countdownModal.style.display = 'flex';
            let count = 3;

            const countdown = setInterval(() => {
                this.countdownNumber.textContent = count;
                this.countdownNumber.style.animation = 'none';
                setTimeout(() => {
                    this.countdownNumber.style.animation = 'countdownPulse 1s ease-in-out';
                }, 10);

                count--;

                if (count < 0) {
                    clearInterval(countdown);
                    this.countdownModal.style.display = 'none';
                    resolve();
                }
            }, 1000);
        });
    }

    async performTyping() {
        this.isTyping = true;
        this.isPaused = false;

        // Update UI
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        this.stopBtn.disabled = false;
        this.textInput.disabled = true;
        this.livePreview.style.display = 'block';

        // Start streaming
        try {
            const response = await fetch('/api/start-typing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: this.currentText,
                    speed: this.typingSpeed
                }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                const lines = buffer.split('\n');
                buffer = lines.pop();

                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            this.updatePreview(data);
                        } catch (e) { }
                    }
                }
            }

            this.finishTyping();
        } catch (error) {
            this.showNotification('❌ Typing failed', 'error');
            this.finishTyping();
        }
    }

    updatePreview(data) {
        const { index, char, total } = data;

        // Update live preview
        this.prevChar.textContent = index > 0 ? this.currentText[index - 1] : '';
        this.currentChar.textContent = char || '';
        this.nextChars.textContent = this.currentText.substring(index + 1, index + 4);

        // Update progress
        const progress = ((index + 1) / total) * 100;
        this.progressFill.style.width = `${progress}%`;

        // Highlight text in input
        this.highlightTextInput(index);
    }

    highlightTextInput(currentIndex) {
        const text = this.currentText;
        const before = text.substring(0, currentIndex);
        const current = text[currentIndex] || '';
        const after = text.substring(currentIndex + 1);

        let overlay = document.getElementById('textOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'textOverlay';
            overlay.className = 'text-overlay';
            this.textInput.parentElement.appendChild(overlay);
            this.textInput.style.color = 'transparent';
            this.textInput.style.caretColor = '#66BB6A';
        }

        const beforeSpan = `<span style="color: #9E9E9E">${this.escapeHtml(before)}</span>`;
        const currentSpan = `<span style="color: #66BB6A; font-weight: bold">${this.escapeHtml(current)}</span>`;
        const afterSpan = `<span style="color: #FFA726">${this.escapeHtml(after)}</span>`;

        overlay.innerHTML = beforeSpan + currentSpan + afterSpan;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
    }

    clearInputHighlight() {
        const overlay = document.getElementById('textOverlay');
        if (overlay) overlay.remove();
        this.textInput.style.color = '';
        this.textInput.style.caretColor = '';
    }

    togglePause() {
        this.isPaused = !this.isPaused;

        if (this.isPaused) {
            this.pauseBtn.innerHTML = '<span class="material-symbols-outlined">play_arrow</span>Resume';
            this.showNotification('⏸ Typing paused');
        } else {
            this.pauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span>Pause';
            this.showNotification('▶ Typing resumed');
        }

        fetch('/api/toggle-pause', { method: 'POST' });
    }

    stopTyping() {
        this.isTyping = false;
        fetch('/api/stop-typing', { method: 'POST' });
        this.showNotification('⏹ Typing stopped');
        this.finishTyping();
    }

    finishTyping() {
        this.isTyping = false;
        this.isPaused = false;

        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
        this.stopBtn.disabled = true;
        this.textInput.disabled = false;
        this.livePreview.style.display = 'none';
        this.progressFill.style.width = '0%';

        this.clearInputHighlight();
        this.pauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span>Pause';
    }

    showNotification(message, type = 'success') {
        this.notificationToast.textContent = message;
        this.notificationToast.classList.add('show');

        if (type === 'error') {
            this.notificationToast.style.background = 'var(--md-sys-color-error)';
        } else {
            this.notificationToast.style.background = 'var(--md-sys-color-surface)';
        }

        setTimeout(() => {
            this.notificationToast.classList.remove('show');
        }, 3000);
    }

    async loadVersion() {
        try {
            const response = await fetch('/api/version');
            const data = await response.json();

            const versionText = document.getElementById('versionText');
            if (versionText && data.current_version) {
                versionText.textContent = `v${data.current_version}`;

                // Update window title if possible
                if (data.version_name) {
                    document.title = `TypingBot v${data.current_version} - ${data.version_name}`;
                }
            }
        } catch (error) {
            console.error('Failed to load version:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const app = new TypingBot();
    // Wait for settings to load before applying
    await app.loadSettings();
    app.applySettings();
});
