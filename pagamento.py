import math
import os
import random
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

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

def validar_num(num: str):
    if len(num) == 16:
        return num.isdigit()
    else:
        return False

def validar_mes(num: int):
    if num > 12 or num <= 0:
        return False
    return True

def validar_ano(num: int):
    if num < 2024 or num <= 0:
        return False
    return True

cristais = ['Azul', 'Verde', 'Rosa', 'Roxo', 'Vermelho', 'Branco', 'Marrom', 'Preto', 'Laranja']
preco = [99.90, 199.90, 31.90, 5.00, 31.90, 149.90, 3.00, 39.20, 6.65]
carrinho = []
valortotal = []
carrinhotam = []
carrinhomat = []

def main():
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
    print(f'\nValor final: R${valorfinal:.2f}\nData de compra: {hoje.strftime("%d/%m/%Y")}')


    pay = int(input('Qual seria a forma de pagamento? Pix(0); Débito(1); Crédito(2): '))
    while pay not in [0, 1, 2]:
        print('Por favor informe um número válido!')
        pay = int(input('Qual seria a forma de pagamento? Pix(0); Débito(1); Crédito(2): '))

    if pay == 0:
        print('1 - Um código será gerado juntamente com um QR CODE; \n2 - Copie e cole o código para efetuar o pagamento ou aponte o celular para o QR CODE! \n3 - Efetue o pagamento no aplicativo do seu banco!')
        cv = random.randint(10000000, 100000000)
        print(f'Código copia e cola -> {cv}')
        dados = "https://youtu.be/z9Ugvt08wwI?si=u6JjHe36RA4YbbUk"
        exibir_qr_code(dados)
       
    elif pay == 1:
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
        cvv = int(input('Informe o cvv para confirmar a compra: '))
        while cvv > 999 or cvv < 100:
            print('Por favor, informe um número válido!')
            cvv = int(input('Informe o cvv para confirmar a compra: '))
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
            print(f'{i}x R${valorfinal/i:.2f}')
        parcela = int(input('Digite aqui: '))
        cvv = int(input('Informe o cvv para confirmar a compra: '))
        while cvv > 999 or cvv < 100:
            print('Por favor, informe um número válido!')
            cvv = int(input('Informe o cvv para confirmar a compra: '))
        print(f'Pagamento parcelado em {parcela}x de R${valorfinal/parcela:.2f} sem juros!')
    print('Compra efetuada com sucesso, aguarde o envio do seu pedido!')

if __name__ == '__main__':
    main()
