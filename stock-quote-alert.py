import time
import argparse
from monitorar_cotacao import monitorar_cotacao
from envia_email import enviar_email

# usando o argparse para ler os parametros CLI
parser = argparse.ArgumentParser(description='Monitorar a cotação de um ativo da B3 e enviar alertas por e-mail.')
parser.add_argument('ticker', type=str, help='Ticker do ativo a ser monitorado (ex: PETR4)')
parser.add_argument('preco_venda', type=float, help='Preço de referência para venda')
parser.add_argument('preco_compra', type=float, help='Preço de referência para compra')
args = parser.parse_args()


# loop para monitorar a cotação
while True:
    # pega a cotação atual do ativo
    cotacao_atual = monitorar_cotacao(args.ticker)
    if cotacao_atual is None:
        time.sleep(10)
        continue

    print(f'Cotação atual de {args.ticker}: R$ {cotacao_atual:.2f}')

    # lógica para enviar alerta de venda ou compra
    if cotacao_atual > args.preco_venda:
        mensagem = f'O preço do ativo {args.ticker} subiu para R$ {cotacao_atual:.2f}. Considere vender.'
        enviar_email('Alerta de Venda', mensagem)
        print('Alerta de venda enviado.')

    elif cotacao_atual < args.preco_compra:
        mensagem = f'O preço do ativo {args.ticker} caiu para R$ {cotacao_atual:.2f}. Considere comprar.'
        enviar_email('Alerta de Compra', mensagem)
        print('Alerta de compra enviado.')
        

    # Esperar um tempo antes de verificar novamente (por exemplo, 60 segundos)
    time.sleep(10)