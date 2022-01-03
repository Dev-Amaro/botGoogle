from selenium import webdriver
from selenium.webdriver.common.keys import Keys

pesquisa = input("Digite a pesquisa:")

options = webdriver.ChromeOptions()
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")

driver = webdriver.Chrome('C:\\Users\\Jefferson Herbert\\Desktop\\chromedriver.exe', options=options)
driver.get("https://www.google.com")

campo = driver.find_element_by_xpath("//input[@aria-label='Pesquisar']")
campo.send_keys(pesquisa)
campo.send_keys(Keys.ENTER)

resultados = driver.find_element_by_xpath("//*[@id='result-stats']").text
print(resultados)

numero_resultado = int(resultados.split("Aproximadamente ")[1].split(' resultados')[0].replace('.',''))
maximo_paginas = numero_resultado/10

print("Número de páginas disponiveis: %s"% (maximo_paginas))

url_pagina = driver.find_element_by_xpath("//a[@aria-label='Page 2']").get_attribute("href")

pagina_atual = 0
start = 10
lista_resultados = []
while pagina_atual <= 10:
    if not pagina_atual == 0:
        url_pagina = url_pagina.replace("start=%s" % start, "start=%s" % (start+10))
        start = start + 10
        driver.get(url_pagina)
    pagina_atual = pagina_atual + 1

    divs = driver.find_elements_by_xpath("//div[@class='g']")
    for div in divs:
        nome = div.find_element_by_tag_name("h3")
        link = div.find_element_by_tag_name("a")
        resultado = "%s;%s" % (nome.text,link.get_attribute("href"))
        print(resultado)
        lista_resultados.append(resultado)


with open("resultadosPesquisa.txt", "w") as arquivo:
    for resultado in lista_resultados:
        arquivo.write("%s\n" %resultado)
    arquivo.close()

print("%s resultado encontrados do Google e salvas no arquivo resultadoPesquisa.txt" % len(lista_resultados))