import socket
import threading
import webbrowser
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, messagebox


class PortScannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Scanner")
        self.root.geometry("780x520")
        self.root.configure(bg="#0f172a")

        self.open_ports = []
        self.scanning = False
        self.total_ports = 0
        self.scanned_ports = 0
        self.lock = threading.Lock()

        self._build_header()
        self._build_form()
        self._build_results()
        self._build_footer()

    def _build_header(self):
        header = tk.Frame(self.root, bg="#0f172a", pady=20)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Port Scanner",
            fg="#e2e8f0",
            bg="#0f172a",
            font=("Helvetica", 22, "bold"),
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Analyse rapide et élégante de vos ports réseau",
            fg="#94a3b8",
            bg="#0f172a",
            font=("Helvetica", 11),
        )
        subtitle.pack()

    def _build_form(self):
        card = tk.Frame(self.root, bg="#111827", bd=0, highlightthickness=0)
        card.pack(fill="x", padx=24, pady=(8, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.TEntry",
            fieldbackground="#0b1221",
            foreground="#e2e8f0",
            borderwidth=0,
            relief="flat",
            padding=8,
        )
        style.configure(
            "Action.TButton",
            padding=10,
            background="#22c55e",
            foreground="#0b1221",
            borderwidth=0,
            focusthickness=0,
            font=("Helvetica", 10, "bold"),
        )
        style.map(
            "Action.TButton",
            background=[("active", "#16a34a"), ("disabled", "#1e293b")],
            foreground=[("disabled", "#475569")],
        )

        form = tk.Frame(card, bg="#111827")
        form.pack(fill="x", pady=12)

        # IP input
        ip_label = tk.Label(
            form,
            text="Adresse IP ou domaine",
            fg="#cbd5e1",
            bg="#111827",
            font=("Helvetica", 10, "bold"),
        )
        ip_label.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 6))

        self.ip_entry = ttk.Entry(form, style="Custom.TEntry")
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))

        # Port range
        range_frame = tk.Frame(form, bg="#111827")
        range_frame.grid(row=1, column=1, sticky="ew")
        range_frame.columnconfigure(1, weight=1)

        start_label = tk.Label(
            range_frame, text="Port début", fg="#cbd5e1", bg="#111827", font=("Helvetica", 9, "bold")
        )
        start_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.start_entry = ttk.Entry(range_frame, style="Custom.TEntry", width=10)
        self.start_entry.insert(0, "1")
        self.start_entry.grid(row=1, column=0, sticky="w")

        end_label = tk.Label(
            range_frame, text="Port fin", fg="#cbd5e1", bg="#111827", font=("Helvetica", 9, "bold")
        )
        end_label.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 6))
        self.end_entry = ttk.Entry(range_frame, style="Custom.TEntry", width=10)
        self.end_entry.insert(0, "1024")
        self.end_entry.grid(row=1, column=1, sticky="w", padx=(10, 0))

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        # Buttons
        actions = tk.Frame(card, bg="#111827")
        actions.pack(fill="x", pady=(0, 8))

        self.scan_button = ttk.Button(actions, text="Lancer le scan", style="Action.TButton", command=self.start_scan)
        self.scan_button.pack(side="left")

        stop_btn = ttk.Button(actions, text="Stop", style="Action.TButton", command=self.stop_scan)
        stop_btn.pack(side="left", padx=(10, 0))

        open_btn = ttk.Button(actions, text="Ouvrir les ports", style="Action.TButton", command=self.open_ports_in_browser)
        open_btn.pack(side="right")

        self.status_label = tk.Label(
            card,
            text="Prêt à scanner",
            fg="#94a3b8",
            bg="#111827",
            font=("Helvetica", 9),
            anchor="w",
        )
        self.status_label.pack(fill="x")

        self.progress = ttk.Progressbar(card, mode="determinate")
        self.progress.pack(fill="x", pady=(6, 0))

    def _build_results(self):
        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        results_card = tk.Frame(container, bg="#111827")
        results_card.pack(fill="both", expand=True)

        heading = tk.Label(
            results_card,
            text="Ports ouverts",
            fg="#e2e8f0",
            bg="#111827",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        heading.pack(fill="x", padx=14, pady=(12, 6))

        self.listbox = tk.Listbox(
            results_card,
            bg="#0b1221",
            fg="#e2e8f0",
            selectbackground="#22c55e",
            selectforeground="#0b1221",
            highlightthickness=0,
            activestyle="none",
            font=("Consolas", 11),
        )
        self.listbox.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def _build_footer(self):
        footer = tk.Frame(self.root, bg="#0f172a", pady=10)
        footer.pack(fill="x")

        info = tk.Label(
            footer,
            text="Cliquez sur \"Ouvrir les ports\" pour tester les services détectés dans votre navigateur.",
            fg="#475569",
            bg="#0f172a",
            font=("Helvetica", 9),
        )
        info.pack()

    def start_scan(self):
        if self.scanning:
            return

        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Champ requis", "Veuillez saisir une adresse IP ou un domaine.")
            return

        try:
            start_port = int(self.start_entry.get())
            end_port = int(self.end_entry.get())
        except ValueError:
            messagebox.showwarning("Ports invalides", "Merci d'indiquer des numéros de ports valides.")
            return

        if not 1 <= start_port <= 65535 or not 1 <= end_port <= 65535 or start_port > end_port:
            messagebox.showwarning("Plage invalide", "La plage de ports doit être comprise entre 1 et 65535.")
            return

        self.open_ports.clear()
        self.listbox.delete(0, tk.END)
        self.total_ports = end_port - start_port + 1
        self.scanned_ports = 0
        self.progress.configure(maximum=self.total_ports, value=0)

        self.scanning = True
        self.scan_button.state(["disabled"])
        self.status_label.config(text="Scan en cours...")

        threading.Thread(
            target=self._run_scan,
            args=(ip, start_port, end_port),
            daemon=True,
        ).start()

    def stop_scan(self):
        if self.scanning:
            self.scanning = False
            self.status_label.config(text="Scan interrompu")
            self.scan_button.state(["!disabled"])

    def _run_scan(self, ip: str, start_port: int, end_port: int):
        with ThreadPoolExecutor(max_workers=120) as executor:
            futures = []
            for port in range(start_port, end_port + 1):
                if not self.scanning:
                    break
                futures.append(executor.submit(self._scan_single_port, ip, port))

            for future in futures:
                if not self.scanning:
                    break
                result = future.result()
                self._update_progress()
                if result:
                    self.root.after(0, self._add_open_port, result)

        self.root.after(0, self._scan_complete)

    def _scan_single_port(self, ip: str, port: int):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.8)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    return port
        except Exception:
            return None
        return None

    def _update_progress(self):
        with self.lock:
            self.scanned_ports += 1
            value = min(self.scanned_ports, self.total_ports)
        self.root.after(0, lambda: self.progress.configure(value=value))

    def _add_open_port(self, port: int):
        self.open_ports.append(port)
        self.listbox.insert(tk.END, f"Port {port} ouvert")
        self.status_label.config(text=f"{len(self.open_ports)} port(s) détecté(s) comme ouvert(s)")

    def _scan_complete(self):
        if self.scanning:
            if self.open_ports:
                self.status_label.config(text="Scan terminé – ports ouverts détectés")
            else:
                self.status_label.config(text="Scan terminé – aucun port ouvert")
        else:
            self.status_label.config(text="Scan interrompu")

        self.scanning = False
        self.scan_button.state(["!disabled"])

    def open_ports_in_browser(self):
        if not self.open_ports:
            messagebox.showinfo("Aucun port", "Lancez un scan pour découvrir les ports ouverts.")
            return

        ip = self.ip_entry.get().strip()
        for port in self.open_ports:
            url = f"https://{ip}:{port}"
            webbrowser.open(url)
        messagebox.showinfo("Ouverture", "Les ports détectés ont été ouverts dans le navigateur.")

    def run(self):
        self.root.mainloop()


def main():
    app = PortScannerApp()
    app.run()


if __name__ == "__main__":
    main()
