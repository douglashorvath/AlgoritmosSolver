import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpVariable, value

# Configurações de faixa para as variáveis base
base_prices = range(50, 201, 10)  # Intervalo de preços base de 50 a 200 com passo de 10
infrastructure_costs = range(50, 201, 10)  # Intervalo de custos base de infraestrutura de 50 a 200 com passo de 10

# Armazenar os lucros líquidos para cada variação
net_profits_infrastructure = []
net_profits_price = []

# Análise com base_price fixo e variação de base_infrastructure_cost
fixed_base_price = 100
for base_infrastructure_cost in infrastructure_costs:
    # Configurações dos preços dos pacotes
    xb_price = fixed_base_price
    xp_price = 2 * fixed_base_price
    xg_price = 3 * fixed_base_price

    # Configurações dos custos de infraestrutura
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

    # Armazenar o lucro líquido para esta configuração
    if model.status == 1:  # Solução ótima encontrada
        net_profits_infrastructure.append(value(model.objective))
    else:
        net_profits_infrastructure.append(0)  # Nenhuma solução encontrada para esta configuração

# Análise com base_infrastructure_cost fixo e variação de base_price
fixed_base_infrastructure_cost = 100
for base_price in base_prices:
    # Configurações dos preços dos pacotes
    xb_price = base_price
    xp_price = 2 * base_price
    xg_price = 3 * base_price

    # Configurações dos custos de infraestrutura
    xb_infrastructure_cost = fixed_base_infrastructure_cost
    xp_infrastructure_cost = 1.5 * fixed_base_infrastructure_cost
    xg_infrastructure_cost = 2 * fixed_base_infrastructure_cost

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

    # Armazenar o lucro líquido para esta configuração
    if model.status == 1:  # Solução ótima encontrada
        net_profits_price.append(value(model.objective))
    else:
        net_profits_price.append(0)  # Nenhuma solução encontrada para esta configuração

# Plotar os gráficos de linha
plt.figure(figsize=(12, 6))

# Gráfico 1: Variação do Lucro Líquido com o Custo de Infraestrutura Base
plt.subplot(1, 2, 1)
plt.plot(infrastructure_costs, net_profits_infrastructure, marker='o')
plt.xlabel("Custo de Infraestrutura Base")
plt.ylabel("Lucro Líquido")
plt.title("Lucro Líquido vs Custo de Infraestrutura Base")

# Gráfico 2: Variação do Lucro Líquido com o Preço Base
plt.subplot(1, 2, 2)
plt.plot(base_prices, net_profits_price, marker='o', color='orange')
plt.xlabel("Preço Base")
plt.ylabel("Lucro Líquido")
plt.title("Lucro Líquido vs Preço Base")

plt.tight_layout()
plt.show()
