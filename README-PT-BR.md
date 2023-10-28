# Scraping Medium

## Descrição do Código
Este código é um script Python que realiza a raspagem (scraping) de dados de artigos no Medium relacionados a diferentes tópicos (tokens). Ele utiliza a biblioteca Selenium para interagir com um navegador da web, a biblioteca BeautifulSoup para analisar o HTML das páginas e a biblioteca re (expressões regulares) para manipular strings. O código é executado no modo "headless", o que significa que não exibe uma interface gráfica do navegador durante a execução.

## Bibliotecas Necessárias
Para executar o código, você precisa ter as seguintes bibliotecas Python instaladas:

- `selenium`: Usado para automação de navegação.
- `beautifulsoup4`: Utilizado para análise de páginas da web.
- `unicodedata`: Usado para lidar com caracteres Unicode.
- `json`: Essencial para trabalhar com dados em formato JSON.
- `re`: Essa biblioteca é utilizada para operações de expressões regulares, o que é útil para encontrar e extrair informações específicas de texto.
- `time`: A biblioteca time é usada para introduzir atrasos no script, permitindo que o navegador tenha tempo suficiente para carregar as páginas ou para sincronização durante a execução do script.

## Instalação

Antes de executar o projeto, certifique-se de ter instalado as bibliotecas necessárias. Você pode instalar as bibliotecas com o seguinte comando:

```bash
pip install selenium
pip install beautifulsoup4
pip install json
pip install unicodedata
pip install re
pip install time
```

## Estrutura do JSON

Os dados coletados são armazenados em arquivos JSON com a seguinte estrutura:
```json
{
    "token": "nome_do_token",
    "link": "url_do_artigo",
    "title": "título_do_artigo",
    "subtitle": "subtítulo_do_artigo",
    "autorName": "nome_do_autor",
    "imageAutor": "url_da_imagem_do_autor",
    "clap": "número_de_claps",
    "response": "número_de_respostas",
    "timeForRead": "tempo_de_leitura",
    "dateCreate": "data_de_criação",
    "text": ["conteúdo_do_artigo_em_parágrafos"],
    "tagsPost": ["tags_associadas_ao_artigo"]
}
```

## Funcionamento do Código
O código começa definindo uma lista de tokens (tópicos) relacionados a artigos no Medium. Em seguida, ele percorre esses tokens e realiza as seguintes etapas:

1. Acessa a página de perfil de um token específico no Medium e coleta os links para os artigos relacionados.
2. Para cada link de artigo coletado, o código faz a raspagem das informações do artigo, como título, autor, número de claps, etc.
3. As informações do artigo são armazenadas em um dicionário no formato JSON.
4. Todas as informações são escritas em um arquivo JSON correspondente ao token.
5. Dessa forma, o código permite coletar informações sobre artigos no Medium relacionados a diferentes tópicos e armazenar essas informações em arquivos JSON para posterior análise ou processamento.
