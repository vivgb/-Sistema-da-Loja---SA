import math
import os
import random
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
import json
import urllib.request

# Funções para validar informações de pagamento
def validar_num(num: str):
    return len(num) == 16 and num.isdigit()

def validar_mes(num: int):
    return 1 <= num <= 12

def validar_ano(num: int):
    return num >= 2024

# Função para gerar código QR
def gerar_qr_code(dados):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(dados)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    return img

def exibir_qr_code(dados):
    img = gerar_qr_code(dados)
    janela = tk.Tk()
    janela.title("QR Code")
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(janela, image=img_tk)
    label.pack()
    label.image = img_tk
    janela.mainloop()

# Funções para o sistema de entregas
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

def obter_dados_comprador():
    nome_comprador = input("Digite o nome do comprador: ")
    telefone_comprador = input("Digite o telefone do comprador: ")
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

def calcular_frete(cep, cidade):
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
        "Rio Grande do Sul": 20.00,
        "Outras": 30.00
    }
    return fretes.get(cidade, fretes["Outras"])

def salvar_pedido(dados_pedido):
    with open("pedidos.json", "a") as arquivo:
        json.dump(dados_pedido, arquivo)
        arquivo.write("\n")

# Função principal
def main():
    cristais = ['Azul', 'Verde', 'Rosa', 'Roxo', 'Vermelho', 'Branco', 'Marrom', 'Preto', 'Laranja']
    preco = [99.90, 199.90, 31.90, 5.00, 31.90, 149.90, 3.00, 39.20, 6.65]
    carrinho = []
    valortotal = []
    carrinhotam = []
    carrinhomat = []

    print("--Seja bem vindo(a) à loja de cristais da Ana!--")
    n = int(input('Quantos itens deseja comprar?: '))
    print('Lista dos cristais:')
    print('Cristais de diamante são 5 vezes mais caros!*')
    for i in range(len(cristais)):
        print(f'{i} = {cristais[i]}: \nPequeno - R${preco[i]} \nMédio - R${preco[i]+(preco[i]*0.8):.2f} \nGrande - R${preco[i]+(preco[i]*1.8):.2f}')

    print('Informe o código dos produtos que deseja adicionar ao carrinho!')
    for _ in range(n):
        num = int(input('Produto: '))
        while num not in range(len(cristais)):
            print('Por favor insira um código existente!')
            num = int(input('Produto: '))
        material = ['Quartzo', 'Diamante']
        mat = int(input('Quartzo(0) ou Diamante(1)?: '))
        while mat not in [0, 1]:
            print('Por favor insira um código existente!')
            mat = int(input('Quartzo(0) ou Diamante(1)?: '))
        tam = str(input('Tamanho (P, M, G): '))
        tamanhos = ['Pequeno', 'Médio', 'Grande']
        while tam not in ['P', 'p', 'M', 'm', 'G', 'g']:
            print('Por favor informe um tamanho existente!')
            tam = str(input('Tamanho (P, M, G): '))
        carrinho.append(cristais[num])
        
        if (tam == 'P' or tam == 'p') and mat == 0:
            valortotal.append(preco[num])
            carrinhotam.append(tamanhos[0])
            carrinhomat.append(material[0])
        elif (tam == 'P' or tam == 'p') and mat == 1:
            valortotal.append(preco[num] * 5)
            carrinhotam.append(tamanhos[0])
            carrinhomat.append(material[1])
        elif (tam == 'M' or tam == 'm') and mat == 0:
            valortotal.append(preco[num] + (preco[num] * 0.8))
            carrinhotam.append(tamanhos[1])
            carrinhomat.append(material[0])
        elif (tam == 'M' or tam == 'm') and mat == 1:
            valortotal.append(((preco[num])+(preco[num]*0.8))*5)
            carrinhotam.append(tamanhos[1])
            carrinhomat.append(material[1])
        elif (tam == 'G' or tam == 'g') and mat == 0:
            valortotal.append(preco[num] + (preco[num] * 1.8))
            carrinhotam.append(tamanhos[2])
            carrinhomat.append(material[0])
        elif (tam == 'G' or tam == 'g') and mat == 1:
            valortotal.append(((preco[num]) + (preco[num] * 1.8))*5)
            carrinhotam.append(tamanhos[2])
            carrinhomat.append(material[1])
        else:
            print('Inválido, por favor tente novamente!')

    os.system('cls') or None
    print('--Pagamento--')
    cod = random.randint(10000000, 10000000000)
    valorfinal = sum(valortotal)
    hoje = datetime.now()
    print(f'Código do pedido: {cod}\nQuantidade de itens: {n}')
    print('Itens do carrinho:')
    for i in range(len(carrinho)):
        print(f'{carrinho[i]}; tamanho: {carrinhotam[i]}; material: {carrinhomat[i]}; valor: R${valortotal[i]:.2f}')
    print(f'\nValor final: R${valorfinal:.2f}\nData e hora de compra: {hoje.strftime("%d/%m/%Y %H:%M:%S")}')
    print("--Preenchimento de dados para a entrega--")
    nome_comprador, telefone_comprador = obter_dados_comprador()
    cep, cidade = validar_cep()
    tipo_residencia = obter_tipo_residencia()
    detalhes_residencia = obter_detalhes_residencia(tipo_residencia)
    frete = calcular_frete(cep, cidade)
    total_com_frete = valorfinal + frete

    dados_pedido = {
        "codigo_pedido": cod,
        "data_compra": hoje.strftime("%d/%m/%Y %H:%M:%S"),
        "itens": [{"produto": carrinho[i], "tamanho": carrinhotam[i], "material": carrinhomat[i], "valor": valortotal[i]} for i in range(len(carrinho))],
        "valor_total": valorfinal,
        "nome_comprador": nome_comprador,
        "telefone_comprador": telefone_comprador,
        "cep": cep,
        "cidade": cidade,
        "tipo_residencia": tipo_residencia,
        "detalhes_residencia": detalhes_residencia,
        "frete": frete,
        "total_com_frete": total_com_frete
    }
    salvar_pedido(dados_pedido)
    print(f'\nValor total com frete: R${total_com_frete:.2f}')

    pay = int(input('Qual seria a forma de pagamento? Pix(0); Débito(1); Crédito(2): '))
    while pay not in [0, 1, 2]:
        print('Por favor informe um método de pagamento existente!')
        pay = int(input('Qual seria a forma de pagamento? Pix(0); Débito(1); Crédito(2): '))

    if pay == 1 :
        ncartao = input('Número do cartão: ')
        while not validar_num(ncartao):
            print('Por favor informe um número válido de cartão!')
            ncartao = input('Número do cartão: ')
        mes = int(input('Mês de validade: '))
        while not validar_mes(mes):
            print('Por favor informe um mês válido!')
            mes = int(input('Mês de validade: '))
        ano = int(input('Ano de validade: '))
        while not validar_ano(ano):
            print('Por favor informe um ano válido!')
            ano = int(input('Ano de validade: '))
        cvv = int(input('CVV: '))
        while cvv > 999 or cvv < 100:
            print('Por favor informe um CVV válido!')
            cvv = input('CVV: ')
        print('Pagamento confirmado!')

    elif pay == 0:
        print('Pagamento confirmado!')
        print("Gerando QR Code com os dados do pedido...")
        dados_pedido = {
            "codigo_pedido": cod,
            "data_compra": hoje.strftime("%d/%m/%Y %H:%M:%S"),
            "itens": [{"produto": carrinho[i], "tamanho": carrinhotam[i], "material": carrinhomat[i], "valor": valortotal[i]} for i in range(len(carrinho))],
            "valor_total": valorfinal
        }
        exibir_qr_code(dados_pedido)
    elif pay == 2:
        print('--Informe as informações do cartão--')
        s = input('Números do cartão (sem espaço e símbolos): ')
        while not validar_num(s):
            print('Por favor, informe um número válido!')
            s = input('Números do cartão (sem espaço e símbolos): ')
        nome_cartao = input('Informe o nome do cartão:')
        mes = int(input('Mês de vencimento:'))
        ano = int(input('Ano de vencimento:'))
        while not (validar_mes(mes) and validar_ano(ano)):
            print('Por favor, informe uma data válida!')
            mes = int(input('Mês de vencimento:'))
            ano = int(input('Ano de vencimento:'))
        print('Quantas vezes deseja parcelar?')
        for i in range(1, 13):
            print(f'{i}x R${total_com_frete/i:.2f}')
        parcela = int(input('Digite aqui: '))
        cvv = int(input('Informe o cvv para confirmar a compra: '))
        while cvv > 999 or cvv < 100:
            print('Por favor, informe um número válido!')
            cvv = int(input('Informe o cvv para confirmar a compra: '))
        print(f'Pagamento parcelado em {parcela}x de R${total_com_frete/parcela:.2f} sem juros!')
    print('Compra efetuada com sucesso, aguarde o envio do seu pedido!')
    
   

if __name__ == "__main__":
    main()
