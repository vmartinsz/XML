import json
from xml.etree.ElementTree import Element, SubElement, tostring

# Função para converter dados do JSON em XML para feed do Facebook com formato <rss>
def json_to_facebook_rss(json_data):
    rss = Element('rss', {'xmlns:g': 'http://base.google.com/ns/1.0', 'version': '2.0'})
    channel = SubElement(rss, 'channel')
    title = SubElement(channel, 'g:tittle')
    title.text = "Mary Kay For Life"
    link = SubElement(channel, 'g:link')
    link.text = "https://loja.marykay.com.br/"
    description = SubElement(channel, 'description')
    description.text = "<![CDATA[Mary Kay For Life]]>"

    # Iterar sobre cada produto no JSON
    for product in json_data:
        item = SubElement(channel, 'item')
        
        # ID do Produto
        g_id = SubElement(item, 'g:id')
        g_id.text = product["@id"]
        
        # Título
        g_title = SubElement(item, 'g:title')
        g_title.text = f'<![[CDATA[ {product["name"]} ]]>'
        
        # Descrição
        g_description = SubElement(item, 'g:description')
        g_description.text = f'<![[CDATA[ {product["description"]} ]]>'

        g_link = SubElement(item, 'g:link')
        g_link.text = f'<![[CDATA[ {product["@id"]} ]]>'
        
        g_image_link = SubElement(item, 'g:image_link')
        g_image_link.text = product["image"]

        # Condição do Produto
        g_condition = SubElement(item, 'g:condition')
        g_condition.text = "new"  # Condição do produto, por exemplo: new, used, refurbished
        
        g_availability = SubElement(item, 'g:availability')
        g_availability.text = "in stock" if any(offer["availability"] == "http://schema.org/InStock" for offer in product["offers"]["offers"]) else "out of stock"

        # Preço
        g_price = SubElement(item, 'g:price')
        format(5.00000, '.2f')
        g_price.text = f"{format(product['offers']['offers'][0]['price'], '.2f')} {product['offers']['offers'][0]['priceCurrency']}"
        
        # Disponibilidade
        
        # Marca
        g_brand = SubElement(item, 'g:brand')
        g_brand.text = f'<![[CDATA[ {product["brand"]["name"]} ]]>'
        
        g_google_product_category = SubElement(item, 'g:google_product_category')
        g_google_product_category.text = f"<![[CDATA[ Cosméticos ]]>"

        product_type = SubElement(item, 'g:product_type')
        product_type.text = f"<![CDATA[ Cosméticos ]]>"
    return rss


# Função para ler dados do arquivo JSON
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Caminho para o arquivo JSON
json_file_path = 'dados_json_ld_marykay.json'

# Lendo dados do arquivo JSON
json_data = read_json_file(json_file_path)

# Gerando XML
facebook_rss = json_to_facebook_rss(json_data)

# Convertendo ElementTree para string XML formatada
xml_string = tostring(facebook_rss, encoding='utf-8').decode('utf-8')

# Imprimindo XML formatado
print(xml_string)

# Salvar XML em arquivo
xml_output_path = 'facebook_product_feed.xml'
with open(xml_output_path, 'w', encoding='utf-8') as xml_file:
    xml_file.write(xml_string)

print(f'XML gerado e salvo com sucesso em "{xml_output_path}"!')
