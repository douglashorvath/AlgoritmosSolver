import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpVariable, value

# Configurações de faixa para o custo de infraestrutura base
base_infrastructure_costs = range(50, 201, 10)  # Intervalo de custos base de infraestrutura de 50 a 200 com passo de 10

# Listas para armazenar os lucros para cada tipo de produto
profits_infrastructure_basic = []
profits_infrastructure_standard = []
profits_infrastructure_premium = []

# Análise de sensibilidade: variando o custo de infraestrutura do Pacote Básico
fixed_base_price = 100
for base_infrastructure_cost in base_infrastructure_costs:
    # Preços dos pacotes fixos
    xb_price = fixed_base_price
    xp_price = 2 * fixed_base_price
    xg_price = 3 * fixed_base_price

    # Custos de infraestrutura variando apenas para o Pacote Básico
    xb_infrastructure_cost = base_infrastructure_cost
    xp_infrastructure_cost = 1.5 * 100  # Fixando o custo de infraestrutura do Padrão
    xg_infrastructure_cost = 2 * 100  # Fixando o custo de infraestrutura do Premium

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

    # Armazenar o lucro para esta configuração
    profits_infrastructure_basic.append(value(model.objective) if model.status == 1 else 0)

# Repetir a análise de sensibilidade para o custo de infraestrutura do Pacote Padrão
for base_infrastructure_cost in base_infrastructure_costs:
    xb_infrastructure_cost = 100  # Fixando o custo de infraestrutura do Básico
    xp_infrastructure_cost = base_infrastructure_cost
    xg_infrastructure_cost = 2 * 100  # Fixando o custo de infraestrutura do Premium

    model = LpProblem(name="maximize-profit", sense=LpMaximize)
    q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")
    q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
    q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")
    
    total_infrastructure_cost = (
        q_basic * xb_infrastructure_cost +
        q_standard * xp_infrastructure_cost +
        q_premium * xg_infrastructure_cost
    )

    model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price) - total_infrastructure_cost, "Net Profit"
    model += (1 * q_basic + 2 * q_standard + 3 * q_premium) <= 300
    model += (2 * q_basic + 3 * q_standard + 4 * q_premium) <= 450
    model += total_infrastructure_cost <= 150000

    model.solve()
    profits_infrastructure_standard.append(value(model.objective) if model.status == 1 else 0)

# Repetir a análise de sensibilidade para o custo de infraestrutura do Pacote Premium
for base_infrastructure_cost in base_infrastructure_costs:
    xb_infrastructure_cost = 100  # Fixando o custo de infraestrutura do Básico
    xp_infrastructure_cost = 1.5 * 100  # Fixando o custo de infraestrutura do Padrão
    xg_infrastructure_cost = base_infrastructure_cost

    model = LpProblem(name="maximize-profit", sense=LpMaximize)
    q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")
    q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
    q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")
    
    total_infrastructure_cost = (
        q_basic * xb_infrastructure_cost +
        q_standard * xp_infrastructure_cost +
        q_premium * xg_infrastructure_cost
    )

    model += (q_basic * xb_price + q_standard * xp_price + q_premium * xg_price) - total_infrastructure_cost, "Net Profit"
    model += (1 * q_basic + 2 * q_standard + 3 * q_premium) <= 300
    model += (2 * q_basic + 3 * q_standard + 4 * q_premium) <= 450
    model += total_infrastructure_cost <= 150000

    model.solve()
    profits_infrastructure_premium.append(value(model.objective) if model.status == 1 else 0)

# Plotar os gráficos de linha para cada tipo de pacote com variação do custo de infraestrutura
plt.figure(figsize=(10, 6))
plt.plot(base_infrastructure_costs, profits_infrastructure_basic, label="Lucro vs Custo Infraestrutura Básico", marker='o')
plt.plot(base_infrastructure_costs, profits_infrastructure_standard, label="Lucro vs Custo Infraestrutura Padrão", marker='o')
plt.plot(base_infrastructure_costs, profits_infrastructure_premium, label="Lucro vs Custo Infraestrutura Premium", marker='o')
plt.xlabel("Custo de Infraestrutura Base")
plt.ylabel("Lucro Máximo")
plt.title("Variação do Lucro Máximo com Custo de Infraestrutura de Cada Pacote")
plt.legend()
plt.show()
