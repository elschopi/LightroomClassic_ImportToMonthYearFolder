import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import ctypes
import sys
from datetime import datetime

class LightroomPatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lightroom Import-Ordner Patcher v3")
        self.root.geometry("650x400")
        self.root.resizable(False, False)

        # Definierte Strings
        self.TEMPLATE_PREFIX = r'"$$$/AgImportDialog/ShootArrangement_1/Template='
        self.ORIGINAL_VALUE = r'%Y/%m-%d'
        
        # Liste gängiger Formate für das Dropdown
        self.PRESET_FORMATS = [
            r'%B %Y',          # November 2025
            r'%Y/%B',          # 2025/November
            r'%Y-%m-%d',       # 2025-11-24
            r'%Y/%m/%d',       # 2025/11/24
            r'%Y/%m-%d',       # 2025/11-24 (Original-ähnlich)
            r'%y%m%d',         # 251124
        ]
        self.DEFAULT_PATCH_VALUE = self.PRESET_FORMATS[0]

        self.check_admin()
        self.create_widgets()
        
        # Aktualisierter Standardpfad
        default_path = r'C:\Program Files\Adobe\Adobe Lightroom Classic\Resources\de\TranslatedStrings.txt'
        if os.path.exists(default_path):
            self.path_var.set(default_path)
            self.check_file_state()

    def check_admin(self):
        """Prüft auf Administratorrechte."""
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        if not is_admin:
            messagebox.showwarning(
                "Fehlende Rechte",
                "Warnung: Diese Anwendung läuft nicht als Administrator.\n\n"
                "Das Bearbeiten von Dateien in 'C:\\Program Files' wird wahrscheinlich fehlschlagen.\n"
                "Bitte starte das Programm als Administrator neu."
            )

    def create_widgets(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Sektion 1: Dateiauswahl ---
        ttk.Label(main_frame, text="Pfad zur 'TranslatedStrings' Datei:").grid(row=0, column=0, sticky=tk.W, columnspan=2)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=60)
        self.path_entry.grid(row=1, column=0, pady=(5, 15), sticky=tk.EW)
        
        browse_btn = ttk.Button(main_frame, text="Durchsuchen...", command=self.browse_file)
        browse_btn.grid(row=1, column=1, padx=(10, 0), pady=(5, 15), sticky=tk.E)

        # --- Sektion 2: Format Anpassung ---
        format_frame = ttk.LabelFrame(main_frame, text="Format Anpassung", padding="15")
        format_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=(0, 20))

        ttk.Label(format_frame, text="Gewünschtes Format:").grid(row=0, column=0, sticky=tk.W)
        
        self.format_var = tk.StringVar(value=self.DEFAULT_PATCH_VALUE)
        self.format_var.trace_add("write", self.update_preview) 
        
        # Combobox statt einfachem Entry für Dropdown-Funktionalität
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, values=self.PRESET_FORMATS, width=25, font=("Consolas", 10))
        self.format_combo.grid(row=0, column=1, sticky=tk.W, padx=10)

        ttk.Label(format_frame, text="Vorschau (heute):").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        
        self.preview_var = tk.StringVar()
        self.preview_label = ttk.Label(format_frame, textvariable=self.preview_var, font=("Helvetica", 10, "bold italic"), foreground="blue")
        self.preview_label.grid(row=0, column=3, sticky=tk.W)

        # Hilfetext
        help_text = (
            "Wähle ein Format aus der Liste oder gib einen eigenen Python strftime Code ein.\n"
            "Beispiele: %Y=Jahr (4-stellig), %y=Jahr (2-stellig), %m=Monat (Zahl), %B=Monatsname.\n"
            "Verwende '/' um Unterordner zu erstellen."
        )
        ttk.Label(format_frame, text=help_text, font=("Helvetica", 8), foreground="gray", justify=tk.LEFT).grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(10,0))

        # --- Sektion 3: Status und Aktionen ---
        self.status_var = tk.StringVar(value="Status: Bereit zum Prüfen")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Helvetica", 9))
        self.status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)

        self.check_btn = ttk.Button(btn_frame, text="Datei prüfen", command=self.check_file_state)
        self.check_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.patch_btn = ttk.Button(btn_frame, text="Format anwenden", command=self.apply_patch, state=tk.DISABLED)
        self.patch_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.restore_btn = ttk.Button(btn_frame, text="Original wiederherstellen", command=self.restore_original, state=tk.DISABLED)
        self.restore_btn.pack(side=tk.RIGHT)

        main_frame.columnconfigure(0, weight=1)
        self.update_preview()

    def update_preview(self, *args):
        """Aktualisiert das Vorschau-Label basierend auf dem Format-String."""
        fmt = self.format_var.get()
        try:
            preview_text = datetime.now().strftime(fmt)
            self.preview_var.set(preview_text)
            self.preview_label.config(foreground="blue")
        except Exception:
            self.preview_var.set("Ungültiges Format")
            self.preview_label.config(foreground="red")

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Wähle die TranslatedStrings Datei",
            filetypes=[("Text Dateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if filename:
            self.path_var.set(filename)
            self.check_file_state()

    def check_file_state(self):
        filepath = self.path_var.get()
        if not os.path.exists(filepath):
            self.set_status("Fehler: Datei nicht gefunden!", "red")
            self.patch_btn.config(state=tk.DISABLED)
            self.restore_btn.config(state=tk.DISABLED)
            return

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            original_full_line = self.TEMPLATE_PREFIX + self.ORIGINAL_VALUE + '"'

            if original_full_line in content:
                self.set_status("Status: Original gefunden. Bereit zum Ändern.", "green")
                self.patch_btn.config(state=tk.NORMAL, text="Format anwenden")
                self.restore_btn.config(state=tk.DISABLED)
            elif self.TEMPLATE_PREFIX in content:
                self.set_status("Status: Datei ist bereits modifiziert.", "orange")
                self.patch_btn.config(state=tk.NORMAL, text="Format aktualisieren")
                self.restore_btn.config(state=tk.NORMAL)
            else:
                self.set_status("Fehler: Ziel-Zeile in dieser Datei nicht gefunden.", "red")
                self.patch_btn.config(state=tk.DISABLED)
                self.restore_btn.config(state=tk.DISABLED)

        except Exception as e:
            self.set_status(f"Fehler beim Lesen: {str(e)}", "red")

    def set_status(self, text, color="black"):
        self.status_var.set(text)
        self.status_label.config(foreground=color)

    def create_backup(self, filepath):
        backup_path = filepath + ".bak"
        if not os.path.exists(backup_path):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as original:
                    data = original.read()
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(data)
                return True
            except Exception as e:
                messagebox.showerror("Backup Fehler", f"Konnte kein Backup erstellen:\n{e}")
                return False
        return True

    def apply_patch(self):
        current_format = self.format_var.get()
        self._modify_file(current_format, f"Format '{current_format}' erfolgreich angewendet!")

    def restore_original(self):
        self._modify_file(self.ORIGINAL_VALUE, "Original wiederhergestellt!")

    def _modify_file(self, new_format_value, success_msg):
        filepath = self.path_var.get()
        
        if not self.create_backup(filepath):
            return

        new_line_content = self.TEMPLATE_PREFIX + new_format_value + '"\n'

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            with open(filepath, 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.strip().startswith(self.TEMPLATE_PREFIX):
                        file.write(new_line_content)
                    else:
                        file.write(line)
            
            messagebox.showinfo("Erfolg", success_msg)
            self.check_file_state()

        except PermissionError:
             messagebox.showerror("Zugriffsfehler", "Zugriff verweigert! Bitte starte das Programm als Administrator.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LightroomPatcherApp(root)
    root.mainloop()