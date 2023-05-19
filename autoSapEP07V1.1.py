
#REQUISITOS PREVIOS: 

"""
1. Navegador (Chrome/Mozilla)
2. Editor de texto (ST/VSC/Otro) 
3. Python 3 (Path y Pip) 
4. Librerias: por cmd como administrador, ejecutar "pip install libreria" con cada libreria no incluida.
"""

#Tareas pendientes
# Ver de agregar en la causa si esta completado cerrado o completado Pediente de Predecesor - OK
# Se agrega una columna de usuario como input, hay que modificar las posiciones del excel. - OK
# Agregar columna con la fecha y hora de Procesado
#


#print(sys.path) #Muestra los path de donde toma las librerias
#help('modules') #Ver modulos default e instalados. 

#LIBRERIAS
#import pathlib  
import os
import datetime
import logging
import time as TM
#import sys
#import openpyxl as OPX
#import pandas as pd
#import numpy  as np
import DataSource as dataExcel


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from openpyxl.descriptors.base import DateTime
from CambioFechaInicioReal import fechaInicioReal



#Abre y/o instala webdriver
global text
global driver
global mensaje




#LOG - CREACION E INICIO
#D:\Movistar_Argentina\Programacion-Desarrollos\Ejercicios\Log_AutoSapEP003
# C:/Users/pereyragu/OneDrive - Telefonica/AutoPython/Desarrollo/Logs/
log=f'D:\Movistar_Argentina\Programacion-Desarrollos\Python\Proyectos\TallerPy\Logger\LOG_{datetime.datetime.now().strftime("%Y-%m-%d")}.txt'
print(f'Loggin to file: {log}')
check=os.makedirs(os.path.dirname(log),exist_ok=True)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler=logging.FileHandler(log)
file_handler.setFormatter(logging.Formatter('\n%(asctime)s - %(levelname)s - at line: %(lineno)d - %(message)s'))
stream_handler=logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('\n%(asctime)s - %(levelname)s - at line: %(lineno)d - %(message)s'))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug("Log de errores creado correctamente.")


#chrome_options = Options()
#chrome_options.add_argument("--headless")
#options.headless = True #para correr en segundo plano

#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install())

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
			logger.debug('Proximo proyecto')
		except:
			logger.debug('No se pudo reactivar la pagina')

def popupControl():
	#text = []
	#mensaje = ''
	TM.sleep(5)
	try:
		WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
		logger.debug('El Proyecto NO se encuentra Bloqueado, se sigue con el proceso')
		
	except: 
		logger.debug('Hay una Adevertencia y/o un Error...')
		try: #para Geenracion de HEA
			while(WebDriverWait(driver, 30).until_not(EC.text_to_be_present_in_element((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))):
				driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
				TM.sleep(1)
				logger.debug('Cierra popUp')
		except:
			pass
	
#WEB - INICIO
def sapAuto():
	#driver=webdriver.Chrome(ChromeDriverManager().install()) #Abre y/o instala webdriver
	driver.implicitly_wait(20) #Cuando algo no aparece, prueba cada 1 seg. durante 20 seg. 
	driver.delete_all_cookies()
	
	#WEB - LOGIN
	#logger.debug(" Iniciando navegador Web.")
	driver.get('https://proyectos.movistar.com.ar/sap/bc/ui2/flp#EnterpriseProject-searchWD?sap-ui-tech-hint=WDA')
	
	driver.maximize_window()
	logger.debug("First window title = " + driver.title)
	TM.sleep(4)
	try:
		#INPUT-USER # aut_rda  Python-23
		driver.find_element(By.ID,'USERNAME_FIELD-inner').send_keys('aut_rda') #ACA PONER USUARIO GENERAL peppel
		#INPUT-PASS
		driver.find_element(By.ID,'PASSWORD_FIELD-inner').send_keys('Python-23') #ACA PONER PASS GENERAL Unqui2022
		#BTN-ACEPTAR
		driver.find_element(By.XPATH,'//*[@id="LOGIN_LINK"]/span[1]').click()
		
		TM.sleep(10)
		#logger.debug("Espera lista, buscando...")
		logger.debug("Espera lista, buscando...")
		#ENTRAR A MARCO 1:
		frame1=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'application-EnterpriseProject-searchWD')))
		logger.debug("Frame1 encontrado ok.")
		#ENTRAR A MARCO 2:
		frame2=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@style,'display: block; width')]")))
		logger.debug("Frame2 encontrado ok.")
	except:
		logger.debug('NO SE PROCESO EL LOGUEO, SE TERMINA LA EJECUCION...')
		quit() #Si no se puede loguear termina la ejecucion
	
	#Tomamos los datos del Excel como una Lista  de dos dimensiones lista[][] y la convertimos en Strings.
	#PROCESAR EL EXCEL	
	dataExl = dataExcel.DataSource().xlData() # creamos el obj para leer los datos del Excel
	
	logger.debug(f'{dataExl}')
	logger.debug(f'Cantidad de Filas a procesar: {len(dataExl)}')
	
	#Iteracion para recorrer las filas del Excel desde la Fila 1
	for fila in range(1, len(dataExl)):
		#print(fila)
		#Se verifica si el Proyecto fue procesado o No
		estadoProyecto = str(dataExl[fila][6])
		if estadoProyecto == 'Procesado':
			logger.debug('Proyecto Procesado...Sigue con la proxima linea...')
			continue #Sigue con la proxima fila del Excel
		else:
			logger.debug('Proximo proyecto a procesar...')
			pass
		
		proyectoNum = str(dataExl[fila][0]) # fila=1 , Col=0 Tomamos el numero de Proyecto
		logger.debug(f'{proyectoNum,type(proyectoNum)}')
		
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
				logger.debug('Sin proyecto para procesar')
				causa.causa(coord[fila][6], 'No Existe ningún proyecto') # Pasamos la celda y la causa de la falla
				#validacion.writeXl(coord[fila][5],0) # pasamos la celda y Flag de "NO Procesado"
				continue # Sigue con la proxima Fila
					
			#BTN-Buscar
			driver.find_element(By.ID,"WDDD").click() #Click al Boton Buscar
			TM.sleep(1)
			driver.find_element(By.PARTIAL_LINK_TEXT,proyectoNum).click() # Click al proyecto
			
			#switch window in x seconds
			TM.sleep(15)
		except:
			logger.debug ('NO SE PROCESO EL NUMERO DE PROYECTO')
			logger.debug ('SEGUIR CON LA SIGUENTE FILA')
			#reactivacion()
			continue # Sigue con la proxima Fila
		
		# CONTROL DEL FRAME DEL PROYECTO
		try:
			flagIframe = 0
			#Activamos la pagina del proyecto (Segunda Windows Handles)
			driver.switch_to.window(driver.window_handles[1]) 
			logger.debug(f'{driver.window_handles}')
			
			#Esperamos que iframe este Activo
			busca_iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div/div/iframe')))
			logger.debug('iframe encontrado ok')
			driver.maximize_window()
			flagIframe = 1
			
			#CONTROL DEL POPUP
			#Se verifica si el proyecto NO esta bloqueado
			WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))
			logger.debug('El Proyecto NO se encuentra Bloqueado, se sigue con el proceso')
			
		except:
			
			if(flagIframe == 1): #Entra al if si no falla por Iframe
				logger.debug('HAY UN POPUP...')
				mensaje=''
				flagMsgAdv = '0'
				flagMsgEr = '0'
				
				#CAPTURAMOS LOS MENSAJES
				try:
					#Caputura mensaje de Adevertencia
					mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div/div/div/table/tbody/tr/td/div/div[2]/div[1]/div[4]').get_attribute('title')	
					logger.debug(f'Mensaje Adv: '+ mensaje)
					mensaje = mensaje.split()
					flagMsgAdv = int (mensaje[1]) # indica que hay un mensaje de Advertencia y el proyecto SI se puede porcesar
				except:
					logger.debug('No hay mensaje de Adevertencia')	
		
				try:	
					#Captura mensaje de Error
					mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div/div/div/table/tbody/tr/td/div/div[2]/div[1]/div[3]').get_attribute('title')	
					logger.debug(f'Mensaje de Error: '+ mensaje)
					mensaje = mensaje.split()
					flagMsgEr = int (mensaje[1]) # Indica que hay un mensaje de Error y el proyecto NO se puede precesar.
				except:
					logger.debug('No hay mensaje de Error')		
				#print(text, type(text))

				#PROCESAMOS LOS MENSAJES CAPTURADOS SEGUN EL TIPO DE MESAJE
				if (flagMsgAdv >= 1 and flagMsgEr == 0):# Si hay algun mensaje de advertencia lo cierra y sigue procesando el proyecto
					try:
						driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
						TM.sleep(1)
						logger.debug('Se cerro el mensaje de advertencia...Sigue procesando el proyecto')
						
					except:
						pass					

				elif(flagMsgEr >= 1):
					try:
						while(WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr/td[1]/span/span'), 'Sin mensajes          '))):#Verifica si esta el mensaje de proyecto bloqueado y cierra el popup
							driver.find_element(By.XPATH, '//*[@id="WDWL1-close"]').click() #Boton x del popup
							TM.sleep(1)
							logger.debug('Se cierra el mensaje de error...se debe continuar con el proximo proyecto')
					except:
						pass		
			else:
				logger.debug('FALLO EL MANEJO DEL IFRAME...')
			
			#Se interrumpe el procesamiento del proyecto en caso que falle por Iframe o el proyecto este Bloqueado.			
			if(flagMsgEr >= 1 or flagIframe == 0):
				try:#Cierro el proyecto del boton.
					WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					TM.sleep(1)
				except:
					pass
				validacion.writeXl(coord[fila][6],'No Procesado') # pasamos la celda y la validación
				causa.causa(coord[fila][7], 'Fallo el IFRAME o el Proyecto esta bloqueado') # Pasamos la celda y la causa de la falla
				TM.sleep(1)
				#reactivacion()#Reactivacion de la pagina		
				continue # Sigue con la proxima Fila	
					
				
		#ELECCION DE LA TAREA (Mediante el boton Buscar)
		try:
			actions = ActionChains(driver)
			TM.sleep(3)
			#Leo del Excel la tarea a procesar		
			tarea = dataExl[fila][1]
			logger.debug(f'Tarea: '+tarea)
			
			#print(driver.window_handles)
			
			#Click al menu Buscar
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/div/span[5]/span[2]').click()
			TM.sleep(3)
			logger.debug(f"Click al menu Buscar")

			#Click al menu desplegable
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[3]/td[1]/div/div/div/div/table/tbody/tr[2]/td[2]/span').click()
			TM.sleep(1)
			logger.debug(f"Click al menu desplegable")


			#Opcion "Tarea"
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[4]').click()
			TM.sleep(1)
			logger.debug(f"Click a la opcion tarea")
					
			#Campo Denominación, pego la tarea
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[4]/td[2]/span').click()
			TM.sleep(1)
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[4]/td[2]/span/input').send_keys(tarea)
			TM.sleep(1)
			actions.send_keys(Keys.ENTER).perform() #Enter
			logger.debug(f"Se pego la tarea elegida")
			
			#Click al menu Numero
			driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/div/div/table/tbody/tr[6]/td/div/div/table/tbody/tr[3]/td/div/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[1]/a').click()
			TM.sleep(2)
			logger.debug(f"Click al menu numero")
			
		except:
			logger.debug("Exception :NO SE PUDO PROCESAR LA TAREA")
			validacion.writeXl(coord[fila][6],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][7], 'No se pudo procesar la tarea') # Pasamos la celda y la causa de la falla
			TM.sleep(1)
			#Intentamos Cerrar el proyecto del boton
			try:
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				logger.debug(f"Se cerró desde el boton")
			except:
				driver.close()#Fuerza el cierre del proyecto
				logger.debug(f"Se forzó el cierre")
				
			#reactivacion()#Reactivacion de la pagina
			continue # Sigue con la proxima Fila										
			
		
		#PROCESAMIENTO DEL CAMPO		
		try:		
			campo = dataExl[fila][2]
			logger.debug(f'Campo: ' +campo)
			TM.sleep(0.5)
			accion = dataExl[fila][3]
			logger.debug(f'Accion: ' +accion)
			TM.sleep(0.5)
			#Caputura el texto y chequeo si el proyecto esta cerrado.
			mensaje = ''
			logger.debug(f'Estado del mensaje: '+mensaje)
			mensaje = driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input').get_attribute('value')	
			logger.debug(f'Estado de la Tarea: '+ mensaje)
			TM.sleep(1)
			if ('Liberado' not in mensaje):# Si el campo del Status es distinto de Liberado significa que esta procesado(Cancelado o Cerrado)
				causa.causa(coord[fila][7], 'El proyecto estaba cerrado o cancelado')
				validacion.writeXl(coord[fila][6],'Procesado')
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				logger.debug('Proyecto Cerrado, Cancelado no se procesa')
				continue
			elif ('Pendiente Predecesor' in mensaje):
				causa.causa(coord[fila][7], 'La tarea del proyecto esta Pendiente de Predecesor')
				validacion.writeXl(coord[fila][6],'No Procesado')
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
				logger.debug('Proyecto Pendiente Predecesor, no se procesa')
				continue
						
			match campo:
				case 'Modificar Status':
													
					#Click en Datos Basico
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[1]/div[1]').click()
					TM.sleep(1)
										
					#Click en Modificar Status
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[15]/td[2]/div/div/table/tbody/tr/td[1]/span/input').click()
					TM.sleep(1)
									
				case 'Fecha prevista Inicio':
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
														
				case 'Fecha prevista Inicio/Final':
					fecha = dataExl[fila][4]
					fechas = fecha.split('/') # Divide el Texto por /
					logger.debug(f'{fecha}')
					logger.debug(f'{fechas}')
					fechaInicio = fechas[0]
					fechaFin = fechas[1]
					logger.debug(f'{fechaInicio}')
					logger.debug(f'{fechaFin}')
					
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
				#case 'No procesar':
				#	pass
				case _:
					logger.debug('No existe el campo')
					validacion.writeXl(coord[fila][6],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
					causa.causa(coord[fila][7], 'No existe el Campo para procesar') # Pasamos la celda y la causa de la falla
					#Intentamos Cerrar el proyecto del boton
					try:
						WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
						
					except:
						driver.close()#Forzamos el cierre del proyecto
										
					#reactivacion()#Reactivacion de la pagina
					continue # Sigue con la proxima Fila	
		except:
			logger.debug('Exception :NO SE PROCESO EL CAMPO')
			validacion.writeXl(coord[fila][6],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][7], 'Exception: No se pudo procesar el campo') # Pasamos la celda y la causa de la falla
			#Intentamos Cerrar el proyecto del boton
			try:
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
					
			except:
				driver.close()#Forzamos el cierre del proyecto
				
			#reactivacion()#Reactivacion de la pagina	
			continue # Sigue con la proxima Fila					
			
		
		#ACCION A REALIZAR: depende deL CAMPO y la TAREA
		try:
			#Leo del excel la accion a realizar "para la tarea en curso"
			#accion = dataExl[fila][3]
			logger.debug(f'{accion}')
			match accion:
				case 'Cerrar':
					#Click a la opcion Cerrar , verificar antes si ya no esta cerrada.		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[3]').click()
					popupControl()
					#Espera que aparezca el texto value="Completado - Cerrado" en el atributo "value" del elemento
					WebDriverWait(driver, 600).until_not(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'), mensaje[1]))
					logger.debug('Acción: Cerrar, OK')
														
				case 'Cancelar':
					#Click a la opcion Cancelar		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[2]').click()
					popupControl()
					WebDriverWait(driver, 600).until(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'),mensaje[1]))						
					logger.debug('Acción: Cancelar, OK')
					
				case 'Anulación "Concluida"':
					#Click a la opcion Anulación "Concluida" 		
					driver.find_element(By.XPATH,'/html/body/table/tbody/tr/td/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[4]/div/div/div[2]').click()
					popupControl()
					WebDriverWait(driver, 600).until(EC.text_to_be_present_in_element_value((By.XPATH,'/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/table/tbody/tr/td/div/table/tbody/tr[3]/td/div[1]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[14]/td[2]/span/input'),mensaje[1]))
					logger.debug('Acción: Anulación "Concluida", OK')
								
				case 'Fecha':
					pass
				#case 'No procesar': #Si el Status esta en un estado distinto de Liberado significa que esta Procesado, luego resta grabar y cerrar.
				#	pass
				
				case _:
					logger.debug('NO EXISTE LA ACCIÓN')
					try:
						WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
						
					except:
						logger.debug('No se pudo cerrar el proyecto del botón')
						driver.close()#Forzamos el cierre del proyecto
						logger.debug('Se Forzo el cierre porque fallo la ACCIÓN')
						
		except:
			logger.debug('Exception : NO SE PROCESO LA ACCIÓN A REALIZAR')
			driver.close()#Forzamos el cierre del proyecto por si falla por tiempo excedido en el Case que corresponda,luego el proyecto queda bloqueado.
			validacion.writeXl(coord[fila][6],'No Procesado') # pasamos la celda y Flag de "NO Procesado"
			causa.causa(coord[fila][7], 'Hubo algun problema al procesar la acción') # Pasamos la celda y la causa de la falla
			#reactivacion()#Reactivacion de la pagina
			continue # Sigue con la proxima Fila	
			
		#GRABAR LOS CAMBIOS
		
		#CLICK AL BOTON GRABAR
		#WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div'))).click()
				
		try:#Click al Boton Grabar	
			#if(accion != 'No procesar' or campo != 'No procesar'):
			driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[1]/div').click()	
			TM.sleep(1)
						
			#Espera el mensaje de grabacion "Se han grabado los datos"
						
			WebDriverWait(driver, 300).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/div/div[3]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/span/span/span/span'), 'Se han grabado los datos'))
			logger.debug('Mensaje: Se han grabado los datos...')
			TM.sleep(1)

			#Cierra el popup  #/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[1]/table/tbody/tr/td[3]/a
			WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/div/div/div[2]/div[1]/div/div/div[1]/table/tbody/tr/td[3]/a'))).click()
			logger.debug('Popup cerrado')
			logger.debug('SE PUDIERON GRABAR LOS CAMBIOS...')
			TM.sleep(1)
			logger.debug('Se completo el proceso de Grabación...')

			#Cerramos el proyecto del boton
			WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			logger.debug('Se cerro el proyecto...')
			validacion.writeXl(coord[fila][6],'Procesado') 
			causa.causa(coord[fila][7], 'OK')
	
		except TimeoutException as ex:
			logger.debug("TimeOutException. " + str(ex))
			driver.close()
			logger.debug('Se Forzo el cierre, por TimeOutException')	
			TM.sleep(0.5)	
			validacion.writeXl(coord[fila][6],'No procesado') # pasamos la celda y Flag de "NO Procesado"
			TM.sleep(0.5)
			causa.causa(coord[fila][7], 'No se pudieron grabar los cambios - Tiempo de grabación excedido') # Pasamos la celda y la causa de la falla
		except:
			logger.debug('Except: FALLO LA GRABACION')
			try:#Intento cerrar del boton
				WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]/span[2]/div'))).click()
			except:
				driver.close()#Forzamos el cierre del proyecto
				logger.debug('Se Forzo el cierre...')
			
				validacion.writeXl(coord[fila][6],'No procesado') # pasamos la celda y Flag de "NO Procesado"
				TM.sleep(1)
				causa.causa(coord[fila][7], 'No se pudieron grabar los cambios') # Pasamos la celda y la causa de la falla
			#reactivacion()#Reactivacion de la pagina			
		

#EJECUCIÓN
#horaInicio=datetime.datetime.now()
if __name__ == '__main__':
	horaInicio=datetime.datetime.now()
	sapAuto()
	horaFin=datetime.datetime.now()
	duracion=str(horaFin-horaInicio)
	logger.debug(f'Fin de la Ejecucion --> Duración: '+duracion)
	




