from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime

dh_inicio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

print('Iniciando rotina - ', dh_inicio)

links = []
phones = []
pagina = 1
qtd_phones = 0
phones_solicitados = 100

driver = webdriver.Chrome()

print('Buscando links - ', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
while qtd_phones <= phones_solicitados and 'Ooooooopss....' not in driver.title:
    try:
        driver.get(f'https://www.tudocelular.com/celulares/fichas-tecnicas_{pagina}.html?o=2')
        elementos = driver.find_elements(By.XPATH, '//*[@id="cellphones_list"]/article')

        for elemento in elementos:
            tag_link = elemento.find_element(By.TAG_NAME, 'a')
            link_adress = tag_link.get_attribute('href')
            if link_adress not in links:
                links.append(link_adress)
                qtd_phones += 1
    except:
        pass
    pagina += 1

qtd_phones = 1
# Processo que busca os dados de cada celular.
for link in links:
    # verificação para evitar muitos prints
    if qtd_phones == 1 or (qtd_phones % 50) == 0:
        print(f'Buscando novos modelos - {qtd_phones} - ', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    phone_atual = []
    driver.get(link)

    # busca titulo
    titulo = driver.find_element(By.XPATH, '//*[@id="fwide_column"]/h2').text
    phone_atual.append(titulo)

    # busca o melhor preço, e caso não exista a informação no site, informa caminho correto para o proximo passo
    try:
        melhor_preco = driver.find_element(By.XPATH, '//*[@id="phone_columns"]/div/ul[2]/li[1]/a[1]').text
        referencia_notas = 3
    except:
        melhor_preco = None
        referencia_notas = 2
    phone_atual.append(melhor_preco)

    # busca os nomes de cada avaliação (nota), com base no que foi disponibilizado pelo site
    notas_titulos = []
    elemento_nome = driver.find_elements(By.XPATH, f'//*[@id="controles_titles"]/div/ul[{referencia_notas}]')
    for elemento in elemento_nome:
        nome = elemento.text
        nome = nome.replace('\n', ';').replace('- ', '')
        itens_nome = nome.split(';')
        notas_titulos.extend(itens_nome)
    
    # busca os valores de cada avaliação (nota)
    notas_valores = []
    elemento_valor = driver.find_elements(By.XPATH, f'//*[@id="phone_columns"]/div/ul[{referencia_notas}]')
    for elemento in elemento_valor:
        notas = elemento.text
        notas = notas.replace('\n', ';')
        itens_valor = notas.split(';')
        notas_valores.extend(itens_valor)
    
    # une a chave (nome) da avaliação com o valor
    avaliacoes = {}
    for i in range(len(notas_titulos)):
        avaliacoes[notas_titulos[i]] = notas_valores[i]

    phone_atual.append(avaliacoes)

    # junta as informação na lista principal
    phones.append(phone_atual)
    qtd_phones += 1

driver.quit()
print('Formatando dados - ', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

# processo de formatação dos dados de acordo com a necessidade de exibição
columns = ['modelo', 'melhor_valor', 'avaliacoes']
dados = pd.DataFrame(phones, columns=columns)
dados = dados.set_index(['modelo', 'melhor_valor'])['avaliacoes'].apply(pd.Series).stack().reset_index()
dados.columns = ['modelo', 'melhor_valor', 'aval_nome', 'aval_nota']
dados['aval_nota'] = dados['aval_nota'].str.split(' / 10').str[0]
dados = dados.pivot_table(index=['modelo', 'melhor_valor'], columns='aval_nome', values='aval_nota', aggfunc='first').reset_index()

dados['Custo-benefício'] = dados['Custo-benefício'].astype(float)
dados['Câmera'] = dados['Câmera'].astype(float)
dados['Desempenho'] = dados['Desempenho'].astype(float)
dados['Hardware'] = dados['Hardware'].astype(float)
dados['Tela'] = dados['Tela'].astype(float)

dados['nota_final'] = dados['Custo-benefício'] + dados['Câmera'] + dados['Desempenho'] + dados['Hardware'] + dados['Tela']
dados['nota_final'] /= 5

# Criação / Atualização do arquivo excel que contem os dados
dados.to_excel('dados.xlsx')

print(f'Rotina finalizada com sucesso! - {qtd_phones} celulares encontrados!', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
