from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Variáveis de configuração
base_price = 100  # Preço base para o Pacote Básico
base_infrastructure_cost = 100  # Custo de infraestrutura base para o Pacote Básico
xb_process = 1 # Índice calculo do valor do processamento do xb
xp_process = 2 # Índice calculo do valor do processamento do xp
xg_process = 3 # Índice calculo do valor do processamento do xg
xb_drive = 2 # Índice calculo do valor do armazenamento do xb
xp_drive = 3 # Índice calculo do valor do armazenamento do xp
xg_drive = 4 # Índice calculo do valor do armazenamento do xg

# Preços dos pacotes
xb_price = base_price # Preço base para calculo
xp_price = 2 * base_price  # Pacote Padrão custa 2x o Pacote Básico
xg_price = 3 * base_price  # Pacote Premium custa 3x o Pacote Básico

# Custos de infraestrutura dos pacotes
xb_infrastructure_cost = base_infrastructure_cost
xp_infrastructure_cost = 1.5 * base_infrastructure_cost  # Pacote Padrão custa 1.5x o Pacote Básico
xg_infrastructure_cost = 2 * base_infrastructure_cost    # Pacote Premium custa 2x o Pacote Básico

# Definir o problema de maximização do lucro
model = LpProblem(name="maximize-profit", sense=LpMaximize)

# Variáveis de decisão para as quantidades de pacotes vendidas
q_basic = LpVariable("q_basic", lowBound=30, cat="Integer")  # Demanda mínima de 30 pacotes básicos
q_standard = LpVariable("q_standard", lowBound=0, cat="Integer")
q_premium = LpVariable("q_premium", lowBound=0, upBound=15, cat="Integer")  # Máximo de 15 pacotes premium

# Definir a função objetivo (Maximizar o lucro total com as quantidades e preços)
model += q_basic * xb_price + q_standard * xp_price + q_premium * xg_price, "Total Profit"

# Restrições de capacidade
model += (xb_process * q_basic + xp_process * q_standard + xg_process * q_premium) <= 300  # Horas de processamento
model += (xb_drive * q_basic + xp_drive * q_standard + xg_drive * q_premium) <= 450  # Capacidade de armazenamento

# Restrição de custo de infraestrutura total
total_infrastructure_cost = (
    q_basic * xb_infrastructure_cost +
    q_standard * xp_infrastructure_cost +
    q_premium * xg_infrastructure_cost
)
model += total_infrastructure_cost <= 150000

# Resolver o problema
model.solve()

# Exibir os melhores resultados encontrados
if model.status == 1:  # Status 1 significa que foi encontrada uma solução ótima
    print("Lucro Máximo:", model.objective.value())
    print("Melhor Configuração de Preços e Quantidades:")
    print("Preço do Pacote Básico (xb):", xb_price)
    print("Preço do Pacote Padrão (xp):", xp_price)
    print("Preço do Pacote Premium (xg):", xg_price)
    print("Quantidades Vendidas - Básico:", q_basic.value(), 
          "Padrão:", q_standard.value(), 
          "Premium:", q_premium.value())
else:
    print("Não foi encontrada uma solução que satisfaça todas as restrições.")
