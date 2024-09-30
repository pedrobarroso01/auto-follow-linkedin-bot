import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_email = ""
user_password = ""
validate_email = False

#Filtros do usuário
filtros = input("Digite os filtros que deseja (separados por ; Ex: python;R) ")

#Digitar email, senha e validações

while True:
    if validate_email == False:
        user_email = input("Digite seu email: ")
        if user_email != "" and "@" in user_email:
            validate_email = True
        else:
            continue
    user_password = input("Digite sua senha: ")
    if len(user_password) >= 6:
        break


#Iniciar navegador
navegador = webdriver.Chrome()
navegador.get("https://br.linkedin.com/")

#Clicar no botão de login
WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > nav > div > a.nav__button-secondary.btn-secondary-emphasis.btn-md'))
).click()


#Fazer Login
try:
    caixa_email = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[1]/input"))
    )
    caixa_email.send_keys(user_email)

    caixa_senha = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[2]/input"))
    )
    caixa_senha.send_keys(user_password)

    WebDriverWait(navegador, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
    ).click()
    
except:
    print("Erro ao logar")

#Realizar pesquisa dos filtros
try:
    clicar_pesquisa = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-search > div > button'))
    )
    clicar_pesquisa.click()

    # Selecionar o campo de entrada de pesquisa
    campo_pesquisa = WebDriverWait(navegador, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Pesquisar"]'))
    )

    # Inserir os filtros na barra de pesquisa
    campo_pesquisa.send_keys(filtros)

    # Pressionar Enter para realizar a pesquisa
    campo_pesquisa.send_keys(Keys.ENTER)

    #Botões da navbar
    botoes = WebDriverWait(navegador, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.artdeco-pill"))
    )
    # Procura pelo botão que contém o texto "Pessoas" e clica
    for botao in botoes:
        if "Pessoas" in botao.text:
            botao.click()

except Exception as e:
    print(f"Erro ao realizar a pesquisa: {e}")


try:
    while True:
        # Verifica se há botões de seguir na página
        try:
            botoes_seguir = WebDriverWait(navegador, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[aria-label^='Seguir']"))
            )
        except Exception as e:
            botoes_seguir = []
            print(f"Erro ao buscar botões de seguir: {e}")

        if botoes_seguir:
            for botao in botoes_seguir:
                try:
                    botao.click()
                    print("Seguiu uma pessoa.")
                    time.sleep(2)
                except Exception as e:
                    print(f"Erro ao clicar em um botão de seguir: {e}")
                    continue
        else:
            print("Não há mais perfis para seguir nessa página.")
            try:
                navegador.execute_script("window.scrollTo(10, document.body.scrollHeight);")
                # Espera o botão "Avançar" estar presente
                button_avancar = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Avançar')]"))
                )
                print("Botão 'Avançar' encontrado.")                
                button_avancar.click()
                time.sleep(2)

            except Exception as e:
                print(f"Erro ao tentar avançar: {e}")



except Exception as e:
    print(f"Erro ao seguir perfis: {e}")

# Manter o navegador aberto
try:
    while True:
        time.sleep(1000)
except KeyboardInterrupt:
    print("Encerrando o navegador.")
    navegador.quit()


