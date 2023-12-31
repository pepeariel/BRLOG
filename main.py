import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import boto3
from dotenv import load_dotenv
import os
from datetime import datetime as dt
from functions import FileHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    # Test for diferent chrome-driver
    CHROMEDRIVER_PATH = 'chromedriver'
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                             )
    # Load local variables
    load_dotenv()

    # Credencials
    brlog_user = os.getenv('usuario')
    brlog_password = os.getenv('senha')
    aws_access_key_id =os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    bucket_name = os.getenv('bucket_name')
    s3_region = os.getenv('s3_region')

    # Selenium ChromeDriver -- UNCOMMENT TO RUN ON LOCAL MACHINE
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    # url website Brasilrisk
    url = 'http://multilog.brasilrisk.com.br'

    # Conectar ao site
    driver.get(url)
    time.sleep(20)
	
    # Registrar objeto de usuario e senha
    username = driver.find_element(By.ID, 'usuario')
    time.sleep(3)
    password = driver.find_element(By.ID, 'senha')

    time.sleep(3)
    login = driver.find_element(By.ID, 'Login')

    # Preencher com usuario e senha
    username.send_keys(brlog_user)
    time.sleep(3)
    password.send_keys(brlog_password)
    time.sleep(3)
    login.click()
    time.sleep(30)

    # Buscar a pagina de relatorio
    filtro_relatorio = driver.find_element(By.CLASS_NAME, 'material-icons')
    time.sleep(3)
    filtro_relatorio.click()
    time.sleep(3)

    # Botao relatorio
    botao_relatorio = driver.find_element(By.XPATH, '//*[@id="slide-out"]/li[10]/a')
    time.sleep(3)
    botao_relatorio.click()
    time.sleep(20)

    # Filtrar relatorio
    filtro_relatorio = driver.find_element(By.XPATH, '//*[@id="filter"]/div/div/div/div[1]/div[2]/div[1]/div/div/i')
    time.sleep(3)
    filtro_relatorio.click()
    time.sleep(3)
    coletas_entregas = driver.find_element(By.XPATH,'//*[@id="filtros_principais"]/div[1]/div/div/div[2]/div[2]')
    time.sleep(3)
    coletas_entregas.click()
    time.sleep(5)

    # Gerar o relatorio final
    gerar_relatorio = driver.find_element(By.XPATH,'//*[@id="filter"]/div/div/div/div[2]/div/a[1]')
    time.sleep(3)
    gerar_relatorio.click()
    time.sleep(300)

    # Exportar o relatorio em excel
    exportar_relatorio = driver.find_element(By.XPATH,'//*[@id="colxl3"]/button')
    time.sleep(3)
    exportar_relatorio.click()
    time.sleep(120)


    # Crate an instance of FileHandler
    Pipeline = FileHandler(aws_access_key_id, aws_secret_access_key, bucket_name, s3_region)

    # Create s3 connection
    s3 = Pipeline.create_s3_connection()

    # Save extracted excel file in parquet format
    Pipeline.excel_to_parquet()

    # Send parquet file to bucket s3
    Pipeline.send_file_to_s3(s3)
