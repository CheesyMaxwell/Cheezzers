import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import platform, psutil, re, os, subprocess, threading, traceback, json
from PIL import Image

class CheezzersLuxury:
    def __init__(self, root):
        self.root = root
        self.root.title("🧀 CHEEZZERS - LUXURY ULTIMATE")
        self.root.geometry("1050x750")
        
        # 1. Einstellungen laden
        self.config_file = "config.json"
        self.load_settings()
        
        # 2. Hardware-Check
        self.cpu = platform.processor() or "AMD Athlon II Neo K145"
        self.ram = round(psutil.virtual_memory().total / (1024**3), 2)
        self.icon_path = tk.StringVar(value="")
        
        # 3. UI Starten
        self.apply_theme()
        self.setup_ui()
        self.setup_cheatsheet()
        self.apply_initial_code()

    def load_settings(self):
        default = {"lang": "DE", "font_size": 12, "contrast": "Normal"}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f: self.settings = json.load(f)
            except: self.settings = default
        else: self.settings = default

    def apply_theme(self):
        if self.settings.get("contrast") == "High":
            self.colors = {"bg": "#000000", "sidebar": "#0a0a0a", "text": "#ffffff", "btn": "#444444", "gold": "#f1c40f", "exit": "#ff0000"}
        else:
            self.colors = {"bg": "#1e1e1e", "sidebar": "#252526", "text": "#d4d4d4", "btn": "#3c3c3c", "gold": "#d4af37", "exit": "#c0392b"}
        self.root.configure(bg=self.colors["bg"])

    def setup_ui(self):
        # SIDEBAR
        self.sidebar = tk.Frame(self.root, width=220, bg=self.colors["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        
        # --- LOGO BANNER ---
        self.logo_frame = tk.Frame(self.sidebar, bg=self.colors["gold"], padx=2, pady=2)
        self.logo_frame.pack(pady=20, padx=10, fill="x")
        self.inner_logo = tk.Frame(self.logo_frame, bg="#1a1a1a")
        self.inner_logo.pack(fill="x")
        self.logo_label = tk.Label(self.inner_logo, text="CHEEZZERS", fg=self.colors["gold"], bg="#1a1a1a", font=("Verdana", 14, "bold italic"))
        self.logo_label.pack(pady=5)
        
        # --- BUTTONS ---
        tk.Button(self.sidebar, text="⚙️ OPTIONEN", bg=self.colors["btn"], fg="white", bd=0, command=self.open_settings).pack(pady=10, fill="x", padx=20)
        
        # --- NEUER QUIT BUTTON ---
        tk.Button(self.sidebar, text="❌ BEENDEN", bg=self.colors["exit"], fg="white", bd=0, font=("Arial", 9, "bold"), command=self.quit_app).pack(pady=10, fill="x", padx=20)
        
        # System Info unten
        info_lbl = tk.Label(self.sidebar, text=f"💻 {self.cpu[:12]}..\n📟 {self.ram} GB RAM", fg="#666666", bg=self.colors["sidebar"], font=("Arial", 8))
        info_lbl.pack(side="bottom", pady=10)

        # MAIN AREA
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_area.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        # TOOLBAR
        toolbar = tk.Frame(self.main_area, bg=self.colors["bg"])
        toolbar.pack(fill="x", pady=5)
        tk.Button(toolbar, text="▶️ RUN", bg="#27ae60", fg="white", bd=0, padx=10, command=self.run_test).pack(side="left", padx=3)
        tk.Button(toolbar, text="🖼️ PNG➔ICO", bg="#8e44ad", fg="white", bd=0, padx=10, command=self.convert_icon).pack(side="left", padx=3)
        tk.Button(toolbar, text="📜 CHEAT", bg="#16a085", fg="white", bd=0, padx=10, command=self.toggle_sheet).pack(side="left", padx=3)
        
        tk.Button(toolbar, text="🐧 BUILD DEB", bg="#3498db", fg="white", bd=0, padx=10, command=lambda: self.start_build("deb")).pack(side="right", padx=3)
        tk.Button(toolbar, text="🪟 BUILD EXE", bg="#e67e22", fg="white", bd=0, padx=10, command=lambda: self.start_build("exe")).pack(side="right", padx=3)

        # EDITOR
        self.editor = scrolledtext.ScrolledText(self.main_area, font=("Consolas", self.settings["font_size"]), bg=self.colors["bg"], fg=self.colors["text"], insertbackground="white", bd=0, undo=True)
        self.editor.pack(fill="both", expand=True)
        self.editor.bind("<KeyRelease>", lambda e: self.highlight())

        # STATUS LOG
        self.status_log = tk.Text(self.main_area, height=3, bg=self.colors["bg"], fg="#00ff00", font=("Consolas", 9), state="disabled")
        self.status_log.pack(fill="x", side="bottom", pady=5)

        self.tags = {"kw": "#569cd6", "str": "#ce9178", "com": "#6a9955", "num": "#b5cea8"}
        for t, c in self.tags.items(): self.editor.tag_config(t, foreground=c)

    def quit_app(self):
        if messagebox.askokcancel("Beenden", "Möchtest du Cheezzers wirklich schließen?"):
            self.root.destroy()

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Konfiguration")
        win.geometry("300x400")
        win.configure(bg=self.colors["sidebar"])
        
        tk.Label(win, text="EINSTELLUNGEN", fg=self.colors["gold"], bg=self.colors["sidebar"], font=("Arial", 11, "bold")).pack(pady=15)
        
        tk.Label(win, text="Textgröße:", fg="white", bg=self.colors["sidebar"]).pack()
        size_sc = tk.Scale(win, from_=8, to=24, orient="horizontal", bg=self.colors["sidebar"], fg="white", highlightthickness=0)
        size_sc.set(self.settings["font_size"])
        size_sc.pack(pady=5, fill="x", padx=30)

        tk.Label(win, text="Kontrast:", fg="white", bg=self.colors["sidebar"]).pack(pady=10)
        con_cb = ttk.Combobox(win, values=["Normal", "High"], state="readonly")
        con_cb.set(self.settings["contrast"])
        con_cb.pack(pady=5)

        def save():
            self.settings = {"lang": "DE", "font_size": size_sc.get(), "contrast": con_cb.get()}
            with open(self.config_file, "w") as f: json.dump(self.settings, f)
            messagebox.showinfo("Cheezzers", "Gespeichert! Bitte neu starten.")
            win.destroy()
            self.apply_theme()
            self.editor.configure(font=("Consolas", self.settings["font_size"]))
        
        tk.Button(win, text="SPEICHERN", bg="#27ae60", fg="white", bd=0, padx=20, pady=5, command=save).pack(pady=30)

    def run_test(self):
        self.status_log.config(state="normal"); self.status_log.delete("1.0", tk.END)
        try: exec(self.editor.get("1.0", tk.END), {"tk": tk, "root": tk.Tk})
        except: self.status_log.insert("1.0", traceback.format_exc())
        self.status_log.config(state="disabled")

    def highlight(self):
        code = self.editor.get("1.0", tk.END)
        for t in self.tags: self.editor.tag_remove(t, "1.0", tk.END)
        for w in ["print","import","def","if","else","return","for","while","class","as"]:
            for m in re.finditer(rf"\b{w}\b", code): self.editor.tag_add("kw", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        for t, p in [("str", r"'.*?'|\".*?\""), ("com", r"#.*"), ("num", r"\b\d+\b")]:
            for m in re.finditer(p, code): self.editor.tag_add(t, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    def convert_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Bilder", "*.png *.jpg *.jpeg")])
        if path:
            try:
                img = Image.open(path); save_p = filedialog.asksaveasfilename(defaultextension=".ico")
                if save_p: img.save(save_p, format='ICO', sizes=[(32,32), (64,64), (256,256)])
                messagebox.showinfo("Icon", "Erfolgreich umgewandelt!")
            except Exception as e: messagebox.showerror("Fehler", str(e))

    def start_build(self, mode):
        with open("temp_build.py", "w") as f: f.write(self.editor.get("1.0", tk.END))
        t = self.build_exe if mode == "exe" else self.build_deb
        threading.Thread(target=t, daemon=True).start()

    def build_exe(self):
        res = subprocess.run(["pyinstaller", "--onefile", "--windowed", "temp_build.py"], capture_output=True)
        messagebox.showinfo("Build", "EXE fertig!" if res.returncode == 0 else "Fehler: PyInstaller fehlt?")

    def build_deb(self):
        try:
            os.makedirs("app_pkg/DEBIAN", exist_ok=True); os.makedirs("app_pkg/usr/bin", exist_ok=True)
            with open("app_pkg/DEBIAN/control", "w") as f: f.write("Package: app\nVersion: 1.0\nArchitecture: all\nMaintainer: Elias\nDescription: App\n")
            subprocess.run(["dpkg-deb", "--build", "app_pkg"])
            messagebox.showinfo("Build", ".DEB fertig!")
        except: messagebox.showerror("Fehler", "Deb-Build fehlgeschlagen.")

    def setup_cheatsheet(self):
        self.sheet = tk.Toplevel(self.root); self.sheet.withdraw()
        self.sheet.title("Hilfe")
        for k, v in {"Print": "print('')", "Loop": "for i in range(5):", "Window": "tk.Tk().mainloop()"}.items():
            tk.Button(self.sheet, text=k, command=lambda c=v: self.editor.insert(tk.INSERT, c + "\n")).pack(fill="x")

    def toggle_sheet(self): self.sheet.deiconify() if not self.sheet.winfo_viewable() else self.sheet.withdraw()
    def apply_initial_code(self): 
        self.editor.insert("1.0", "# Willkommen Elias\nimport tkinter as tk\n\nprint('System bereit!')")
        self.highlight()

if __name__ == "__main__":
    root = tk.Tk()
    app = CheezzersLuxury(root)
    root.mainloop()

