import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, value

# Preços fixos dos pacotes
xb_price = 1000
xp_price = 2000
xg_price = 3000

# Faixa de valores para as horas de processamento
basic_hours = np.arange(1, 11, 1)  # Horas para o Básico (1 a 10)
standard_hours = np.arange(2, 21, 1)  # Horas para o Padrão (2 a 20)
premium_hours = np.arange(3, 31, 1)  # Horas para o Premium (3 a 30)

# Listas para armazenar os resultados
basic_sales = []
standard_sales = []
premium_sales = []
profits = []
hours_combinations = []

# Loop para testar diferentes combinações de horas de processamento
for xb_process in basic_hours:
    for xp_process in standard_hours:
        if xp_process <= xb_process:  # Garantir que o Padrão consuma mais que o Básico
            continue
        for xg_process in premium_hours:
            if xg_process <= xp_process:  # Garantir que o Premium consuma mais que o Padrão
                continue

            # Definir o problema de maximização do lucro
            model = LpProblem(name="maximize-profit", sense=LpMaximize)

            # Variáveis de decisão para as quantidades de pacotes vendidas
            q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")
            q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
            q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")

            # Definir a função objetivo (Maximizar o lucro total)
            model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price), "Total Profit"

            # Restrições para horas de processamento e armazenamento (simplificadas)
            model += (xb_process * q_basic + xp_process * q_standard + xg_process * q_premium) <= 300  # Total de horas de processamento
            model += (1 * q_basic + 1 * q_standard + 1 * q_premium) <= 450  # Total de capacidade de armazenamento

            # Resolver o problema
            model.solve()

            # Calcular total de horas manualmente e filtrar valores inválidos
            if model.status == 1:
                basic = q_basic.value()
                standard = q_standard.value()
                premium = q_premium.value()
                total_hours = xb_process * basic + xp_process * standard + xg_process * premium

                if total_hours <= 300:  # Garantir que respeita o limite
                    profit = value(model.objective)
                    basic_sales.append(basic)
                    standard_sales.append(standard)
                    premium_sales.append(premium)
                    profits.append(profit)
                    hours_combinations.append((xb_process, xp_process, xg_process))

# Encontrar o ponto de equilíbrio (menor diferença nas vendas)
differences = [abs(b - s) + abs(s - p) + abs(b - p) for b, s, p in zip(basic_sales, standard_sales, premium_sales)]
min_diff_index = np.argmin(differences)

# Obter a combinação de horas e vendas correspondentes
best_hours = hours_combinations[min_diff_index]
best_sales = (basic_sales[min_diff_index], standard_sales[min_diff_index], premium_sales[min_diff_index])
best_profit = profits[min_diff_index]

# Exibir os resultados
print("Horas de Processamento que equilibram as vendas:")
print(f"Básico: {best_hours[0]}, Padrão: {best_hours[1]}, Premium: {best_hours[2]}")
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
plt.xlabel("Configuração de Horas de Processamento")
plt.ylabel("Quantidade Vendida")
plt.title("Vendas por Configuração de Horas de Processamento")
plt.legend()

# Gráfico 2: Lucro máximo
plt.subplot(1, 2, 2)
plt.scatter(range(len(profits)), profits, label="Lucro", marker="o", color="green")
plt.xlabel("Configuração de Horas de Processamento")
plt.ylabel("Lucro Máximo")
plt.title("Lucro Máximo por Configuração de Horas de Processamento")
plt.legend()

plt.tight_layout()
plt.show()
