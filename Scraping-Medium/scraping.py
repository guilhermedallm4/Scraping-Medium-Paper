from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options

# Configurar opções para o modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')

# Criar um conjunto para armazenar URLs únicas
unique_links = set()
unique_links_post = set()

# Configurar o driver do Chrome 
navegador = webdriver.Chrome(options=chrome_options)

#url = 'https://medium.com/search?q=Natural+Language+Process'
url = 'https://medium.com/search/lists?q=Natural+Language+Process&source=search_list---------4----------------------------'

def getLinks(url):
    navegador.get(url)
    
    # Aguarde alguns segundos para a página carregar completamente
    navegador.implicitly_wait(10)  # Você pode ajustar o tempo de espera conforme necessário
    variable = 13
    sleep(5)
    
    for i in range(0,2):
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(i)
        try:
            button = navegador.find_element(By.XPATH, f'//*[@id="root"]/div/div[3]/div[2]/div/main/div/div/div/div/div[{(10*i)+variable}]/div[1]/button')
            print(button)
            sleep(10)
            button.click()
        except Exception as e:
            #print(f"Erro ao clicar no botão: {e}")
            print(f'Max: {i}')
            break
        sleep(10)

    # Obtenha o HTML da página após o clique
    html_content = navegador.page_source
    
    # Use BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontre todas as tags <a> com a classe 'af ag ah ai aj ak al am an ao ap aq ar as at'
    links = soup.find_all('a', class_='af ag ah ax aj ak al am an ao ap aq ar as at ff kc')
    # Crie um conjunto para armazenar os links únicos

    pattern = re.compile(r'/@.*/list/n')

    # Imprima os atributos 'href' das tags <a> que atendem à condição
    for link in links:
        href = link.get('href')
        if href and pattern.match(href):
            text = "https://medium.com" + href
            unique_links.add(text)
            print(text)

    soup = soup.prettify()

    # Salve o HTML em um arquivo
    file_name = "info_div2.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup)
        
    # Feche o navegador quando terminar
    #navegador.quit()

def acessAndGetLinksInPerfil(url):
    navegador.get(url)
    # Aguarde alguns segundos para a página carregar completamente
    sleep(5)
    maxscroll = 1
    for i in range(0, maxscroll):
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)

    # Obtenha o HTML da página após o clique
    html_content = navegador.page_source
    
    # Use BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontre todas as tags <a> com a classe 'af ag ah ai aj ak al am an ao ap aq ar as at'
    links = soup.find_all('a', class_='af ag ah ai aj ak al am an ao ap aq ar as at')
    # Crie um conjunto para armazenar os links únicos

    pattern = re.compile(r'^/@.+/.+$')

    # Imprima os atributos 'href' das tags <a> que atendem à condição
    for link in links:
        href = link.get('href')
        if href and pattern.match(href):
            text = "https://medium.com" + href
            unique_links_post.add(text)
            #print(text)

    soup = soup.prettify()

    file_name = "link_post.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup)

def main(url):
    getLinks(url)
    for link in unique_links:
        acessAndGetLinksInPerfil(link)
    for i in unique_links_post:
        print(i)
#getLinks(url)
#acessAndGetLinksInPerfil('https://medium.com/@k.upendar007/list/natural-language-processing-35122275c687')

main(url)
