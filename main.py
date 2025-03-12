import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuração inicial (substitua com seus valores) ---
DRIVER_PATH = '/caminho/do/seu/chromedriver'  # Necessário para sites com JavaScript
ESTADOS_BRASIL = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'DF']  # Lista completa de estados

# --- Função de scraping (exemplo genérico) ---
def scrape_crime_data():
    url = 'https://exemplo-site-gov.com/criminalidade'  # Substituir por fonte real
    dados_estados = []

    # Opção 1: Site estático (BeautifulSoup)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Exemplo de extração (ajuste os seletores):
    tabela = soup.find('table', {'class': 'dados-crime'})
    for linha in tabela.find_all('tr')[1:]:  # Pular cabeçalho
        celulas = linha.find_all('td')
        estado = celulas[0].text.strip()
        indice = float(celulas[1].text.replace(',', '.'))
        dados_estados.append({'Estado': estado, 'Índice': indice})

    # Opção 2: Site dinâmico (Selenium)
    """
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(url)
    time.sleep(3)  # Espera carregar JavaScript
    
    elementos = driver.find_elements(By.CSS_SELECTOR, '.classe-dos-dados')
    for elemento in elementos:
        # Processamento similar...
    driver.quit()
    """

    return pd.DataFrame(dados_estados)

# --- Execução e tratamento de dados ---
# (Se o scraping real não for possível, use dados mockados para teste)
dados_mockados = pd.DataFrame({
    'Estado': ESTADOS_BRASIL,
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
# Baixe shapefile do Brasil em: https://www.ibge.gov.br/geociencias/downloads-geociencias.html
mapa_br = gpd.read_file('/caminho/BR_UF_2022.shp')
mapa_br = mapa_br.merge(df, left_on='SIGLA_UF', right_on='Estado')

fig, ax = plt.subplots(1, figsize=(14, 8))
mapa_br.plot(column='Índice', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.axis('off')
plt.title('Mapa da Criminalidade por Estado - Brasil')
plt.show()
