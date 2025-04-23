import json
import urllib.request
from datetime import datetime

# Preços base das cores dos cristais
precos_cores = {
    "01": ("azul", 99.90),
    "02": ("verde", 199.90),
    "03": ("rosa", 31.90),
    "04": ("roxo", 5.00),
    "05": ("vermelho", 31.90),
    "06": ("branco", 149.00),
    "07": ("marrom", 3.00),
    "08": ("preto", 39.20),
    "09": ("laranja", 6.65)
}

# Fatores de multiplicação para os tamanhos
fatores_tamanho = {
    "A": ("pequeno", 1.0),
    "B": ("médio", 1.8),
    "C": ("grande", 2.8)
}

# Materiais dos produtos
materiais = {
    "Q": ("Quartzo", 1),
    "D": ("Dióxido de carbono", 5)
}

def validar_cep():
    primeira_vez = True
    while True:
        if primeira_vez:
            cep = input("Digite o CEP (somente números): ")
            primeira_vez = False
        else:
            cep = input("CEP inválido ou não encontrado. Tente novamente: ")
        
        if len(cep) == 8 and cep.isdigit():
            link = f"https://viacep.com.br/ws/{cep}/json/"
            try:
                with urllib.request.urlopen(link) as response:
                    data = json.loads(response.read().decode())
                    if "erro" not in data:
                        print("CEP: ", data["cep"])
                        print("Logradouro: ", data["logradouro"])
                        print("Bairro: ", data["bairro"])
                        print("Cidade: ", data["localidade"])
                        print("Estado: ", data["uf"])
                        return cep, data["localidade"]
                    else:
                        print("CEP não encontrado.")
            except urllib.error.URLError as e:
                print("Erro ao acessar o serviço de CEP:", e)
        else:
            print("CEP deve conter 8 dígitos numéricos.")

def obter_dados_por_codigo(codigo):
    if len(codigo) == 10 and codigo.startswith("1234") and codigo.endswith("56"):
        codigo_cor = codigo[4:6]
        codigo_tamanho = codigo[6]
        codigo_material = codigo[7]
        
        if codigo_cor in precos_cores and codigo_tamanho in fatores_tamanho and codigo_material in materiais:
            cor, preco_base = precos_cores[codigo_cor]
            tamanho, fator_tamanho = fatores_tamanho[codigo_tamanho]
            material, fator_material = materiais[codigo_material]
            preco_final = preco_base * fator_tamanho * fator_material
            return cor, tamanho, material, preco_final
    return None

def validar_telefone(telefone):
    return telefone.isdigit() and len(telefone) == 11

def obter_dados_comprador():
    nome_comprador = input("Digite o nome do comprador: ")
    telefone_comprador = input("Digite o telefone do comprador (somente números com DDD): ")
    while not validar_telefone(telefone_comprador):
        print("Número de telefone inválido. Deve conter 11 dígitos numéricos (incluindo DDD).")
        telefone_comprador = input("Digite o telefone do comprador (somente números com DDD): ")
    return nome_comprador, telefone_comprador

def obter_tipo_residencia():
    while True:
        tipo_residencia = input("Casa ou apartamento? ").lower()
        if tipo_residencia == "casa" or tipo_residencia == "apartamento":
            return tipo_residencia
        else:
            print("Por favor, digite apenas 'casa' ou 'apartamento'.")

def obter_detalhes_residencia(tipo_residencia):
    if tipo_residencia == "casa":
        numero_casa = input("Digite o número da casa: ")
        return {"numero_casa": numero_casa}
    elif tipo_residencia == "apartamento":
        bloco_apto = input("Digite o bloco do apartamento: ")
        numero_apto = input("Digite o número do apartamento: ")
        return {"bloco_apto": bloco_apto, "numero_apto": numero_apto}

def validar_codigo_produto():
    while True:
        codigo = input("Digite o código do cristal (formato: 1234XXAM56): ")
        dados_cristal = obter_dados_por_codigo(codigo)
        if dados_cristal:
            cor, tamanho, material, preco_final = dados_cristal
            print("\nDetalhes do Cristal:")
            print("Cor do cristal:", cor.capitalize())
            print("Tamanho do cristal:", tamanho.capitalize())
            print("Matéria prima:", material)
            print(f"Preço final: R${preco_final:.2f}")
            print("Código de identificação do produto:", codigo)
            confirmar = input("Esse é o produto comprado? (sim/não): ").lower()
            if confirmar == 'sim':
                return codigo, preco_final
        else:
            print("Código inválido ou não encontrado.")

def calcular_frete(cep, cidade):
    # Exemplo simples de cálculo de frete baseado na cidade
    fretes = {
        "São Paulo": 20.00,
        "Rio de Janeiro": 20.00,
        "Santa Catarina": 10.00,
        "Distrito Federal": 20.00,
        "Goiás": 20.00,
        "Mato Grosso do Sul": 20.00,
        "Minas Gerais": 20.00,
        "Espírito Santo": 20.00,
        "Paraná": 20.00,
        "Rio Grande do Sul":20.00,        
        "Outras": 30.00
    }
    return fretes.get(cidade, fretes["Outras"])

def salvar_pedido(dados_pedido):
    with open("pedidos.json", "a") as arquivo:
        json.dump(dados_pedido, arquivo)
        arquivo.write("\n")

def main():
    print("=== Sistema de Entregas ===")

    cep_entrega, cidade = validar_cep()
    nome_comprador, telefone_comprador = obter_dados_comprador()
    codigo_produto, preco_produto = validar_codigo_produto()
    tipo_residencia = obter_tipo_residencia()
    detalhes_residencia = obter_detalhes_residencia(tipo_residencia)
    frete = calcular_frete(cep_entrega, cidade)
    total = preco_produto + frete
    data_pedido = datetime.now().strftime("%d/%m/%y")
    hora_pedido = datetime.now().strftime("%H:%M:%S")

    print("\nDetalhes do Pedido:")
    print("Nome do comprador:", nome_comprador)
    print("Telefone do comprador:", telefone_comprador)
    print("Código do produto comprado:", codigo_produto)
    print("Tipo de residência:", tipo_residencia)
    if tipo_residencia == "casa":
        print("Número da casa:", detalhes_residencia["numero_casa"])
    elif tipo_residencia == "apartamento":
        print("Bloco do apartamento:", detalhes_residencia["bloco_apto"])
        print("Número do apartamento:", detalhes_residencia["numero_apto"])
    print("CEP para entrega:", cep_entrega)
    print(f"Frete: R${frete:.2f}")
    print(f"Total: R${total:.2f}")
    print("Data do pedido:", data_pedido)
    print("Hora do pedido:", hora_pedido)

    confirmar_pedido = input("Deseja confirmar o pedido? (sim/não): ").lower()
    if confirmar_pedido == 'sim':
        dados_pedido = {
            "nome_comprador": nome_comprador,
            "telefone_comprador": telefone_comprador,
            "codigo_produto": codigo_produto,
            "tipo_residencia": tipo_residencia,
            "detalhes_residencia": detalhes_residencia,
            "cep_entrega": cep_entrega,
            "frete": frete,
            "total": total,
            "data_pedido": data_pedido,
            "hora_pedido": hora_pedido
        }
        salvar_pedido(dados_pedido)
        print("Endereço confirmado e salvo com sucesso!")
    else:
        print("Pedido cancelado.")

if __name__ == "__main__":
    main()
