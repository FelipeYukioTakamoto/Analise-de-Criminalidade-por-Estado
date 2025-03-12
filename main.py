import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# --- Configuração inicial ---
URL = 'https://www.ipea.gov.br/atlasviolencia/'  # Site oficial do Atlas da Violência
DRIVER_PATH = 'C:\Users\yukio\Downloads\chromedriver_win32'  # Substitua pelo caminho do seu ChromeDriver
SHAPEFILE_PATH = 'C:\Users\yukio\Downloads\BR_Pais_2023'  # shapefile do Brasil

# --- Função de scraping ---
def scrape_crime_data():
    # Requisição ao site
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemplo de extração de dados (ajuste os seletores conforme o site)
    tabela = soup.find('table', {'class': 'tabela-dados'})  # Substitua pela classe correta
    dados_estados = []

    if tabela:
        for linha in tabela.find_all('tr')[1:]:  # Pular cabeçalho
            celulas = linha.find_all('td')
            estado = celulas[0].text.strip()
            indice = float(celulas[1].text.replace(',', '.'))
            dados_estados.append({'Estado': estado, 'Índice': indice})
    else:
        print("Tabela não encontrada. Verifique o seletor ou a estrutura do site.")

    return pd.DataFrame(dados_estados)

# --- Execução e tratamento de dados ---
# (Se o scraping real não for possível, use dados mockados para teste)
dados_mockados = pd.DataFrame({
    'Estado': ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'DF'],
    'Índice': [8.7, 9.4, 7.1, 6.5, 5.9, 4.3, 8.2, 7.8, 9.1, 6.7]  # Valores hipotéticos
})

df = dados_mockados  # Substituir por scrape_crime_data() para uso real

# --- Análise ---
top_5 = df.sort_values(by='Índice', ascending=False).head(5)

# --- Visualização ---
plt.figure(figsize=(12, 6))
sns.barplot(x='Estado', y='Índice', data=top_5, palette='Reds')
plt.title('Top 5 Estados com Maiores Índices de Criminalidade (2023)')
plt.xlabel('')
plt.ylabel('Índice por 100 mil habitantes')
plt.show()

# --- Mapa Brasil (requer shapefile) ---
# Baixe o shapefile do Brasil em: https://www.ibge.gov.br/geociencias/downloads-geociencias.html
mapa_br = gpd.read_file(SHAPEFILE_PATH)
mapa_br = mapa_br.merge(df, left_on='SIGLA_UF', right_on='Estado')

fig, ax = plt.subplots(1, figsize=(14, 8))
mapa_br.plot(column='Índice', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.axis('off')
plt.title('Mapa da Criminalidade por Estado - Brasil')
plt.show()
