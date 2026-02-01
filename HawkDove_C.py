import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
W0 = 3
# Matriz da letra C: H, D, R
E = np.array([[-0.5, 2.0, -0.5],
              [ 0.0, 1.0,  0.9],
              [-0.5, 1.1,  1.0]])

T_final = 100
p0 = 0.33 # proporção inicial de falcões
p1 = 0.33 # proporção inicial de pombos

# Inicialização da matriz (3 linhas, T_final colunas)
p = np.zeros((3, T_final)) 
# Linha 0: Falcão, Linha 1: Pombo, Linha 2: Retaliador
p[0, 0] = p0
p[1, 0] = p1
p[2, 0] = 1 - p0 - p1

# Loop
for t in range(1, T_final):
    p_atual = p[:, t-1]
    
    # Esperança no ganho do fitness para cada "espécie"
    # MATLAB: E * p_atual  -> Python: E @ p_atual
    ########  ALTERE A LINHA ABAIXO. ELA ESTA ERRADA #########
    ganho = E @ p_atual
    
    # Esperança do fitness para cada espécie (Baseline + Ganho)
    # Python entende W0 + vetor e soma W0 em todos os elementos (broadcasting)
    w = W0 + ganho
    
    # Fitness médio da população
    # MATLAB: w' * p_atual -> Python: w @ p_atual (produto escalar de vetores 1D)
    w_med = w @ p_atual
    
    # Atualizando a proporção de cada espécie
    # se o fitness for superior ao fitness médio, a proporção aumenta.
    # se o fitness for inferior ao fitness médio, a proporção diminui.

    ########  ALTERE A LINHA ABAIXO.  ELA ESTA ERRADA #########
    p[:, t] = p_atual * (w / w_med)

# Plotagem
plt.figure(figsize=(10, 6))
plt.plot(p[0, :], 'b', label='Falcão')
plt.plot(p[1, :], 'r', label='Pombo')
plt.plot(p[2, :], 'g', label='Retaliador')
plt.title('Dinâmica do Replicador (H vs D vs R)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()