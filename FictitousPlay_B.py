import numpy as np
import matplotlib.pyplot as plt

######################  Par ou Ímpar
# Matriz de Payoff do Jogador 1 (A)
A = np.array([[ 1, -1],   # Par
              [-1,  1]])  # Ímpar

# Matriz de Payoff do Jogador 2 (B) - Jogo de Soma Zero
B = -A 
##################### Batalha dos Sexos
#A = np.array([[2, 0],   # (Futebol, Futebol), (Futebol, Balé)
#               [1, 3]])  # (Balé, Futebol),     (Balé, Balé)
#B = np.array([[3, 1],   # (Futebol, Futebol), (Futebol, Balé)
#               [0, 2]])  # (Balé, Futebol),     (Balé, Balé)

#-------------------------------------------

T_final = 2000  # Número de rodadas

# 2. Inicialização das Crenças (Histórico)
# Começamos com uma contagem fictícia inicial para evitar divisão por zero
# [Qtd Estratégia 1, Qtd Estratégia 2]
contagem_p1 = np.array([1.0, 2.0]) 
contagem_p2 = np.array([1.0, 2.0])

# Para guardar o histórico das probabilidades (para o gráfico)
hist_prob_p1 = np.zeros((2, T_final)) # Probabilidade empírica do Jogador 1 jogar Estratégia 1/2
hist_prob_p2 = np.zeros((2, T_final)) # Probabilidade empírica do Jogador 2 jogar Cara/Coroa

# 3. Loop do Jogo (Aprendizado)
for t in range(T_final):
    
    # --- Passo A: Calcular Crenças (Probabilidades Empíricas) ---
    # "O que eu acho que o outro vai jogar com base no passado?"
    crenca_sobre_p2 = contagem_p2 / np.sum(contagem_p2)
    crenca_sobre_p1 = contagem_p1 / np.sum(contagem_p1)
    
    # --- Passo B: Calcular Melhor Resposta (Best Response) ---
    # Jogador 1 calcula seu ganho esperado contra a crença sobre P2
    # Ganho esperado = Matriz A * Vetor de Crença
    eu_p1 = A @ crenca_sobre_p2
    ######## ALTERE A LINHA ABAIXO. ELA ESTA ERRADA #########
    melhor_resposta_p1 = np.argmax(eu_p1)
    
    # Jogador 2 calcula seu ganho esperado contra a crença sobre P1
    eu_p2 = B.T @ crenca_sobre_p1 # Transposta porque P2 é coluna
    ######## ALTERE A LINHA ABAIXO. ELA ESTA ERRADA #########
    melhor_resposta_p2 = np.argmax(eu_p2)
    

    # --- Passo C: Atualizar Histórico (O Jogo Acontece) ---
    # Adicionamos +1 na contagem da jogada que foi escolhida
    contagem_p1[melhor_resposta_p1] += 1
    contagem_p2[melhor_resposta_p2] += 1
    
    # Guardar os dados para o gráfico (frequência acumulada)
    hist_prob_p1[:, t] = contagem_p1 / np.sum(contagem_p1)
    hist_prob_p2[:, t] = contagem_p2 / np.sum(contagem_p2)

# 4. Plotagem dos Resultados
plt.figure(figsize=(10, 6))

# Plotando a probabilidade de jogar "Cara" (Estratégia 0) para ambos
plt.plot(hist_prob_p1[0, :], label='Freq. Histórica P1 (Jogar Cara)', color='blue')
plt.plot(hist_prob_p2[0, :], label='Freq. Histórica P2 (Jogar Cara)', color='red')

plt.title('Fictitious Play')
plt.xlabel('Rodadas')
plt.ylabel('Probabilidade Empírica de Jogar Estratégia 1')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 1)
plt.show()