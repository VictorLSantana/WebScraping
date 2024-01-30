
# Carregando as bibliotecas que são utilizadas.
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

# Definindo o site do qual serão raspados os dados.
url = "https://www.forbes.com/sites/chasewithorn/2023/04/04/the-25-richest-people-in-the-world-2023/?sh=4bee60f14969" 

# Simulando um navegador para a requisição ser aceita pelo domínio do site.
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Pegando o html do site.
requisicao = requests.get(url, headers=header).text

# Utilizando o BeautifulSoup para preparar o html que será utilizado na raspagem dos dados.
sopa = BeautifulSoup(requisicao, 'html.parser')
 
# Raspando os nomes dos bilionários.             
Nomes = []
ricos = sopa.find_all('h3')
for i in range(len(ricos)):
    Nomes.append(ricos[i].text.split('. ')[1])
    
# Raspando as características de cada bilionário.
linhas = sopa.find_all('h4')
linhas_df = []
for i in range(3, len(linhas)-2):
    linhas_df.append(linhas[i].text)

for i in range(len(linhas_df)):
    linhas_df[i] = linhas_df[i].split('|')


# Função para extrair as características(0, 1, 2 e 3) de cada bilionário,
# posteriormente cada característica será uma coluna no DataFrame.
# 0 -> Patrimônio Líquido
# 1 -> Fonte de Riqueza
# 2 -> Idade
# 3 -> País de Origem
def caracteristicas(linha, coluna):
    return linha[coluna].split(':')[1].strip()
    
# Criando a Coluna do Patrimônio Líquido.
patrimonio_liquido = []
for linha in linhas_df:
    patrimonio_liquido.append(caracteristicas(linha, 0).split(' ')[0].replace('$', ''))
for i in range(len(patrimonio_liquido)):
    patrimonio_liquido[i] = float(patrimonio_liquido[i])
    
# Criando a Coluna da Fonte de Riqueza.
fonte_riqueza = []
for linha in linhas_df:
    fonte_riqueza.append(caracteristicas(linha, 1))

# Criando coluna Idade.
Idade = []
for linha in linhas_df:
    Idade.append(int(caracteristicas(linha, 2)))

# Criando coluna País
pais_origem = []
for linha in linhas_df:
    pais_origem.append(caracteristicas(linha, 3))

# Posição do Ranking.
Ranking = list(range(1, 26))

# Criando o DataFrame.
DataFrame = pd.DataFrame({
    'Ranking': Ranking,
    'Nome': Nomes,
    'Patrimônio_Líquido': patrimonio_liquido,
    'Fonte_Riqueza': fonte_riqueza,
    'Idade': Idade,
    'País_Origem': pais_origem
    
})
print(DataFrame.to_string(index=False))

# Criando um bando de dados no MySQL a partir do DataFrame.


# Configurar a conexão com o banco de dados MySQL.
user = input('Digite seu usuário ')
password = input('Digite sua senha ')
host = input('Digite o host ')
database = input('Digite o banco de dados ')
port = input('Digite a porta ')

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Enviar o DataFrame para o banco de dados MySQL.
tabela = 'ranking_ricos'
DataFrame.to_sql(name=tabela, con=engine, if_exists='replace', index=False)

DataFrame.to_excel('RankingPBI.xlsx', index=False)