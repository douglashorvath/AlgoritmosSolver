import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pulp import LpMaximize, LpProblem, LpVariable, value

# Definir intervalos para preço base e custo de infraestrutura base
base_prices = np.arange(50, 201, 10)  # Preço base de 50 a 200
infrastructure_costs = np.arange(50, 201, 10)  # Custo de infraestrutura base de 50 a 200

# Matrizes para armazenar os lucros para as combinações de preço base e custo de infraestrutura
profits = np.zeros((len(base_prices), len(infrastructure_costs)))

# Loop sobre todas as combinações de preço base e custo de infraestrutura base
for i, base_price in enumerate(base_prices):
    for j, base_infrastructure_cost in enumerate(infrastructure_costs):
        # Preços dos pacotes com base no preço base atual
        xb_price = base_price
        xp_price = 2 * base_price
        xg_price = 3 * base_price

        # Custos de infraestrutura dos pacotes com base no custo de infraestrutura atual
        xb_infrastructure_cost = base_infrastructure_cost
        xp_infrastructure_cost = 1.5 * base_infrastructure_cost
        xg_infrastructure_cost = 2 * base_infrastructure_cost

        # Definir o problema de maximização do lucro
        model = LpProblem(name="maximize-profit", sense=LpMaximize)

        # Variáveis de decisão para as quantidades de pacotes vendidas
        q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")
        q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
        q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")

        # Cálculo do custo total de infraestrutura com as variáveis de quantidade
        total_infrastructure_cost = (
            q_basic * xb_infrastructure_cost +
            q_standard * xp_infrastructure_cost +
            q_premium * xg_infrastructure_cost
        )

        # Definir a função objetivo (Maximizar o lucro líquido: lucro total - custo de infraestrutura)
        model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price) - total_infrastructure_cost, "Net Profit"

        # Restrições de capacidade
        model += (1 * q_basic + 2 * q_standard + 3 * q_premium) <= 300  # Horas de processamento
        model += (2 * q_basic + 3 * q_standard + 4 * q_premium) <= 450  # Capacidade de armazenamento

        # Limite para o custo de infraestrutura total (restrição de orçamento)
        model += total_infrastructure_cost <= 150000

        # Resolver o problema
        model.solve()

        # Armazenar o lucro para esta combinação
        if model.status == 1:  # Solução ótima encontrada
            profits[i, j] = value(model.objective)
        else:
            profits[i, j] = 0  # Nenhuma solução encontrada para esta configuração

# Plotar o gráfico de superfície 3D
X, Y = np.meshgrid(base_prices, infrastructure_costs)
Z = profits.T  # Transpor para alinhar as dimensões

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k')

# Personalizar o gráfico
ax.set_xlabel("Preço Base")
ax.set_ylabel("Custo de Infraestrutura Base")
ax.set_zlabel("Lucro Máximo")
ax.set_title("Impacto do Preço Base e Custo de Infraestrutura Base no Lucro Máximo")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label="Lucro Máximo")
plt.show()
