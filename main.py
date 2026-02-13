import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import qrcode
from PIL import Image, ImageTk

# --- CORES OFICIAIS E ESTILO ---
COLOR_BG = "#F0F2F5"         # Fundo da Janela (Cinza Claro)
COLOR_CARD = "#FFFFFF"       # Fundo dos Cards (Branco)
COLOR_PIX = "#32BCAD"        # Verde Pix Oficial
COLOR_PIX_HOVER = "#2DAAA0"  # Verde um pouco mais escuro para hover
COLOR_TEXT = "#333333"       # Cor do texto principal
COLOR_BTN_TEXT = "#FFFFFF"   # Texto do botão

class PixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador Pix Pro")
        self.root.geometry("850x720")
        self.root.configure(bg=COLOR_BG) # Define a cor de fundo da janela
        
        self.setup_styles()
        self.create_layout()
        self.qr_image = None 

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # 'clam' permite maior customização de cores

        # Configuração Genérica de Frames e Labels
        style.configure("Card.TFrame", background=COLOR_CARD, relief="flat")
        style.configure("TLabel", background=COLOR_CARD, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=COLOR_CARD, foreground=COLOR_PIX, font=("Segoe UI", 16, "bold"))
        style.configure("SubHeader.TLabel", background=COLOR_CARD, foreground="#666666", font=("Segoe UI", 11))
        
        # Configuração dos Inputs
        style.configure("TEntry", fieldbackground="#FAFAFA", insertcolor=COLOR_TEXT)
        
        # --- BOTÃO VERDE (PIX) ---
        style.configure(
            "Pix.TButton",
            background=COLOR_PIX,
            foreground=COLOR_BTN_TEXT,
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            focuscolor=COLOR_PIX
        )
        style.map("Pix.TButton", background=[('active', COLOR_PIX_HOVER)])

        # --- BOTÃO SECUNDÁRIO (IMPORTAR) ---
        style.configure(
            "Outline.TButton",
            background="#E0E0E0",
            foreground="#444444",
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map("Outline.TButton", background=[('active', "#D0D0D0")])

    def create_layout(self):
        # Container Principal com padding para não colar nas bordas
        main_container = tk.Frame(self.root, bg=COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # === CARD ESQUERDO (DADOS) ===
        # Usamos Frame normal do tk para conseguir bordas arredondadas (truque visual) ou padding limpo
        left_card = ttk.Frame(main_container, style="Card.TFrame", padding=25)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # Título Esquerda
        ttk.Label(left_card, text="Criar Cobrança", style="Header.TLabel").pack(anchor="w")
        ttk.Label(left_card, text="Preencha os dados para gerar o QR Code", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 20))

        # Botão Importar
        btn_import = ttk.Button(left_card, text="📋 Colar Pix Copia e Cola", style="Outline.TButton", cursor="hand2", command=self.abrir_caixa_importacao)
        btn_import.pack(fill=tk.X, pady=(0, 20), ipady=5)

        # Inputs
        self.create_label_entry(left_card, "Chave Pix (CPF, Email, Tel, Aleatória)", "entry_chave")
        self.create_label_entry(left_card, "Nome do Beneficiário", "entry_nome")
        self.create_label_entry(left_card, "Cidade do Beneficiário", "entry_cidade")
        self.create_label_entry(left_card, "Valor (R$) - Opcional", "entry_valor")
        self.create_label_entry(left_card, "Identificador (TxID) - Opcional", "entry_txid", default="***")

        # Botão Gerar
        tk.Label(left_card, bg=COLOR_CARD).pack(expand=True) # Espaçador
        btn_gerar = ttk.Button(left_card, text="GERAR QR CODE", style="Pix.TButton", cursor="hand2", command=self.gerar_pix)
        btn_gerar.pack(fill=tk.X, pady=10, ipady=8)

        # === CARD DIREITO (VISUALIZAÇÃO) ===
        right_card = ttk.Frame(main_container, style="Card.TFrame", padding=25)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_card, text="Seu Pix", style="Header.TLabel").pack(anchor="center")
        
        # Área da Imagem (com borda sutil)
        img_frame = tk.Frame(right_card, bg="#FAFAFA", highlightbackground="#E0E0E0", highlightthickness=1)
        img_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.lbl_img = tk.Label(img_frame, text="O QR Code aparecerá aqui", bg="#FAFAFA", fg="#999", font=("Segoe UI", 10))
        self.lbl_img.pack(fill=tk.BOTH, expand=True)

        # Botão Salvar
        self.btn_save = ttk.Button(right_card, text="⬇ Salvar Imagem", style="Outline.TButton", cursor="hand2", command=self.salvar_imagem, state="disabled")
        self.btn_save.pack(fill=tk.X, pady=(0, 15))

        # Copia e Cola
        ttk.Label(right_card, text="Código Copia e Cola:", style="TLabel").pack(anchor="w")
        self.txt_copia_cola = tk.Text(right_card, height=4, width=30, font=("Consolas", 9), 
                                      relief="flat", bg="#F4F4F4", highlightthickness=0, fg="#333")
        self.txt_copia_cola.pack(fill=tk.X, pady=(5, 0))

    def create_label_entry(self, parent, text, attr_name, default=""):
        lbl = ttk.Label(parent, text=text, font=("Segoe UI", 9, "bold"), foreground="#555")
        lbl.pack(anchor="w", pady=(10, 5))
        
        # Entry com padding interno visual
        entry = ttk.Entry(parent, font=("Segoe UI", 11))
        entry.pack(fill=tk.X, ipady=3) # ipady aumenta a altura do input
        if default:
            entry.insert(0, default)
        setattr(self, attr_name, entry)

    # --- LÓGICA (Mantida igual) ---
    def get_crc16(self, payload):
        payload += "6304"
        polinomio = 0x1021
        crc = 0xFFFF
        byte_data = payload.encode('utf-8')
        for byte in byte_data:
            crc ^= (byte << 8)
            for _ in range(8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ polinomio
                else:
                    crc = crc << 1
            crc &= 0xFFFF
        return f"{crc:04X}"

    def format_tlv(self, id, value):
        return f"{id}{len(value):02}{value}"

    def gerar_pix(self):
        chave = self.entry_chave.get().strip()
        nome = self.entry_nome.get().strip()
        cidade = self.entry_cidade.get().strip()
        valor = self.entry_valor.get().replace(',', '.').strip()
        txid = self.entry_txid.get().strip()

        if not chave or not nome or not cidade:
            messagebox.showwarning("Atenção", "Preencha a Chave Pix, Nome e Cidade para continuar.")
            return

        try:
            merchant_info = f"0014BR.GOV.BCB.PIX01{len(chave):02}{chave}"
            
            payload_parts = [
                self.format_tlv("00", "01"),
                self.format_tlv("26", merchant_info),
                self.format_tlv("52", "0000"),
                self.format_tlv("53", "986"),
            ]
            
            if valor:
                payload_parts.append(self.format_tlv("54", f"{float(valor):.2f}"))
            
            payload_parts.extend([
                self.format_tlv("58", "BR"),
                self.format_tlv("59", nome),
                self.format_tlv("60", cidade),
                self.format_tlv("62", self.format_tlv("05", txid or "***"))
            ])
            
            payload_str = "".join(payload_parts)
            crc = self.get_crc16(payload_str)
            full_code = f"{payload_str}6304{crc}"

            self.txt_copia_cola.delete(1.0, tk.END)
            self.txt_copia_cola.insert(tk.END, full_code)
            
            qr = qrcode.QRCode(box_size=10, border=1) # Borda menor pois já temos frame
            qr.add_data(full_code)
            qr.make(fit=True)
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            
            img_display = self.qr_image.resize((280, 280), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img_display)
            self.lbl_img.config(image=self.tk_img, text="", bg="white")
            self.btn_save.config(state="normal", style="Pix.TButton", text="⬇ Baixar QR Code") # Muda estilo ao ativar

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar: {str(e)}")

    def salvar_imagem(self):
        if self.qr_image:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png")],
                title="Salvar QR Code Pix"
            )
            if filename:
                self.qr_image.save(filename)
                messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")

    def abrir_caixa_importacao(self):
        raw_data = simpledialog.askstring("Importar Pix", "Cole o código Pix aqui:")
        if not raw_data: return

        raw_data = raw_data.strip().replace(" ", "").replace("\n", "").replace("\r", "")
        if not raw_data.startswith("000201"):
            messagebox.showerror("Inválido", "O código deve começar com 000201.")
            return
        self.processar_importacao(raw_data)

    def processar_importacao(self, raw_data):
        try:
            data_map = {}
            i = 0
            while i < len(raw_data):
                try:
                    p_id = raw_data[i:i+2]
                    p_len = int(raw_data[i+2:i+4])
                    p_val = raw_data[i+4:i+4+p_len]
                    data_map[p_id] = p_val
                    i += 4 + p_len
                except ValueError: break

            self.entry_nome.delete(0, tk.END); self.entry_nome.insert(0, data_map.get('59', ''))
            self.entry_cidade.delete(0, tk.END); self.entry_cidade.insert(0, data_map.get('60', ''))
            val = data_map.get('54', '')
            self.entry_valor.delete(0, tk.END); self.entry_valor.insert(0, val)

            if '26' in data_map:
                sub_26 = data_map['26']
                k = 0
                while k < len(sub_26):
                    try:
                        k_id = sub_26[k:k+2]; k_len = int(sub_26[k+2:k+4]); k_val = sub_26[k+4:k+4+k_len]
                        if k_id == '01':
                            self.entry_chave.delete(0, tk.END); self.entry_chave.insert(0, k_val); break
                        k += 4 + k_len
                    except: break

            if '62' in data_map:
                sub_62 = data_map['62']
                k = 0
                while k < len(sub_62):
                    try:
                        k_id = sub_62[k:k+2]; k_len = int(sub_62[k+2:k+4]); k_val = sub_62[k+4:k+4+k_len]
                        if k_id == '05':
                            self.entry_txid.delete(0, tk.END); self.entry_txid.insert(0, k_val); break
                        k += 4 + k_len
                    except: break
            
            self.gerar_pix()
            messagebox.showinfo("Sucesso", "Pix importado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Não foi possível ler o código: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixApp(root)
    root.mainloop()