import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, value

# Definir faixa para horas de processamento base
base_hours = np.arange(1, 11, 1)  # Horas base de 1 a 10, com passo de 1

# Listas para armazenar os resultados
basic_sales = []
standard_sales = []
premium_sales = []
profits = []

# Loop para testar diferentes valores de horas de processamento
for xb_process in base_hours:
    xp_process = 2 * xb_process  # Padrão usa o dobro do Básico
    xg_process = 3 * xb_process  # Premium usa o triplo do Básico

    # Preços fixos dos pacotes
    base_price = 100
    xb_price = base_price
    xp_price = 2 * base_price
    xg_price = 3 * base_price

    # Custos de infraestrutura (fixos para este teste)
    xb_infrastructure_cost = 100
    xp_infrastructure_cost = 1.5 * 100
    xg_infrastructure_cost = 2 * 100

    # Definir o problema de maximização do lucro
    model = LpProblem(name="maximize-profit", sense=LpMaximize)

    # Variáveis de decisão para as quantidades de pacotes vendidas
    q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")
    q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
    q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")

    # Definir a função objetivo (Maximizar o lucro total)
    model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price), "Total Profit"

    # Restrições de capacidade ajustadas para horas de processamento
    model += (xb_process * q_basic + xp_process * q_standard + xg_process * q_premium) <= 300  # Horas de processamento
    model += (2 * q_basic + 3 * q_standard + 4 * q_premium) <= 450  # Capacidade de armazenamento

    # Resolver o problema
    model.solve()

    # Armazenar os resultados se a solução for ótima
    if model.status == 1:
        basic_sales.append(q_basic.value())
        standard_sales.append(q_standard.value())
        premium_sales.append(q_premium.value())
        profits.append(value(model.objective))
    else:
        basic_sales.append(0)
        standard_sales.append(0)
        premium_sales.append(0)
        profits.append(0)

# Plotar os resultados
plt.figure(figsize=(14, 7))

# Plotar vendas equilibradas
plt.subplot(1, 2, 1)
plt.plot(base_hours, basic_sales, label="Básico", marker="o")
plt.plot(base_hours, standard_sales, label="Padrão", marker="o")
plt.plot(base_hours, premium_sales, label="Premium", marker="o")
plt.xlabel("Horas de Processamento por Pacote Básico")
plt.ylabel("Quantidade Vendida")
plt.title("Equilíbrio nas Vendas vs Horas de Processamento")
plt.legend()

# Plotar lucro correspondente
plt.subplot(1, 2, 2)
plt.plot(base_hours, profits, label="Lucro", marker="o", color="green")
plt.xlabel("Horas de Processamento por Pacote Básico")
plt.ylabel("Lucro Máximo")
plt.title("Lucro vs Horas de Processamento por Pacote Básico")
plt.legend()

plt.tight_layout()
plt.show()
