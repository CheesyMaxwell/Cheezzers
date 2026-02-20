import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import platform, psutil, re, os, subprocess, threading, traceback
from PIL import Image

class CheezzersLuxury:
    def __init__(self, root):
        self.root = root
        self.root.title("🧀 CHEEZZERS - LUXURY ULTIMATE")
        self.root.geometry("1000x720")
        self.root.configure(bg="#1e1e1e")
        
        # Hardware & Pfade
        self.cpu = platform.processor() or "AMD Athlon II Neo K145"
        self.ram = round(psutil.virtual_memory().total / (1024**3), 2)
        self.icon_path = tk.StringVar(value="")
        
        self.setup_ui()
        self.setup_cheatsheet()
        self.apply_initial_code()

    def setup_ui(self):
        # SIDEBAR
        sidebar = tk.Frame(self.root, width=220, bg="#252526")
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="LUXURY MODE", fg="#f1c40f", bg="#252526", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Label(sidebar, text=f"💻 {self.cpu[:15]}...\n📟 RAM: {self.ram} GB", 
                 fg="#888888", bg="#1e1e1e", justify="left", font=("Consolas", 9), padx=10, pady=10).pack(padx=10, fill="x")

        # MAIN
        main_area = tk.Frame(self.root, bg="#1e1e1e")
        main_area.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        # TOOLBAR
        toolbar = tk.Frame(main_area, bg="#1e1e1e")
        toolbar.pack(fill="x", pady=5)

        # Buttons Links
        tk.Button(toolbar, text="▶️ RUN", bg="#27ae60", fg="white", bd=0, padx=10, command=self.run_test).pack(side="left", padx=3)
        tk.Button(toolbar, text="🖼️ PNG➔ICO", bg="#8e44ad", fg="white", bd=0, padx=10, command=self.convert_icon).pack(side="left", padx=3)
        tk.Button(toolbar, text="📜 CHEAT", bg="#16a085", fg="white", bd=0, padx=10, command=self.toggle_sheet).pack(side="left", padx=3)
        
        # Build Buttons Rechts
        tk.Button(toolbar, text="🐧 BUILD DEB", bg="#3498db", fg="white", bd=0, padx=10, command=lambda: self.start_build("deb")).pack(side="right", padx=3)
        tk.Button(toolbar, text="🪟 BUILD EXE", bg="#e67e22", fg="white", bd=0, padx=10, command=lambda: self.start_build("exe")).pack(side="right", padx=3)

        # EDITOR
        self.editor = scrolledtext.ScrolledText(main_area, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", bd=0, undo=True)
        self.editor.pack(fill="both", expand=True)
        self.editor.bind("<KeyRelease>", lambda e: self.highlight())

        # DEBUG LOG
        debug_frame = tk.LabelFrame(main_area, text="🛠️ DEBUG & STATUS", bg="#1e1e1e", fg="#ff4444")
        debug_frame.pack(fill="x", side="bottom", pady=5)
        self.status_log = tk.Text(debug_frame, height=4, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9), state="disabled")
        self.status_log.pack(fill="x", padx=5, pady=5)

        # Syntax Tags
        self.tags = {"kw": "#569cd6", "str": "#ce9178", "com": "#6a9955", "num": "#b5cea8", "err": "#440000"}
        for t, c in self.tags.items(): self.editor.tag_config(t, foreground=c if t != "err" else None, background=c if t == "err" else None)

    def log(self, msg, error=False):
        self.status_log.config(state="normal")
        self.status_log.delete("1.0", tk.END)
        self.status_log.insert(tk.END, msg)
        self.status_log.config(state="disabled", fg="#ff4444" if error else "#00ff00")

    def highlight(self):
        code = self.editor.get("1.0", tk.END)
        for t in self.tags: self.editor.tag_remove(t, "1.0", tk.END)
        for w in ["print","import","def","if","else","return","for","while","class","as"]:
            for m in re.finditer(rf"\b{w}\b", code): self.editor.tag_add("kw", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        for t, p in [("str", r"'.*?'|\".*?\""), ("com", r"#.*"), ("num", r"\b\d+\b")]:
            for m in re.finditer(p, code): self.editor.tag_add(t, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    def run_test(self):
        self.log("🚀 Starte Testlauf...")
        try: exec(self.editor.get("1.0", tk.END), {"__name__": "__main__", "tk": tk})
        except Exception: self.log(traceback.format_exc(), True)

    def convert_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Bilder", "*.png *.jpg")])
        if path:
            try:
                img = Image.open(path)
                save_p = filedialog.asksaveasfilename(defaultextension=".ico")
                if save_p:
                    img.save(save_p, format='ICO', sizes=[(32,32), (64,64), (256,256)])
                    self.icon_path.set(save_p)
                    self.log(f"✅ Icon erstellt: {os.path.basename(save_p)}")
            except Exception as e: self.log(f"Fehler: {e}", True)

    def start_build(self, mode):
        with open("temp_project.py", "w") as f: f.write(self.editor.get("1.0", tk.END))
        if mode == "exe": threading.Thread(target=self.build_exe).start()
        else: threading.Thread(target=self.build_deb).start()

    def build_exe(self):
        self.log("📦 Baue Windows .EXE... Bitte warten.")
        cmd = ["pyinstaller", "--onefile", "--windowed"]
        if self.icon_path.get(): cmd.append(f"--icon={self.icon_path.get()}")
        cmd.append("temp_project.py")
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.log("✅ EXE fertig im 'dist' Ordner!" if res.returncode == 0 else f"❌ Fehler: {res.stderr[:100]}", res.returncode != 0)

    def build_deb(self):
        self.log("🐧 Baue Debian .DEB... Bitte warten.")
        try:
            name = "cheezzers-app"
            os.makedirs(f"{name}/DEBIAN", exist_ok=True)
            os.makedirs(f"{name}/usr/local/bin", exist_ok=True)
            with open(f"{name}/DEBIAN/control", "w") as f:
                f.writelines(["Package: cheezzers-app\n","Version: 1.0\n","Architecture: all\n","Maintainer: Elias\n","Description: App\n"])
            with open(f"{name}/usr/local/bin/{name}", "w") as f:
                f.write("#!/usr/bin/env python3\n" + self.editor.get("1.0", tk.END))
            os.chmod(f"{name}/usr/local/bin/{name}", 0o755)
            subprocess.run(["dpkg-deb", "--build", name])
            self.log(f"✅ .DEB Paket fertig: {name}.deb")
        except Exception as e: self.log(str(e), True)

    def setup_cheatsheet(self):
        self.sheet = tk.Toplevel(self.root); self.sheet.withdraw()
        self.sheet.title("Hilfe"); self.sheet.geometry("200x300")
        cmds = {"Button": "tk.Button(text='OK').pack()", "Loop": "for i in range(5):", "Print": "print('Hi')"}
        for k, v in cmds.items(): tk.Button(self.sheet, text=k, command=lambda c=v: self.editor.insert(tk.INSERT, c)).pack(fill="x")

    def toggle_sheet(self): self.sheet.deiconify() if not self.sheet.winfo_viewable() else self.sheet.withdraw()
    def apply_initial_code(self): 
        self.editor.insert("1.0", "# Cheezzers Luxury\nimport tkinter as tk\nroot = tk.Tk()\ntk.Label(text='Hallo Elias').pack()\nroot.mainloop()")
        self.highlight()

if __name__ == "__main__":
    root = tk.Tk()
    app = CheezzersLuxury(root)
    root.mainloop()

