import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from googletrans import Translator
from gtts import gTTS
import playsound
import os

# Language map without country codes (flags removed)
LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese': 'zh-CN',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Portuguese': 'pt',
    'Bengali': 'bn',
    'Dutch': 'nl',
    'Turkish': 'tr',
    'Swedish': 'sv',
    'Danish': 'da',
    'Finnish': 'fi',
    'Norwegian': 'no',
    'Greek': 'el',
    'Urdu': 'ur'
}

translator = Translator()

def get_language_name(code):
    for name, lang_code in LANGUAGES.items():
        if lang_code == code:
            return name
    return "Unknown"

# The main application class
class MultiLinguaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Light and Dark mode colors
        self.light_bg = "#f0f0f0"
        self.light_fg = "#000000"
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#f0f0f0"
        self.is_dark = False

        self.title("\U0001F310 MultiLingua Translator")
        self.geometry("700x600")
        self.resizable(False, False)

        self.bg_color = self.light_bg
        self.fg_color = self.light_fg
        self.configure(bg=self.bg_color)

        self.create_widgets()
    
    def create_widgets(self):
        self.title_lbl = tk.Label(self, text="MultiLingua Translator", font=("Helvetica", 16, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.title_lbl.pack(pady=10)

        # Input label and text
        tk.Label(self, text="Enter text:", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor='w', padx=20)
        self.input_text = tk.Text(self, height=6, width=75, bg="white" if not self.is_dark else "#444", fg=self.fg_color)
        self.input_text.pack(padx=20)

        # Language dropdown
        tk.Label(self, text="Select destination language:", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor='w', padx=20, pady=(10, 0))
        self.lang_dropdown = ttk.Combobox(self, values=list(LANGUAGES.keys()), state='readonly')
        self.lang_dropdown.pack(padx=20, pady=5)
        self.lang_dropdown.set("English")

        # Buttons Frame
        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(pady=10)

        # Translate Button
        self.translate_btn = tk.Button(btn_frame, text="Translate", font=("Helvetica", 12), command=self.translate)
        self.translate_btn.grid(row=0, column=0, padx=5)

        # Dark Mode toggle
        self.dark_mode_btn = tk.Button(btn_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_btn.grid(row=0, column=1, padx=5)

        # Detected language label
        self.detected_label = tk.Label(self, text="", font=("Helvetica", 11), fg="blue", bg=self.bg_color)
        self.detected_label.pack()

        # Output label and text
        tk.Label(self, text="Translated text:", font=("Helvetica", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor='w', padx=20)
        self.output_text = tk.Text(self, height=6, width=75, bg="white" if not self.is_dark else "#444", fg=self.fg_color)
        self.output_text.pack(padx=20, pady=10)

        # Bottom buttons: Speak, Save, Clear
        bottom_frame = tk.Frame(self, bg=self.bg_color)
        bottom_frame.pack(pady=5)

        self.speak_btn = tk.Button(bottom_frame, text="\U0001F50A Speak", width=15, command=self.speak)
        self.speak_btn.grid(row=0, column=0, padx=5)

        self.save_btn = tk.Button(bottom_frame, text="\U0001F4BE Save to File", width=15, command=self.save_to_file)
        self.save_btn.grid(row=0, column=1, padx=5)

        self.clear_btn = tk.Button(bottom_frame, text="\U0001F5D1 Clear All", width=15, command=self.clear_all)
        self.clear_btn.grid(row=0, column=2, padx=5)

    def update_colors(self):
        bg = self.dark_bg if self.is_dark else self.light_bg
        fg = self.dark_fg if self.is_dark else self.light_fg
        self.bg_color = bg
        self.fg_color = fg
        self.configure(bg=bg)

        widgets = [self.title_lbl, self.detected_label]
        for w in widgets:
            w.config(bg=bg, fg=fg)

        for lbl in self.winfo_children():
            if isinstance(lbl, tk.Label) and lbl not in widgets:
                lbl.config(bg=bg, fg=fg)

        self.input_text.config(bg="#444" if self.is_dark else "white", fg=fg)
        self.output_text.config(bg="#444" if self.is_dark else "white", fg=fg)

    def toggle_dark_mode(self):
        self.is_dark = not self.is_dark
        self.update_colors()

    def translate(self):
        text = self.input_text.get("1.0", tk.END).strip()
        dest_lang = self.lang_dropdown.get()

        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        if dest_lang not in LANGUAGES:
            messagebox.showwarning("Language Error", "Invalid destination language.")
            return

        try:
            detected = translator.detect(text)
            translated = translator.translate(text, src=detected.lang, dest=LANGUAGES[dest_lang])
            detected_name = get_language_name(detected.lang)

            self.detected_label.config(text=f"Detected Language: {detected_name} ({detected.lang})")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated.text)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

    def speak(self):
        output = self.output_text.get("1.0", tk.END).strip()
        dest_lang_code = LANGUAGES.get(self.lang_dropdown.get(), 'en')

        if output:
            try:
                tts = gTTS(text=output, lang=dest_lang_code)
                tts.save("temp.mp3")
                playsound.playsound("temp.mp3")
                os.remove("temp.mp3")
            except Exception as e:
                messagebox.showerror("Speech Error", str(e))
        else:
            messagebox.showinfo("No Output", "Translate something first!")

    def save_to_file(self):
        translated = self.output_text.get("1.0", tk.END).strip()
        if not translated:
            messagebox.showinfo("No Output", "Nothing to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(translated)
            messagebox.showinfo("Saved", "Translation saved successfully.")

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.detected_label.config(text="")

if __name__ == "__main__":
    app = MultiLinguaApp()
    app.mainloop()
