from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options

# mode headless
chrome_options = Options()
chrome_options.add_argument('--headless')

# Create a conjunt for unique URLS 
unique_links = set()
unique_links_post = set()

data = []

#Settings driver Chrome 
navegador = webdriver.Chrome(options=chrome_options)

#url = 'https://medium.com/search?q=Natural+Language+Process'
url = 'https://medium.com/search/lists?q=Natural+Language+Process&source=search_list---------4----------------------------'

def clean_text(text):
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return cleaned_text

# init = 0 start scraping with function getLinks, init = 1 other call of the function
def getPageSource(url, init = 0, maxscroll = 1):
    navegador.get(url)

    sleep(5)

    if init == 0:
        variable = 13
        for i in range(0, maxscroll):
            
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(i)
            
            try:
                
                button = navegador.find_element(By.XPATH, f'//*[@id="root"]/div/div[3]/div[2]/div/main/div/div/div/div/div[{(10*i)+variable}]/div[1]/button')
                sleep(10)
                button.click()
                
            except Exception as e:

                print(f'Max: {i}')
                break
            
            sleep(10)
            
    else:
        
        for i in range(0, maxscroll):
            
            navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(10)

    # Obtenha o HTML da página após o clique
    html_content = navegador.page_source
    
    # Use BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup

def getLinks(url):

    soup = getPageSource(url, 0, 10)
    
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
    file_name = "struct_getLinks.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup)
        
    #navegador.quit()

def acessAndGetLinksInPerfil(url):
    
    soup = getPageSource(url, 1, 20)
    
    html_content = navegador.page_source
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    links = soup.find_all('a', class_='af ag ah ai aj ak al am an ao ap aq ar as at')

    pattern = re.compile(r'^/@.+/.+$')

    for link in links:
        href = link.get('href')
        if href and pattern.match(href):
            text = "https://medium.com" + href
            unique_links_post.add(text)

    soup = soup.prettify()

    file_name = "struct_acessAndGetLinksInPerfil.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup)

def getData(url):
    
    soup = getPageSource(url, 1, 1)
    
    html_content = navegador.page_source
    
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.find('h1', class_=re.compile(r'pw-post-title.*'))
    
    subtitle = soup.find('h2', class_=re.compile(r'pw-subtitle-paragraph.*'))
    
    clap = soup.find('div', class_=re.compile(r'pw-multi-vote-count.*')) 
    
    responses = soup.find('span', class_=re.compile(r'pw-responses-count.*'))
    
    autorName = soup.find('a', {'data-testid': 'authorName'})
    
    followers = soup.find('span', class_=re.compile(r'pw-follower-count.*'))
    
    imageAutor = soup.find('img', {'data-testid': 'authorPhoto'})
    
    timeForRead = soup.find('span', {'data-testid': 'storyReadTime' })
    
    dateCreate = soup.find('span', {'data-testid': 'storyPublishDate'})
    
    post = soup.find_all('p', class_=re.compile(r'pw-post-body-paragraph.*'))
    info = {}
    
    info['link'] = url
    if title:
        title = title.text
        info['title'] = title 
        #print(title)
    else:
        info['title'] = 'false' 
    
    if subtitle:
        subtitle = subtitle.text
        info['subtitle'] = subtitle
        #print(subtitle)
    else:
        info['subtitle'] = 'false'
    
    if autorName:
        autorName = autorName.text
        info['autorName'] = autorName
        #print(autorName)
    else:
        info['autorName'] = 'false'
        
    if imageAutor:
        imageAutor = imageAutor['src']
        info['imageAutor'] = imageAutor
        #print(imageAutor)
    else:
        info['imageAutor'] = 'false'
        
    if clap:
        clap = clap.text
        info['clap'] = clap
        #print(clap)
    else:
        info['clap'] = 'false'

    if responses:
        responses = responses.text
        info['response'] = responses
        #print(responses)
    else:
        info['response'] = 'false'
    
    if timeForRead:
        timeForRead = timeForRead.text
        info['timeForRead'] = timeForRead
        #print(timeForRead)
    else:
        info['timeForRead'] = 'false'
        
    if dateCreate:
        dateCreate = dateCreate.text
        info['dateCreate'] = dateCreate
        #print(dateCreate)
    else:
        info['dateCreate'] = 'false'
    
    if post:
        text_list = []

        for tag in post:
            stringAppend = clean_text(tag.text)
            
            text_list.append(stringAppend+'\n')

        info['text'] = text_list.copy()

        text_list.clear()
    else:
        info['text'] = 'false'
    
    print(info)
    soup = soup.prettify()

    file_name = "struct_getData.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup)
    
def main(url):
    getLinks(url)
    for link in unique_links:
        acessAndGetLinksInPerfil(link)
    for acessPost in unique_links_post:
        getData(acessPost)

main(url)
