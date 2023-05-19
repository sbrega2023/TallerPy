'''
Created on 11 nov. 2022

@author: sbrega
'''
import pathlib  
import os
import datetime
import logging
import time as TM
import sys
import openpyxl as OPX
import pandas as pd
import numpy  as np
import DataSource as dataExcel

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def main():
    global action
    
    driver = webdriver.Chrome(ChromeDriverManager().install()) #Abre y/o instala webdriver
    driver.implicitly_wait(20) #Cuando algo no aparece, prueba cada 1 seg. durante 20 seg. 
    driver.delete_all_cookies()
    #WEB - LOGIN
    #logger.debug(" Iniciando navegador Web.")
    driver.get('https://proyectos.movistar.com.ar/sap/bc/ui2/flp#EnterpriseProject-searchWD?sap-ui-tech-hint=WDA')
    
    driver.maximize_window()
    print("First window title = " + driver.title)
    TM.sleep(4)
    try:
        #INPUT-USER # sbrega    # Junio2022
        driver.find_element(By.ID,'USERNAME_FIELD-inner').send_keys('sbrega') #ACA PONER USUARIO GENERAL
        #INPUT-PASS
        driver.find_element(By.ID,'PASSWORD_FIELD-inner').send_keys('Junio2022') #ACA PONER PASS GENERAL
        #BTN-ACEPTAR
        driver.find_element(By.XPATH,'//*[@id="LOGIN_LINK"]/span[1]').click()
        
        TM.sleep(10)
        print("Espera lista, buscando...")
        #ENTRAR A MARCO 1:
        frame1=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'application-EnterpriseProject-searchWD')))
        print("Frame1 encontrado ok.")
        #ENTRAR A MARCO 2:
        frame2=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@style,'display: block; width')]")))
        print("Frame2 encontrado ok.")
    except:
        print('NO SE PROCESO EL LOGUEO')
    
    #Tomamos los datos del Excel como una Lista  de dos dimensiones lista[][] y la convertimos en Strings.
    #PROCESAR EL EXCEL    
    dataExl = dataExcel.DataSource.xlData()
    print(dataExl,type(dataExl))
    print(len(dataExl))
    #actions = ActionChains(driver)
    for fila in range(1, len(dataExl)):
        print(fila)    
        proyectoNum = str(dataExl[fila][0]) # fila=1 , Col=0
        print(proyectoNum,type(proyectoNum))
        
        #INPUT-Numero de Proyecto
        try:
            
            if proyectoNum!=None:    
                driver.find_element(By.ID,"WD92").clear() #Limpia el campo del proyecto
                TM.sleep(1)
                driver.find_element(By.ID,"WD92").send_keys(proyectoNum)
                
            else:
                print('Sin proyecto para procesar')
            
            #BTN-Buscar
            driver.find_element(By.ID,"WDDD").click()
            driver.find_element(By.PARTIAL_LINK_TEXT,proyectoNum).click()    
            #abrirProyecto = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,proyectoNum))).click()
            #print("First window title = " + driver.title)
            
            TM.sleep(15)
        except:
            print ('NO SE PROECSO EL NUMERO DE PROYECTO')    
        
        # Control del Frame del proyecto
        try:
            driver.switch_to.window(driver.window_handles[1]) #window_handles[1] is a second window
            
            #busca_iframe = driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div/div/iframe' )) #Xpath del iframe que contiene el pop-up
            print(driver.window_handles)
            
            busca_iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div/div/iframe')))
            print("iframe encontrado ok.", busca_iframe)
            #driver.maximize_window()
                    
            #Manejo de Alerta
            for i in range(4):
                print(i)
                TM.sleep(1)
                boton_x = driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click()# click a la x del pop-up
                        
        except:
            print("NO SE PUDO PROCESAR EL FRAME DEL PROYECTO")
        #CERRAR
        try:
            #CLICK AL BOTON CERRAR EL PROYECTO
            print(driver.window_handles)
            
            #driver.find_element(By.PARTIAL_LINK_TEXT, "Cerrar aplicación") # 0:'Cerrar'
            
            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
            #driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div').click()
            #/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span/div
            print(driver.window_handles)
            #===================================================================
            TM.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            TM.sleep(1)
            #driver.refresh()
                       
            frame1=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'application-EnterpriseProject-searchWD')))
            print("Frame1 encontrado ok.")
            #ENTRAR A MARCO 2:
            frame2=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@style,'display: block; width')]")))
            print("Frame2 encontrado ok.")
            print('Cerrar boton')
            TM.sleep(1)
        except:
            print('NO CERRO EL PROYECTO')    
    driver.close()
    driver.quit()   
        
        

if __name__ == '__main__':
    main()