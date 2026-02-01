import tkinter as tk
from tkinter import messagebox
import random

class JogoNim:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo Nim - Configurável")
        self.mostrar_menu_configuracao()

    def mostrar_menu_configuracao(self):
        # --- TELA DE CONFIGURAÇÃO ---
        
        # Frame para organizar o layout
        self.frame_config = tk.Frame(self.root, padx=20, pady=20)
        self.frame_config.pack()

        # Título
        tk.Label(self.frame_config, text="Configurações do Jogo", font=("Arial", 16, "bold")).pack(pady=10)

        # 1. Input: Número de Palitos
        tk.Label(self.frame_config, text="Número Inicial de Palitos:").pack()
        self.entry_total = tk.Entry(self.frame_config)
        self.entry_total.insert(0, "13") # Valor padrão
        self.entry_total.pack(pady=5)

        # 2. Input: Máximo de Retirada
        tk.Label(self.frame_config, text="Máximo de palitos por jogada:").pack()
        self.entry_max = tk.Entry(self.frame_config)
        self.entry_max.insert(0, "3") # Valor padrão
        self.entry_max.pack(pady=5)

        # 3. Radio: Quem começa
        tk.Label(self.frame_config, text="Quem começa jogando?").pack(pady=5)
        self.var_quem_comeca = tk.StringVar(value="humano")
        
        frame_radio = tk.Frame(self.frame_config)
        frame_radio.pack()
        tk.Radiobutton(frame_radio, text="Humano", variable=self.var_quem_comeca, value="humano").pack(side="left", padx=10)
        tk.Radiobutton(frame_radio, text="Computador", variable=self.var_quem_comeca, value="computador").pack(side="left", padx=10)

        # Botão Iniciar
        btn_iniciar = tk.Button(self.frame_config, text="INICIAR JOGO", command=self.iniciar_jogo, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        btn_iniciar.pack(pady=20)

    def iniciar_jogo(self):
        # Validação dos dados inseridos
        try:
            self.total_palitos = int(self.entry_total.get())
            self.max_retirada = int(self.entry_max.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira apenas números inteiros.")
            return

        if self.total_palitos < 1 or self.max_retirada < 1:
            messagebox.showerror("Erro", "Os números devem ser maiores que zero.")
            return

        quem = self.var_quem_comeca.get()
        self.turno_jogador = True if quem == "humano" else False

        # Remove a tela de configuração e monta a tela do jogo
        self.frame_config.destroy()
        self.montar_tela_jogo()

        # Se o computador começa, já faz a jogada dele
        if not self.turno_jogador:
            self.root.after(1000, self.jogada_computador)

    def montar_tela_jogo(self):
        # --- TELA DO JOGO (Igual à anterior, mas adaptada) ---
        
        self.palitos_selecionados = []
        
        # Texto Informativo
        self.lbl_info = tk.Label(self.root, text=f"Restam {self.total_palitos} palitos.", font=("Arial", 14))
        self.lbl_info.pack(pady=10)
        
        self.lbl_vez = tk.Label(self.root, text="Sua vez!" if self.turno_jogador else "Vez do Computador...", fg="blue")
        self.lbl_vez.pack()

        # Canvas
        self.canvas = tk.Canvas(self.root, width=800, height=200, bg="white")
        self.canvas.pack()

        # Botão Confirmar
        self.btn_confirmar = tk.Button(self.root, text="Confirmar Jogada", command=self.confirmar_jogada, state="normal" if self.turno_jogador else "disabled")
        self.btn_confirmar.pack(pady=20)

        self.desenhar_palitos()

    def desenhar_palitos(self):
        self.canvas.delete("all")
        self.palitos_selecionados = []
        
        # Cálculo dinâmico para caber na tela se houver muitos palitos
        largura_tela = 800
        margem = 50
        espaco_disponivel = largura_tela - (2 * margem)
        
        # Tamanho do palito e espaçamento se ajustam conforme a quantidade
        if self.total_palitos > 0:
            largura_palito = min(20, espaco_disponivel // (self.total_palitos * 2))
            espacamento = espaco_disponivel // self.total_palitos
        else:
            largura_palito = 20
            espacamento = 40

        for i in range(self.total_palitos):
            x1 = margem + (i * espacamento)
            y1 = 50
            x2 = x1 + largura_palito
            y2 = 150
            
            # Tag 'palito_i' ajuda a saber qual index é qual
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black", tags=("palito", f"p{i}"))

        self.canvas.tag_bind("palito", "<Button-1>", self.clicar_palito)
        self.lbl_info.config(text=f"Restam {self.total_palitos} palitos. (Tire 1 a {self.max_retirada})")

    def clicar_palito(self, event):
        if not self.turno_jogador: return

        item_id = self.canvas.find_closest(event.x, event.y)[0]
        
        if item_id in self.palitos_selecionados:
            self.palitos_selecionados.remove(item_id)
            self.canvas.itemconfig(item_id, fill="orange")
        else:
            if len(self.palitos_selecionados) < self.max_retirada:
                self.palitos_selecionados.append(item_id)
                self.canvas.itemconfig(item_id, fill="red")
            else:
                messagebox.showwarning("Aviso", f"O máximo permitido é {self.max_retirada} palitos!")

    def confirmar_jogada(self):
        qtd = len(self.palitos_selecionados)
        if qtd == 0:
            messagebox.showinfo("Aviso", "Selecione pelo menos 1 palito.")
            return

        self.processar_retirada(qtd)

    def processar_retirada(self, qtd):
        self.total_palitos -= qtd
        self.desenhar_palitos()

        # Verifica Vitória/Derrota
        if self.total_palitos == 0:
            vencedor = "Computador" if self.turno_jogador else "Você"
            msg = f"O último palito foi retirado.\nVencedor: {vencedor}!"
            messagebox.showinfo("Fim de Jogo", msg)
            self.root.destroy()
            return

        # Troca o turno
        self.turno_jogador = not self.turno_jogador
        
        if self.turno_jogador:
            self.lbl_vez.config(text="Sua vez!", fg="blue")
            self.btn_confirmar.config(state="normal")
        else:
            self.lbl_vez.config(text="Vez do Computador...", fg="red")
            self.btn_confirmar.config(state="disabled")
            self.root.after(1000, self.jogada_computador)

    def jogada_computador(self):
        # Aqui é definida a estratégia do computador
        
        k = self.max_retirada # escolhido pelo usuário
        palitos_restantes = self.total_palitos
        
        # Estratégia Vencedora
        tirar = (palitos_restantes - 1) % (k + 1)
        # Caso esteja em uma posição ruim, o computador tirará o mínimo de palitos
        if tirar == 0:
            tirar = 1

        messagebox.showinfo("Computador", f"O computador retirou {tirar} palito(s).")
        self.processar_retirada(tirar)

# Inicialização
if __name__ == "__main__":
    root = tk.Tk()
    app = JogoNim(root)
    root.mainloop()