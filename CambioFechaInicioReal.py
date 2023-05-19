
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
from datetime import date
from datetime import datetime


#Abre y/o instala webdriver
global text
global driver
global mensaje
global campoFecha
driver=webdriver.Chrome(ChromeDriverManager().install())

#VALIDACION------------------------
validacion = dataExcel.DataSource() # Objeto para la Validacion
causa = dataExcel.DataSource() #Objeto para escribir la causa de la Falla
coord = dataExcel.DataSource().getCoord() #Generamos el objeto para coordenadas de celdas
	#----------------------------------


def reactivacion():
		#Reactivacion de la pagina
		try:
			driver.switch_to.window(driver.window_handles[0])
			TM.sleep(1)
			frame1=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'application-EnterpriseProject-searchWD')))
			frame2=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@style,'display: block; width')]")))
			TM.sleep(1)
			print('Procesando proyecto')
		except:
			print('No se pudo reactivar la pagina')

def popupControl():
	#text = []
	#mensaje = ''
	try:
		WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
		print('El Proyecto NO se encuentra Bloqueado, se sigue con el proceso')
		
	except: 
		print('Hay una Adevertencia y/o un Error...')
		try: #para Geenracion de HEA
			while(WebDriverWait(driver, 30).until_not(EC.text_to_be_present_in_element((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))):
				driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
				TM.sleep(1)
				print('Cierra popUp')
		except:
			pass
	
#WEB - INICIO
def fechaInicioReal():
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
		driver.find_element(By.ID,'USERNAME_FIELD-inner').send_keys('aut_rda') #ACA PONER USUARIO GENERAL peppel
		#INPUT-PASS
		driver.find_element(By.ID,'PASSWORD_FIELD-inner').send_keys('Python-23') #ACA PONER PASS GENERAL Unqui2022
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
		print('NO SE PROCESO EL LOGUEO, SE TERMINA LA EJECUCION...')
		quit() #Si no se puede loguear termina la ejecucion
	
	#Tomamos los datos del Excel como una Lista  de dos dimensiones lista[][] y la convertimos en Strings.
	#PROCESAR EL EXCEL	
	dataExl = dataExcel.DataSource().xlData() # creamos el obj para leer los datos del Excel
	
	print(dataExl,type(dataExl))
	print(len(dataExl))
	
	#Iteracion para recorrer las filas del Excel desde la Fila 1
	for fila in range(1, len(dataExl)):
		#print(fila)
		#Se verifica si el Proyecto fue procesado o No
		estadoProyecto = str(dataExl[fila][3])
		if estadoProyecto == 'Procesado':
			print('Proyecto Procesado...Sigue con la proxima linea...')
			continue #Sigue con la proxima fila del Excel
		else:
			print('Proximo proyecto a procesar...')
			pass
		
		proyectoNum = str(dataExl[fila][0]) # fila=1 , Col=0 Tomamos el numero de Proyecto
		print(proyectoNum,type(proyectoNum))
		
		#Si se quiere Finalizar la ejecucion desde la planilla Excel 
		if(proyectoNum == 'Finalizar'):
			exit()
		#INPUT-Numero de Proyecto
		reactivacion()
		try:
			if (proyectoNum != 'None'):	
				driver.find_element(By.ID,"WD92").clear() #Limpia el campo del proyecto
				TM.sleep(2)
				driver.find_element(By.ID,"WD92").send_keys(proyectoNum)
				
			else:
				print('Sin proyecto para procesar')
				causa.causa(coord[fila][4], 'No Existe ningún proyecto') # Pasamos la celda y la causa de la falla
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
			#reactivacion()
			continue # Sigue con la proxima Fila
		
		# CONTROL DEL FRAME DEL PROYECTO
		try:
			flagIframe = 0
			#Activamos la pagina del proyecto (Segunda Windows Handles)
			driver.switch_to.window(driver.window_handles[1]) 
			print(driver.window_handles)
			
			#Esperamos que iframe este Activo
			busca_iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div/div/iframe')))
			print("iframe encontrado ok.", busca_iframe)
			driver.maximize_window()
			flagIframe = 1
			
			#CONTROL DEL POPUP
					
			#Se verifica si el proyecto NO esta bloqueado
			WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
			print('El Proyecto NO se encuentra Bloqueado, se sigue con el proceso')
			
		except:
			#print('FALLO EL MANEJO DEL IFRAME...O EL PROYECTO ESTA BLOQUEUADO')
			if(flagIframe == 1): #Entra al if si no falla por Iframe
				print('HAY UN POPUP...')
				mensaje=''
				flagMsgAdv = '0'
				flagMsgEr = '0'
				
				#CAPTURAMOS LOS MENSAJES
				try:
					#Caputura mensaje de Adevertencia
					mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div/div/div/table/tbody/tr/td/div/div[2]/div[1]/div[4]').get_attribute('title')	
					print(mensaje,type(mensaje))
					mensaje = mensaje.split()
					flagMsgAdv = int (mensaje[1]) # indica que hay un mensaje de Advertencia y el proyecto SI se puede porcesar
				except:
					print('No hay mensaje de Adevertencia')	
		
				try:	
					#Captura mensaje de Error
					mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div/div/div/table/tbody/tr/td/div/div[2]/div[1]/div[3]').get_attribute('title')	
					print(mensaje,type(mensaje))
					mensaje = mensaje.split()
					flagMsgEr = int (mensaje[1]) # Indica que hay un mensaje de Error y el proyecto NO se puede precesar.
				except:
					print('No hay mensaje de Error')		
				#print(text, type(text))

				#PROCESAMOS LOS MENSAJES CAPTURADOS SEGUN EL TIPO DE MESAJE
				if (flagMsgAdv >= 1 and flagMsgEr == 0):# Si hay algun mensaje de advertencia lo cierra y sigue procesando el proyecto
					try:
						driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
						TM.sleep(1)
						print('Se cerro el mensaje de advertencia...Sigue procesando el proyecto')
						
					except:
						pass					

				elif(flagMsgEr >= 1):
					try:
						while(WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))):#Verifica si esta el mensaje de proyecto bloqueado y cierra el popup
							driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
							TM.sleep(1)
							print('Se cierra el mensaje de error...se debe continuar con el proximo proyecto')
					except:
						pass		
			else:
				print('FALLO EL MANEJO DEL IFRAME...')
			
			#Se interrumpe el procesamiento del proyecto en caso que falle por Iframe o el proyecto este Bloqueado.			
			if(flagMsgEr >= 1 or flagIframe == 0):
				try:#Cierro el proyecto del boton.
					WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					TM.sleep(1)
				except:
					pass
				validacion.writeXl(coord[fila][3],'No Procesado') # pasamos la celda y la validación
				causa.causa(coord[fila][4], 'Fallo el IFRAME o el Proyecto esta bloqueado') # Pasamos la celda y la causa de la falla
				TM.sleep(1)
				#reactivacion()#Reactivacion de la pagina		
				continue # Sigue con la proxima Fila	
					
				
		#ELECCION DE LA TAREA (Mediante el boton Buscar)
		try:
			actions = ActionChains(driver)
			
			#Leo del Excel la tarea a procesar		
			tarea = dataExl[fila][1]
			print('Tarea: ',tarea, type(tarea))
			
			#print(driver.window_handles)
			
			#Click al menu Buscar
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/div/span[5]/span[2]').click()
			TM.sleep(3)
			
			#Click al menu desplegable
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[3]/td[1]/div/div/div/div/table/tbody/tr[2]/td[2]/span').click()
			TM.sleep(1)
			
			#Opcion "Tarea"
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[4]').click()
			TM.sleep(1)
					
			#Campo Denominación, pego la tarea
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[4]/td[2]/span').click()
			TM.sleep(1)
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[4]/td[2]/span/input').send_keys(tarea)
			TM.sleep(1)
			actions.send_keys(Keys.ENTER).perform() #Enter
			
			#Click al menu Numero
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[6]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[1]/a').click()
			TM.sleep(2)
			
		except:
			print("Exception :NO SE PUDO PROCESAR LA TAREA")
			validacion.writeXl(coord[fila][3],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][4], 'No se pudo procesar la tarea') # Pasamos la celda y la causa de la falla
			TM.sleep(1)
			#Intentamos Cerrar el proyecto del boton
			try:
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				
			except:
				driver.close()#Fuerza el cierre del proyecto
				
			#reactivacion()#Reactivacion de la pagina
			continue # Sigue con la proxima Fila										
			
		
		#PROCESAMIENTO DEL CAMPO		
	
		mensaje = ''
		mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input').get_attribute('value')

		if ('Completado' in mensaje):
			print('Proyecto Cerrado o Cancelado no se puede cambiar la fecha')
			validacion.writeXl(coord[fila][3],'Procesado') # pasamos la celda y Flag de "Procesado"
			causa.causa(coord[fila][4], 'No se pudo cambiar la fecha porque la tarea esta Completada') # Pasamos la celda y la causa
		
		else:
			try:
				today = date.today()
				# dd/mm/YY
				fecha = today.strftime("%d.%m.%Y")
				print("fecha =", fecha)

					
				#Click al Menu Fechas y trabajo 
				driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[2]/div[1]').click()
				TM.sleep(1)
				

				campoFecha = ''
				flagGrabacion = 0
				campoFecha = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[15]/td[2]/span/input').get_attribute('value')
				if (campoFecha==''):
					#Click en Fecha Inicio Real                  
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[15]/td[2]/span/input').click()
					TM.sleep(1)
					#Limpiar campo donde se coloca la fecha				
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[15]/td[2]/span/input').clear()
					TM.sleep(1)
					#Colocamos la fecha del dia
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr[15]/td[2]/span/input').send_keys(fecha)
					flagGrabacion = 1 # Si hay datos para grabar

			except:
				print('Exception :NO SE PROCESO EL CAMBIO DE FECHA')
				validacion.writeXl(coord[fila][3],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
				causa.causa(coord[fila][4], 'Exception: Error al querer cambiar la fecha') # Pasamos la celda y la causa de la falla
			
				#Intentamos Cerrar el proyecto del boton
				try:
					WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					
				except:
					driver.close()#Forzamos el cierre del proyecto
				
				#reactivacion()#Reactivacion de la pagina	
				continue # Sigue con la proxima Fila					
				# PENDIENTE "CAMPO A MODIFICAR"
		
		
						
		#GRABAR LOS CAMBIOS
		
		#CLICK AL BOTON GRABAR
		#WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div'))).click()
				
		try:#Click al Boton Grabar	
			if(flagGrabacion == 1):
				driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div').click()	
				TM.sleep(1)
					
				#Verifica si hay modificaciones para grabar
				#mensaje = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/span/span/span/span').text
				#Espera el mensaje de grabacion "Se han grabado los datos"
				WebDriverWait(driver, 300).until_not(EC.text_to_be_present_in_element((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
				#WebDriverWait(driver, 300).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/span/span/span/span'), 'Se han grabado los datos'))
				print('Mensaje: Se han grabado los datos...')
				TM.sleep(1)
				#Cierra el popup 
				WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[1]/table/tbody/tr/td[3]/a'))).click()
				print('Popup cerrado')
				print('SE PUDIERON GRABAR LOS CAMBIOS...')
				TM.sleep(1)
				#validacion.writeXl(coord[fila][5],'Procesado') 
				print('Se completo el proceso de Grabacion...')
				causa.causa(coord[fila][4], 'OK')
				#Cerramos el proyecto del boton
				#WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				
			else:
				try:#Intento cerrar del boton
					#WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					print('Ya hay dato de Fecha')
					causa.causa(coord[fila][4], 'Ya hay dato de Fecha')
					#validacion.writeXl(coord[fila][5],'Procesado') 
					#causa.causa(coord[fila][6], mensaje[1])
					#reactivacion()#Reactivacion de la pagina
				except:
					pass
			
			WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			validacion.writeXl(coord[fila][3],'Procesado') 		
			#causa.causa(coord[fila][6], 'OK')	
			#reactivacion()#Reactivacion de la pagina			
		except:
			print('Except: NO SE PUDO HACER CLICK AL BOTON GRABAR')
			try:#Intento cerrar del boton
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			except:
				#driver.close()#Forzamos el cierre del proyecto
				print('Se Forzo el cierre porque fallo la ACCIÓN')
			
			validacion.writeXl(coord[fila][3],'No procesado') # pasamos la celda y Flag de "NO Procesado"
			TM.sleep(1)
			causa.causa(coord[fila][4], 'No se pudieron grabar los cambios') # Pasamos la celda y la causa de la falla
			#reactivacion()#Reactivacion de la pagina			
		
		
	#Cierra For
	# termina la Ejecucion.
	exit()
	

#EJECUCIÓN
#horaInicio=datetime.datetime.now()
if __name__ == '__main__':
	fechaInicioReal()

#horaFin=datetime.datetime.now()
#duracion=str(horaFin-horaInicio)
#logger.debug(f'Duración: '+duracion)



