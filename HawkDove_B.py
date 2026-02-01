import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
W0 = 3
V = 2
C = 6
E = np.array([[(V-C)/2, V], 
              [0,       V/2]])

T_final = 100
p0 = 0.90 # proporção inicial de falcões

# Inicialização da matriz (2 linhas, T_final colunas)
p = np.zeros((2, T_final)) 
# Linha 0: Falcão, Linha 1: Pombo (Python começa em 0)
p[0, 0] = p0
p[1, 0] = 1 - p0

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
plt.title('Dinâmica do Replicador (Hawk vs Dove)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()