import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json


# URL do sitemap
all_json_data = []
sitemap_url = "https://loja.marykay.com.br/sitemap/product-0.xml"

try:
    # Fazendo a requisição GET ao sitemap
    response = requests.get(sitemap_url)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseando o conteúdo XML da resposta
        root = ET.fromstring(response.content)

        # Inicializando uma lista para armazenar as URLs
        urls = []

        # Iterando sobre os elementos <url> dentro de <urlset>
        for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text.strip()
            urls.append(loc)

        # Exibindo as URLs encontradas
        for url in urls:
            try:
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')
                json_ld_script = soup.find('script', type='application/ld+json')
                
                if json_ld_script:
                    json_ld_content = json_ld_script.string
                    json_data = json.loads(json_ld_content)
                    all_json_data.append(json_data)  # Adiciona os dados JSON-LD à lista
                else:
                    print(f'Nenhum script JSON-LD encontrado na página: {url}')

            except Exception as e:
                print(f'Ocorreu um erro ao processar a URL {url}: {e}')

        # Imprime todos os dados JSON-LD coletado

    else:
        print(f"Erro ao acessar o sitemap. Código de status HTTP: {response.status_code}")
    # Nome do arquivo onde os dados serão salvos
    output_file = 'dados_json_ld_marykay.json'

    # Escreve os dados JSON-LD no arquivo
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_json_data, f, ensure_ascii=False, indent=2)
        print(f'Dados salvos com sucesso em {output_file}')
    except Exception as e:
        print(f'Ocorreu um erro ao salvar os dados no arquivo {output_file}: {e}')
except Exception as e:
    print(f"Ocorreu um erro: {e}")
