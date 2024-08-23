import requests


ativo = "PETR4"
def monitorar_cotacao(ativo):

    url = f"https://brapi.dev/api/quote/{ativo}?token=3Tu4RVE65Gh97hHorLH9et"
    response = requests.get(url)

    if response.status_code == 200:
        # converte a resposta para JSON
        data = response.json()

        # extrai a cotação atual do ativo do JSON
        cotacao = data['results'][0]['regularMarketPrice']
        
        return cotacao
    else:
        # tratamento de erro
        print(f"Erro ao buscar cotação. Código de status: {response.status_code}")
    
        

