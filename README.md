# Desafio Aviso de Cotação

<br>

## Desafio proposto

- O objetivo do sistema é avisar, via e-mail, caso a cotação de um ativo da B3 caia mais do que certo nível, ou suba acima de outro.

- O programa deve ser uma aplicação de console (não há necessidade de interface gráfica).

- Ele deve ser chamado via linha de comando com 3 parâmetros.

    - O ativo a ser monitorado
    - O preço de referência para venda
    - O preço de referência para compra
    Ex.

```cmd
stock-quote-alert.exe PETR4 22.67 22.59
```

- Ele deve ler de um arquivo de configuração com:
    - O e-mail de destino dos alertas
As configurações de acesso ao servidor de SMTP que irá enviar o e-mail
A escolha da API de cotação é livre.
- O programa deve ficar continuamente monitorando a cotação do ativo enquanto estiver rodando.

## Aspectos Gerais

- O programa foi feito subdivindo o problema em quatro partes, sendo elas:
    - Enviar o e-mail
    - Monitor a cotação
    - Configuração CLI e lógica (feitas no arquivo principal)
- Além disso, no arquivo de configuração ([config.ini](./config.ini)) há informações como o remetente, destinatário e servidor smtp.

## Envio do e-mail

- **Dependências**:
    ```python
    import smtplib
    import email.message
    import configparser
    ```
    - *smtplib*: Biblioteca padrão do Python para enviar e-mails usando o protocolo SMTP.
    - *email.message*: Módulo para criar mensagens de e-mail.
    - *configparser*: Módulo para ler arquivos de configuração.

- A função recebe como parâmetros a string do assunto e corpo do e-mail:

```python
def enviar_email(assunto, corpo):
```
- config = configparser.ConfigParser(): Cria uma instância do objeto ConfigParser, que será usada para ler o arquivo de configuração.
- config.read('config.ini'): Lê o conteúdo do arquivo config.ini e carrega as configurações em config.

```python
config = configparser.ConfigParser()
config.read('config.ini')
```
```ini
[EMAIL]
Destino = pedromileipp@gmail.com
Remetente = pedromileipp2@gmail.com

[SMTP]
Servidor = smtp.gmail.com
Porta = smtp.gmail.com: 587
Senha = senha
```
- É necessário criar uma instância de Message que será usada para construir o e-mail

```python
msg = email.message.Message()
```

- Deve-se definir o assunto, remetente e destinatário do e-mail, ambos serão lidos do config.ini.
- A senha também será lida do config.ini e no caso do G-mail é necessário criar uma senha para a aplicação e ativar a verificação em duas etapas, no [link](https://support.google.com/accounts/answer/185833?hl=pt-BR) é possível encontrar como criar a senha de aplicação do G-mail.

```python
    msg['Subject'] = assunto
    msg['From'] = config['EMAIL']['Remetente']
    msg['To'] = config['EMAIL']['Destino']        password = config['SMTP']['Senha'] 
```

 - Corpo do e-mail é definido utilizando `msg.set_payload(corpo)`, permitindo o envio de e-mails em formato HTML.
- Uma conexão SMTP é estabelecida utilizando o servidor e as credenciais configuradas no config.ini.
- A função autentica o remetente com as credenciais fornecidas e envia o e-mail para o destinatário.

<br>

## Monitoramento da cotação

- _**OBS: o token usado nesse código já não está mais ativo**_
- É feito pela função `monitorar_cotacao(ativo)` que recebe como parâmetro o ativo a ser monitorado
```python
def monitorar_cotacao(ativo)
```
- Utiliza a API Brapi para obter a cotação em tempo real de um ativo da B3 utilizando a API Brapi. Essa função envia uma requisição para a API, processa a resposta e retorna o preço atual do ativo solicitado.
- Para utilizar a Brapi, deve ser feito o cadastro no [site](brapi.dev) e gerar um token.

- Construção da URL da API:
    - A URL da API é construída dinamicamente usando o ticker do ativo fornecido como parâmetro.
    - A URL segue o formato `https://brapi.dev/api/quote/{ativo}?token=TOKEN`, onde `{ativo}` é substituído pelo ticker do ativo.
    ```python
    url = f"https://brapi.dev/api/quote/{ativo}?token=TOKEN"
    ```

- Envio da Requisição HTTP GET:
    - A função utiliza a biblioteca `requests` para enviar uma requisição HTTP GET para a URL construída.
    ```python
    response = requests.get(url)
    ```

- Verificação do Status da Resposta:
    - Após enviar a requisição, a função verifica se o status da resposta é 200, o que indica que a requisição foi bem-sucedida.
     ```python
    if response.status_code == 200:
    ```

- Conversão da resposta para JSON e extração da cotação atual
    - Se a requisição foi bem-sucedida, a resposta é convertida para o formato JSON, o que facilita a extração das informações necessárias.
    - A função extrai o valor da cotação atual do ativo a partir da chave 'regularMarketPrice' dentro da estrutura JSON retornada.
    ```python
    data = response.json()
    cotacao = data['results'][0]['regularMarketPrice']
    ```

- A função retorna o valor da cotação extraído:
```python
return cotacao
```

<br>

## Programa principal
- Este programa monitora a cotação de um ativo da B3 em tempo real e envia alertas por e-mail caso a cotação do ativo atinja certos limites definidos pelo usuário. O programa é executado via linha de comando (CLI) e continua monitorando a cotação enquanto estiver em execução.

- _**Funcionamento**_
    - Monitoramento de Cotações: O programa verifica periodicamente a cotação atual de um ativo especificado.
    - Envio de Alertas: Se a cotação ultrapassar um preço de venda definido ou cair abaixo de um preço de compra definido, o programa envia um alerta por e-mail ao usuário.

- O programa deve ser executado com três parâmetros obrigatórios na linha de comando:
```
python nome_do_programa.py <ticker> <preco_venda> <preco_compra>
```
- Parâmetros
    - ticker: Ticker do ativo a ser monitorado (por exemplo, PETR4).
    - preco_venda>: Preço de referência para venda (se a cotação atual ultrapassar este valor, um alerta de venda é enviado).
    - preco_compra: Preço de referência para compra (se a cotação atual cair abaixo deste valor, um alerta de compra é enviado).

- Importações necessárias
    - **time**: Usada para pausar o programa entre as verificações de cotação.
    - **argparse**: Utilizado para ler os parâmetros fornecidos via linha de comando.
    - **monitorar_cotacao**: Função importada do módulo monitorar_cotacao.py para obter a cotação do ativo.
    - **enviar_email**: Função importada do módulo envia_email.py para enviar e-mails de alerta.
    ```python
    import time
    import argparse
    from monitorar_cotacao import monitorar_cotacao
    from envia_email import enviar_email
    ```

- Configuração do ArgumentPasser
    - O `argparse` configura o programa para aceitar três parâmetros na linha de comando: `ticker`, `preco_venda` e `preco_compra`.
    ```python
    parser = argparse.ArgumentParser(description='Monitorar a cotação de um ativo da B3 e enviar alertas por e-mail.')
    parser.add_argument('ticker', type=str, help='Ticker do ativo a ser monitorado (ex: PETR4)')
    parser.add_argument('preco_venda', type=float, help='Preço de referência para venda')
    parser.add_argument('preco_compra', type=float, help='Preço de referência para compra')
    args = parser.parse_args()
    ```

- Loop de Monitoramento Contínuo:
    - O programa entra em um loop infinito (while True) para monitorar continuamente a cotação do ativo.
    - Em cada iteração, a função monitorar_cotacao é chamada para obter a cotação atual do ativo.
    ```python
    while True:
    cotacao_atual = monitorar_cotacao(args.ticker)
    if cotacao_atual is None:
        time.sleep(10)
        continue
    ```

- Verificação da cotação e envio dos alertas
    - Se a cotação atual for maior que o preço de venda (preco_venda), um e-mail de alerta de venda é enviado.
    - Se a cotação atual for menor que o preço de compra (preco_compra), um e-mail de alerta de compra é enviado.
    - O programa faz uma pausa (nesse caso, 10 segundos) antes de verificar a cotação novamente. Esse tempo pode ser ajustado pelo usuário
    ```python
        print(f'Cotação atual de {args.ticker}: R$ {cotacao_atual:.2f}')

    if cotacao_atual > args.preco_venda:
        mensagem = f'O preço do ativo {args.ticker} subiu para R$ {cotacao_atual:.2f}. Considere vender.'
        enviar_email('Alerta de Venda', mensagem)
        print('Alerta de venda enviado.')

    elif cotacao_atual < args.preco_compra:
        mensagem = f'O preço do ativo {args.ticker} caiu para R$ {cotacao_atual:.2f}. Considere comprar.'
        enviar_email('Alerta de Compra', mensagem)
        print('Alerta de compra enviado.')
    ```




