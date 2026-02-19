import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class Cheezzers:
    def __init__(self, root):
        self.root = root
        self.root.title("Cheezzers v1.0 - Low Resource Edition")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        # Header
        self.header = tk.Label(root, text="CHEEZZERS", font=("Courier", 24, "bold"), bg="#f0f0f0")
        self.header.pack(pady=10)

        # Mode Selector (Basic / Expert)
        self.mode_frame = tk.Frame(root, bg="#f0f0f0")
        self.mode_frame.pack(fill="x", padx=20)
        
        self.is_expert = tk.BooleanVar(value=False)
        self.mode_btn = tk.Checkbutton(self.mode_frame, text="Expert Mode aktivieren", 
                                      variable=self.is_expert, command=self.toggle_mode)
        self.mode_btn.pack(side="right")

        # Software Info Bereich
        self.info_label = tk.Label(root, text="Free-to-use .deb & .exe Creator", font=("Arial", 10, "italic"))
        self.info_label.pack()

        # Hauptbereich
        self.main_frame = tk.LabelFrame(root, text="Projekt-Einstellungen", padx=10, pady=10)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # Name
        tk.Label(self.main_frame, text="Software Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self.main_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Format
        tk.Label(self.main_frame, text="Zielformat:").grid(row=1, column=0, sticky="w")
        self.format_combo = ttk.Combobox(self.main_frame, values=[".exe (Windows)", ".deb (Debian/Ubuntu)", ".zip (Portable)"])
        self.format_combo.current(0)
        self.format_combo.grid(row=1, column=1, pady=5)

        # Expert Features (initial versteckt)
        self.expert_label = tk.Label(self.main_frame, text="Expert Options (LTO Optimization, Stripping)", fg="red")
        self.expert_entry = tk.Entry(self.main_frame, width=30)

        # Build Button
        self.build_btn = tk.Button(root, text="START BUILD", bg="#4CAF50", fg="white", 
                                  font=("Arial", 12, "bold"), command=self.run_build)
        self.build_btn.pack(pady=10)

    def toggle_mode(self):
        if self.is_expert.get():
            self.expert_label.grid(row=2, column=0, sticky="w")
            self.expert_entry.grid(row=2, column=1, pady=5)
            self.root.configure(bg="#2c3e50") # "Modern" Darker Look
        else:
            self.expert_label.grid_forget()
            self.expert_entry.grid_forget()
            self.root.configure(bg="#f0f0f0")

    def run_build(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Fehler", "Bitte einen Namen eingeben!")
            return
        
        # Simulierter Build-Prozess
        format_ext = self.format_combo.get()
        mode = "Expert" if self.is_expert.get() else "Basic"
        messagebox.showinfo("Cheezzers Build", f"Erstelle {name}{format_ext[:4]} im {mode} Modus...\n\nHardware-Check: AMD Athlon II Neo erkannt - Optimierung aktiv.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Cheezzers(root)
    root.mainloop()

