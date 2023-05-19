
#REQUISITOS PREVIOS: 

"""
1. Navegador (Chrome/Mozilla)
2. Editor de texto (ST/VSC/Otro) 
3. Python 3 (Path y Pip) 
4. Librerias: por cmd como administrador, ejecutar "pip install libreria" con cada libreria no incluida.
"""

#print(sys.path) #Muestra los path de donde toma las librerias
#help('modules') #Ver modulos default e instalados. 

#LIBRERIAS
#import pathlib  
#import os
#import datetime
#import logging
import time as TM
#import sys
#import openpyxl as OPX
#import pandas as pd
#import numpy  as np
import DataSource as dataExcel


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


#Abre y/o instala webdriver
global driver
driver=webdriver.Chrome(ChromeDriverManager().install())

#FUNCION PROVISORIA HASTA CREAR EL MODULO
def reactivacion():
		#Reactivacion de la pagina
		try:
			driver.switch_to.window(driver.window_handles[0])
			TM.sleep(1)
			frame1=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'application-EnterpriseProject-searchWD')))
			frame2=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@style,'display: block; width')]")))
			TM.sleep(1)
			print('Proximo proyecto')
		except:
			print('No se pudo reactivar la pagina')
			
#WEB - INICIO
def sapAuto():
	#driver=webdriver.Chrome(ChromeDriverManager().install()) #Abre y/o instala webdriver
	driver.implicitly_wait(20) #Cuando algo no aparece, prueba cada 1 seg. durante 20 seg. 
	driver.delete_all_cookies()
	#WEB - LOGIN
	#logger.debug(" Iniciando navegador Web.")
	driver.get('https://proyectos.movistar.com.ar/sap/bc/ui2/flp#EnterpriseProject-searchWD?sap-ui-tech-hint=WDA')
	
	driver.maximize_window()
	print("First window title = " + driver.title)
	TM.sleep(4)
	try:
		#INPUT-USER # sbrega	# Junio2022
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
		quit() #Si no se puede loguear termina la ejecucion
	
	#Tomamos los datos del Excel como una Lista  de dos dimensiones lista[][] y la convertimos en Strings.
	#PROCESAR EL EXCEL	
	dataExl = dataExcel.DataSource().xlData() # creamos el obj para leer los datos del Excel
	
	#VALIDACION------------------------
	validacion = dataExcel.DataSource() # Objeto para la Validacion
	causa = dataExcel.DataSource() #Objeto para escribir la causa de la Falla
	coord = dataExcel.DataSource().getCoord() #Generamos el objeto para coordenadas de celdas
	#----------------------------------
	
	print(dataExl,type(dataExl))
	print(len(dataExl))
	
	#Iteracion para recorrer las filas del Excel desde la Fila 1
	for fila in range(1, len(dataExl)):
		global count # Contador de Alertas 
		count = 0 # Iniciamos el Contador de Alertas
		#print(fila)
		
		#Se verifica si el Proyecto fue procesado o No
		estadoProyecto = str(dataExl[fila][5])
		if estadoProyecto == 'Procesado':
			print('Proyecto Procesado...')
			continue #Sigue con la proxima fila del Excel
		else:
			print('Proyecto No Procesado...')
			pass
		
		proyectoNum = str(dataExl[fila][0]) # fila=1 , Col=0 Tomamos el numero de Proyecto
		print(proyectoNum,type(proyectoNum))
		
		#INPUT-Numero de Proyecto
		try:
			if proyectoNum != None:	
				driver.find_element(By.ID,"WD92").clear() #Limpia el campo del proyecto
				TM.sleep(2)
				driver.find_element(By.ID,"WD92").send_keys(proyectoNum)
				
			else:
				print('Sin proyecto para procesar')
				#validacion.writeXl(coord[fila][5],0) # pasamos la celda y Flag de "NO Procesado"
				continue # Sigue con la proxima Fila
					
			#BTN-Buscar
			driver.find_element(By.ID,"WDDD").click() #Click al Boton Buscar
			TM.sleep(1)
			driver.find_element(By.PARTIAL_LINK_TEXT,proyectoNum).click() # Click al proyecto
			
			#switch window in x seconds
			TM.sleep(15)
		except:
			print ('NO SE PROCESO EL NUMERO DE PROYECTO')
			print ('SEGUIR CON LA SIGUENTE FILA')
			reactivacion()
			continue # Sigue con la proxima Fila
		
		# CONTROL DEL FRAME DEL PROYECTO
		try:
			#Activamos la pagina del proyecto (Segunda Windows Handles)
			driver.switch_to.window(driver.window_handles[1]) 
			print(driver.window_handles)
			
			#Esperamos que iframe este Activo
			busca_iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div/div/iframe')))
			print("iframe encontrado ok.", busca_iframe)
			driver.maximize_window()
			
			#CONTROL DEL POPUP
			try:
			#Se verifica si el proyecto NO esta bloqueado
				WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
				print('El Proyecto NO se encuentra Bloqueado, se sigue con el proceso')
			except:
				print('EL PROYECTO ESTA BLOQUEADO...')
				while(WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/span/span/span/span'), 'El desbloqueo es automatico si no se trata. Intente en un par de minutos'))):#Verifica si esta el mensaje de proyecto bloqueado y cierra el popup
					driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
					TM.sleep(1)
					print('Encontro el pop-Up')
				
		except:
			print('FALLO EL MANEJO DEL IFRAME....O EL PROYECTO ESTA BLOQUEADO...')
			validacion.writeXl(coord[fila][5],'No Procesado') # pasamos la celda y la validación
			causa.causa(coord[fila][6], 'Proyecto Bloqueado') # Pasamos la celda y la causa de la falla
			#Intentamos Cerrar el proyecto del boton
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			TM.sleep(1)
			reactivacion()#Reactivacion de la pagina		
			continue # Sigue con la proxima Fila			
				
		#ELECCION DE LA TAREA (Mediante el boton Buscar)
		try:
			actions = ActionChains(driver)
			
			#Leo del Excel la tarea a procesar		
			tarea = dataExl[fila][1]
			print('Tarea: ',tarea, type(tarea))
			print(driver.window_handles)
			
			#Click al menu Buscar
			driver.find_element(By.XPATH, '//*[@id="WD67-title"]').click()
			TM.sleep(3)
			
			#Click al menu desplegable
			driver.find_element(By.XPATH, '//*[@id="WD0324-r"]').click()
			TM.sleep(1)
			
			#Opcion "Tarea"
			driver.find_element(By.XPATH, '//*[@id="WD0329"]').click()
			TM.sleep(1)
					
			#Campo Denominación, pego la tarea
			driver.find_element(By.XPATH,'//*[@id="WD03AE-r"]').click()
			TM.sleep(1)
			driver.find_element(By.XPATH,'//*[@id="WD03AE"]').send_keys(tarea)
			TM.sleep(1)
			actions.send_keys(Keys.ENTER).perform() #Enter
			
			#Click al menu Numero
			driver.find_element(By.XPATH,'//*[@id="WD041A-text"]').click()
			TM.sleep(2)
			
		except:
			print("Exception :NO SE PUDO PROCESAR LA TAREA")
			validacion.writeXl(coord[fila][5],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][6], 'No se pudo procesar la tarea') # Pasamos la celda y la causa de la falla
			TM.sleep(1)
			#Intentamos Cerrar el proyecto del boton
			try:
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				
			except:
				driver.close()#Fuerza el cierre del proyecto
				
			reactivacion()#Reactivacion de la pagina
			continue # Sigue con la proxima Fila										
			
		
		#PROCESAMIENTO DEL CAMPO		
		try:		
			campo = dataExl[fila][2]
			print('Campo: ',campo, type(campo))
			match campo:
				case 'Modificar status':
					#Click en Datos Basico
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[1]/div[1]').click()
					TM.sleep(1)
					#Click en Modificar Status
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[15]/td[2]/div/div/table/tbody/tr/td[1]/span/input').click()
					TM.sleep(1)
				
				case 'Fecha prevista inicio':
					fecha = dataExl[fila][4]
					
					#Click al Menu Fechas y trabajo
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[2]/div[1]').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').clear()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').send_keys(fecha)
				
				case 'Fecha prevista Final':
					fecha = dataExl[fila][4]
					
					#Click al Menu Fechas y trabajo
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[2]/div[1]').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').clear()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').send_keys(fecha)
														
				case 'Fecha prevista inicio/Final':
					fecha = dataExl[fila][4]
					fechas = fecha.split('/') # Divide el Texto por /
					print(fecha)
					print(fechas)
					fechaInicio = fechas[0]
					fechaFin = fechas[1]
					print(fechaInicio)
					print(fechaFin)
					
					#Click al Menu Fechas y trabajo
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[2]/div[1]').click()
					TM.sleep(1)
					#Inicio
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').clear()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[1]/span/input').send_keys(fechaInicio)
					#Final
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').click()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').clear()
					TM.sleep(1)
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[6]/td[2]/div/div/table/tbody/tr/td[3]/span/input').send_keys(fechaFin)
													
				case 'Emisión de PDG':
					WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ''))).click()				
				
				case 'Formulario Instalación de Sitio':
					driver.find_element(By.XPATH, '').click()
								
				case 'Carga de Materiales':
					driver.find_element(By.XPATH, '').click()
															
				case _:
					print('No existe el campo')
					validacion.writeXl(coord[fila][5],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
					causa.causa(coord[fila][6], 'No existe el Campo para procesar') # Pasamos la celda y la causa de la falla
					#Intentamos Cerrar el proyecto del boton
					try:
						WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
						
					except:
						driver.close()#Forzamos el cierre del proyecto
										
					reactivacion()#Reactivacion de la pagina
					continue # Sigue con la proxima Fila	
		except:
			print('Exception :NO SE PROCESO EL CAMPO')
			validacion.writeXl(coord[fila][5],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][6], 'Exception: No se pudo procesar el campo') # Pasamos la celda y la causa de la falla
			#Intentamos Cerrar el proyecto del boton
			try:
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					
			except:
				driver.close()#Forzamos el cierre del proyecto
				
			reactivacion()#Reactivacion de la pagina	
			continue # Sigue con la proxima Fila					
			# PENDIENTE "CAMPO A MODIFICAR"
		
		#ACCION A REALIZAR: depende deL CAMPO y la TAREA
		try:
			#Leo del excel la accion a realizar "para la tarea en curso"
			accion = dataExl[fila][3]
			print(accion)
			match accion:
				case 'Cerrar':
					#Click a la opcion Cerrar		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[3]').click()
					TM.sleep(1)
					#text = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input').get_attribute('value')
					#print(text)
					#Espera que aparezca el texto value="Completado - Cerrado" en el atributo "value" del elemento
					WebDriverWait(driver, 70).until(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'),'Completado - Cerrado'))
					print('Acción: Cerrar, OK')
														
				case 'Cancelar':
					#Click a la opcion Cancelar		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[2]').click()
					TM.sleep(1)
					WebDriverWait(driver, 70).until(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'),'Cancelado - Pendiente Predecesor'))						
					print('Acción: Cancelar, OK')
					
				case 'Anulación "Concluida"':
					#Click a la opcion Anulación "Concluida" 		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[2]').click()
					TM.sleep(1)
					WebDriverWait(driver, 70).until(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'),'En tratamiento - Liberado - Pendiente Predecesor'))
					print('Acción: Anulación "Concluida", OK')
								
				case 'Fecha':
					pass
					
				case _:
					print('NO EXISTE LA ACCIÓN')
					try:
						WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
						#Ver que pasa si se setea una fecha determinada y falla en la accion e intenta cerrar la ventana.
						#Lo que se ve es que al cambiar la fecha y falla la accion, al intentar cerrar el proyecto del boton cerrar aparece un popup de si se 
						#necesita grabar el cambio y como no lo trata, sigue la ejecucion y queda el proyecto abierto.
					except:
						print('No se pudo cerrar el proyecto del botón')
						driver.close()#Forzamos el cierre del proyecto
						print('Se Forzo el cierre porque fallo la ACCIÓN')
						
		except:
			print('Exception : NO SE PROCESO LA ACCIÓN A REALIZAR')
			driver.close()#Forzamos el cierre del proyecto por si falla por tiempo excedido en el Case que corresponda,luego el proyecto queda bloqueado.
			validacion.writeXl(coord[fila][5],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][6], 'Hubo algun problema al procesar la acción') # Pasamos la celda y la causa de la falla
			reactivacion()#Reactivacion de la pagina
			continue # Sigue con la proxima Fila	
			
		#GRABAR LOS CAMBIOS
		
		#CLICK AL BOTON GRABAR
		#WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div'))).click()
				
		try:#Click al Boton Grabar	
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div').click()	
			TM.sleep(1)
			
			#Verifica si hay modificaciones para grabar
			try: 
				#mensaje = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/span/span/span/span').text
				#Espera el mensaje de grabacion "Se han grabado los datos"
				WebDriverWait(driver, 80).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/span/span/span/span'), 'Se han grabado los datos'))
				print('Mensaje: Se han grabado los datos...')
				TM.sleep(1)
				#Cierra el popup 
				WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[1]/table/tbody/tr/td[3]/a'))).click()
				print('Popup cerrado')
				print('SE PUDIERON GRABAR LOS CAMBIOS...')
				TM.sleep(1)
				validacion.writeXl(coord[fila][5],'Procesado') # pasamos la celda y Flag de "Procesado"
				print('Se completo el proceso de Grabacion...')
				
			except:
				print('No se grabaron los cambios...')
				validacion.writeXl(coord[fila][5],'No procesado') # pasamos la celda y Flag de "NO Procesado"
				TM.sleep(1)
				causa.causa(coord[fila][6], 'No se pudieron grabar los cambios') # Pasamos la celda y la causa de la falla
						
		except:
			print('Except: NO SE PUDO HACER CLICK AL BOTON GRABAR')
			validacion.writeXl(coord[fila][5],'No procesado') # pasamos la celda y Flag de "NO Procesado"
			TM.sleep(1)
			causa.causa(coord[fila][6], 'No se pudieron grabar los cambios') # Pasamos la celda y la causa de la falla
			print('Proyecto Cerrado del Boton...')
						
		#cerramos el proyecto
		try:
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			print('Proyecto Cerrado del Boton...')
			TM.sleep(1)
			reactivacion()#Reactivacion de la pagina
		except:
			print('NO se pudo cerrar el proyecto del Boton...')		
		
	#Cierra For
	# termina la Ejecucion.
	exit()
	

#EJECUCIÓN
#horaInicio=datetime.datetime.now()
if __name__ == '__main__':
	sapAuto()
#horaFin=datetime.datetime.now()
#duracion=str(horaFin-horaInicio)
#logger.debug(f'Duración: '+duracion)



