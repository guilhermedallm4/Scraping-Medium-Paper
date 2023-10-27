from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options
import json
import unicodedata

# mode headless
chrome_options = Options()
chrome_options.add_argument('--headless')

# Create a conjunt for unique URLS 
unique_links = set()
unique_links_post = set()
tagToken = set()

data = []

#Settings driver Chrome 
navegador = webdriver.Chrome(options=chrome_options)

tokens = ['iot', 'nlp', 'agriculture', 'ontology', 'postgresql', 'cluster', 'distributed-processing', 'parallel-processing']

counter = 0

informationToken = {}

def jsonImport(info, token):
    dados_existentes = []
    archive = f'./scraping_MediumV2/papersMedium-{token}.json'
    try:
        with open(archive, 'r', encoding="utf-8") as arquivo:
            dados_existentes = json.load(arquivo)
        dados_existentes.append(info)

    except FileNotFoundError:
        dados_existentes = [info]

    
    
    with open(archive, 'w', encoding="utf-8") as arquivo:
        json.dump(dados_existentes, arquivo, ensure_ascii=False)
        
    dados_existentes.clear()

def clean_text(text): 
    return ''.join(char for char in text if unicodedata.name(char).isascii())

# init = 0 start scraping with function getLinks, init = 1 other call of the function
def getPageSource(url, init = 0, maxscroll = 1):
    navegador.get(url)

    sleep(5)

    for i in range(0, maxscroll):
            
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)

    
    html_content = navegador.page_source
    
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    return soup
    
def acessAndGetLinksInPerfil(url):
    
    soup = getPageSource(url, 1, 40)

    links = soup.find_all('a', class_='af ag ah ai aj ak al am an ao ap aq ar as at')
    
    pattern = re.compile(r'^/@.+/.+$')

    for link in links:
        href = link.get('href')
        if href and pattern.match(href):
            text = "https://medium.com" + href
            if text is not None:
                unique_links_post.add(text)
                
    try:
        
        with open(f'./scraping_MediumV2/linksPaper-{token}.txt', 'w', encoding='utf-8') as arquivo:
            for link in unique_links_post:
                arquivo.write(link + '\n')
    except:
        print("Error save in file")
    
def getOtherTags(soup):

    elementoToken = soup.find_all('a', class_=re.compile(r'.*ax am ao'))

    filterElement = re.compile(r'/tag/(.*?)(?:\?source|$)')

    for element in elementoToken:
        match = filterElement.search(element['href'])
        if match:
            tag_value = match.group(1)
            tagToken.add(tag_value)
    
def getData(url, token):
    
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
    
    info['token'] = token
    info['link'] = url
    if title:
        title = title.text
        info['title'] = title 
       
    else:
        info['title'] = 'false' 
    
    if subtitle:
        subtitle = subtitle.text
        info['subtitle'] = subtitle
       
    else:
        info['subtitle'] = 'false'
    
    if autorName:
        autorName = autorName.text
        info['autorName'] = autorName
    
    else:
        info['autorName'] = 'false'
        
    if imageAutor:
        imageAutor = imageAutor['src']
        info['imageAutor'] = imageAutor
       
    else:
        info['imageAutor'] = 'false'
        
    if clap:
        clap = clap.text
        info['clap'] = clap
        
    else:
        info['clap'] = 'false'

    if responses:
        responses = responses.text
        info['response'] = responses
        
    else:
        info['response'] = 'false'
    
    if timeForRead:
        timeForRead = timeForRead.text
        info['timeForRead'] = timeForRead
        
    else:
        info['timeForRead'] = 'false'
        
    if dateCreate:
        dateCreate = dateCreate.text
        info['dateCreate'] = dateCreate
        
    else:
        info['dateCreate'] = 'false'
    
    if post:
        text_list = []

        for tag in post:
            text_list.append(str(tag.text) +'\n')

        info['text'] = text_list.copy()

        text_list.clear()
    else:
        info['text'] = 'false'
    
    getOtherTags(soup)
    
    info['tagsPost'] = []
    
    for tag in tagToken:
        info['tagsPost'].append(tag)
    
    print(info['tagsPost'])

    jsonImport(info, token)
 
def main():
    for token in tokens:
        url = f'https://medium.com/tag/{token}/archive'
        print(url)
        print("1 Step: ")
        sleep(5)
        acessAndGetLinksInPerfil(url)
        print("2 Step: ")
        for acessPost in unique_links_post:
            getData(acessPost, token)
        unique_links.clear()
        unique_links_post.clear()
        tagToken.clear()
 
#getOtherTags()
#getData('https://medium.com/@bajrang1081siyag/blackhole-attacks-and-sinkhole-attacks-in-iot-networks-a64542380129?source=tag_archive---------277----------------------------', 'iot')       
main()
