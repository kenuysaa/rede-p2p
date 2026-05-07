import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Importando as lógicas que você já tem
from tracker_client import send_request
from utils import get_file_hash
from config import SHARED_FOLDER, TRACKER_HOST, TRACKER_PORT, PEER_PORT, AUTHOR, DISCIPLINE

class P2PClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"P2P Acadêmico - {AUTHOR}")
        self.root.geometry("700x500")

        self.setup_ui()
        self.update_status(f"Conectado ao Tracker: {TRACKER_HOST}:{TRACKER_PORT}")

    def setup_ui(self):
        # Painel Superior - Status e Info
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        self.status_label = tk.Label(top_frame, text="Status: Iniciando...", fg="blue", font=("Arial", 10, "bold"))
        self.status_label.pack()

        # Painel de Ações
        action_frame = tk.LabelFrame(self.root, text="Ações da Rede", padx=10, pady=10)
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_register = tk.Button(action_frame, text="Registrar Meus Arquivos", command=self.handle_register, width=20, bg="#e1f5fe")
        btn_register.grid(row=0, column=0, padx=5)

        btn_list = tk.Button(action_frame, text="Listar Rede", command=self.handle_list, width=20, bg="#e1f5fe")
        btn_list.grid(row=0, column=1, padx=5)

        # Busca por Hash
        search_frame = tk.Frame(action_frame)
        search_frame.grid(row=0, column=2, padx=20)

        tk.Label(search_frame, text="Hash:").pack(side=tk.LEFT)
        self.hash_entry = tk.Entry(search_frame, width=15)
        self.hash_entry.pack(side=tk.LEFT, padx=5)

        btn_lookup = tk.Button(search_frame, text="Buscar Peers", command=self.handle_lookup, bg="#c8e6c9")
        btn_lookup.pack(side=tk.LEFT)

        # Área de Resultados (Tabela)
        result_frame = tk.LabelFrame(self.root, text="Resultados / Arquivos na Rede", padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("nome", "disciplina", "autor", "hash")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")

        self.tree.heading("nome", text="Nome")
        self.tree.heading("disciplina", text="Disciplina")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("hash", text="Hash MD5")

        self.tree.column("nome", width=150)
        self.tree.column("disciplina", width=100)
        self.tree.column("hash", width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def update_status(self, text, color="black"):
        self.status_label.config(text=f"Status: {text}", fg=color)

    def handle_register(self):
        """Executa o registro em uma thread separada para não travar a interface"""
        def task():
            if not SHARED_FOLDER.exists():
                messagebox.showerror("Erro", "Pasta 'shared' não encontrada.")
                return

            files = []
            for entry in SHARED_FOLDER.iterdir():
                if entry.is_file():
                    file_hash = get_file_hash(entry)
                    if file_hash:
                        files.append({
                            "name": entry.name,
                            "discipline": DISCIPLINE,
                            "author": AUTHOR,
                            "type": entry.suffix.lstrip("."),
                            "hash": file_hash
                        })

            if not files:
                messagebox.showwarning("Aviso", "Nenhum arquivo para registrar.")
                return

            request = {
                "type": "REGISTER",
                "ip": self.get_my_ip(),
                "port": PEER_PORT,
                "files": files
            }

            response = send_request(request)
            if response and response.get("status") == "OK":
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"{len(files)} arquivos registrados!"))
                self.update_status("Arquivos registrados com sucesso.", "green")
                self.handle_list()
            else:
                self.update_status("Falha no registro.", "red")

        threading.Thread(target=task, daemon=True).start()

    def handle_list(self):
        def task():
            response = send_request({"type": "LIST"})
            if response and "files" in response:
                self.root.after(0, lambda: self.populate_tree(response["files"]))
                self.update_status("Lista atualizada.", "black")

        threading.Thread(target=task, daemon=True).start()

    def handle_lookup(self):
        file_hash = self.hash_entry.get().strip()
        if not file_hash:
            messagebox.showwarning("Aviso", "Insira um hash para buscar.")
            return

        def task():
            response = send_request({"type": "LOOKUP", "hash": file_hash})
            if response and "peers" in response:
                peers_list = "\n".join([f"{p['ip']}:{p['port']} (Score: {p['score']:.4f})" for p in response["peers"]])
                self.root.after(0, lambda: messagebox.showinfo("Peers Encontrados", peers_list))
            else:
                self.root.after(0, lambda: messagebox.showwarning("Busca", "Nenhum peer encontrado para este hash."))

        threading.Thread(target=task, daemon=True).start()

    def populate_tree(self, files):
        # Limpa a tabela
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Adiciona novos dados
        for f in files:
            self.tree.insert("", tk.END, values=(f["name"], f["discipline"], f["author"], f["hash"]))

    def get_my_ip(self):
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except: return "127.0.0.1"

if __name__ == "__main__":
    root = tk.Tk()
    app = P2PClientGUI(root)
    root.mainloop()
