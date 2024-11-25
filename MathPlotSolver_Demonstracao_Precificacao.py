import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, value

# Definir faixa para preços possíveis
basic_prices = np.arange(50, 201, 10)  # Preços possíveis para o Básico
standard_prices = np.arange(60, 301, 10)  # Preços possíveis para o Padrão
premium_prices = np.arange(70, 401, 10)  # Preços possíveis para o Premium

# Constantes de demanda base para cada pacote (ajustável)
basic_demand_base = 100
standard_demand_base = 80
premium_demand_base = 50

# Listas para armazenar os resultados
basic_sales = []
standard_sales = []
premium_sales = []
profits = []
price_combinations = []

# Loop para testar diferentes combinações de preços
for xb_price in basic_prices:
    for xp_price in standard_prices:
        if xp_price <= xb_price:  # Garantir que o Padrão seja maior que o Básico
            continue
        for xg_price in premium_prices:
            if xg_price <= xp_price:  # Garantir que o Premium seja maior que o Padrão
                continue

            # Demanda ajustada com base no preço (inversamente proporcional)
            basic_demand = max(basic_demand_base - 0.5 * xb_price, 0)
            standard_demand = max(standard_demand_base - 0.3 * xp_price, 0)
            premium_demand = max(premium_demand_base - 0.2 * xg_price, 0)

            # Definir o problema de maximização do lucro
            model = LpProblem(name="maximize-profit", sense=LpMaximize)

            # Variáveis de decisão para as quantidades de pacotes vendidas
            q_basic = LpVariable("q_basic", lowBound=0, upBound=basic_demand, cat="Integer")
            q_standard = LpVariable("q_standard", lowBound=0, upBound=standard_demand, cat="Integer")
            q_premium = LpVariable("q_premium", lowBound=0, upBound=premium_demand, cat="Integer")

            # Definir a função objetivo (Maximizar o lucro total)
            model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price), "Total Profit"

            # Restrições simplificadas para horas de processamento e armazenamento
            model += (1 * q_basic + 1 * q_standard + 1 * q_premium) <= 300  # Total de horas de processamento
            model += (1 * q_basic + 1 * q_standard + 1 * q_premium) <= 450  # Total de capacidade de armazenamento

            # Resolver o problema
            model.solve()

            # Armazenar os resultados se a solução for ótima
            if model.status == 1:
                basic = q_basic.value()
                standard = q_standard.value()
                premium = q_premium.value()
                profit = value(model.objective)
                basic_sales.append(basic)
                standard_sales.append(standard)
                premium_sales.append(premium)
                profits.append(profit)
                price_combinations.append((xb_price, xp_price, xg_price))

# Encontrar o ponto de equilíbrio (menor diferença nas vendas)
differences = [abs(b - s) + abs(s - p) + abs(b - p) for b, s, p in zip(basic_sales, standard_sales, premium_sales)]
min_diff_index = np.argmin(differences)

# Obter a combinação de preços e vendas correspondentes
best_prices = price_combinations[min_diff_index]
best_sales = (basic_sales[min_diff_index], standard_sales[min_diff_index], premium_sales[min_diff_index])
best_profit = profits[min_diff_index]

# Exibir os resultados
print("Preços que equilibram as vendas:")
print(f"Preço do Básico: {best_prices[0]}, Padrão: {best_prices[1]}, Premium: {best_prices[2]}")
print("Vendas equilibradas:")
print(f"Básico: {best_sales[0]}, Padrão: {best_sales[1]}, Premium: {best_sales[2]}")
print(f"Lucro Máximo: {best_profit}")

# Plotar os resultados
plt.figure(figsize=(12, 6))

# Gráfico 1: Quantidades vendidas
plt.subplot(1, 2, 1)
plt.scatter(range(len(basic_sales)), basic_sales, label="Básico", marker="o")
plt.scatter(range(len(standard_sales)), standard_sales, label="Padrão", marker="o")
plt.scatter(range(len(premium_sales)), premium_sales, label="Premium", marker="o")
plt.xlabel("Configuração de Preço")
plt.ylabel("Quantidade Vendida")
plt.title("Vendas por Configuração de Preços")
plt.legend()

# Gráfico 2: Lucro máximo
plt.subplot(1, 2, 2)
plt.scatter(range(len(profits)), profits, label="Lucro", marker="o", color="green")
plt.xlabel("Configuração de Preço")
plt.ylabel("Lucro Máximo")
plt.title("Lucro Máximo por Configuração de Preços")
plt.legend()

plt.tight_layout()
plt.show()
