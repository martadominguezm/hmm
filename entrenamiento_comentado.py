
import csv  
import numpy as np  
from pomegranate import *  # Para crear el modelo de Markov oculto
import matplotlib.pyplot as plt 

#### Añadido por mi ####
#from hmmlearn.hmm import HiddenMarkovModel


input1 = csv.reader(open('.\\datos\\marta\\data_processed\\model\\2-Nivel-13042023.csv','r'))
#input1 = csv.reader(open('datos/2-Nivel.csv','r'))

# Declarar algunas variables que se utilizarán más adelante
pathTrain = []  # Lista vacía donde se almacenará la secuencia de estados del modelo
nivel1Train = []  #estados del primer nivel
nivel2Train = []  #estados del segundo nivel
nivel3Train = []  #estados del tercer nivel
# nivel4Train = []  # Lista vacía donde se almacenarán los estados del cuarto nivel
nivel1Dic = {'': 0, None: 0}  # Diccionario que se utilizará para codificar los estados del primer nivel
nivel2Dic = {'': 0, None: 0}  # Diccionario que se utilizará para codificar los estados del segundo nivel
nivel3Dic = {'': 0, None: 0}  # Diccionario que se utilizará para codificar los estados del tercer nivel
# nivel4Dic = {'': 0, None: 0}  # Diccionario que se utilizará para codificar los estados del cuarto nivel
typesTrain = []  #almacenarán los tipos de eventos (PAGE o EVENT)
typesDic = {'PAGE': 0, 'EVENT': 1}  #codificar los tipos de eventos
lenTrain = []  #almacenarán las longitudes de las sesiones

nvis1 = []  #tiempos de inicio de cada página o evento
i=0  # Contador para llevar el registro de las filas del archivo que se están leyendo
tempId = 0  # Variable temporal que se utilizará para detectar el inicio de una nueva sesión

# Recorrer cada fila del archivo CSV que contiene los datos
for row in input1:
	# Ignorar la primera fila que contiene los nombres de las columnas
	if (i > 0):
		# Agregar el tiempo de inicio de la página o evento a la lista nvis1
		nvis1.append(row[1])

		# Si el tiempo desde el inicio de la página o evento es menor que 200 segundos
		if ((int(row[1])-int(nvis1[0])) < 200):
			# Si el tipo es PAGE
			if (row[6] == 'PAGE'):
				# Si la categoría nivel 1 no está en el diccionario nivel1Dic, agregarla
				if (row[8] not in nivel1Dic):
					nivel1Dic[row[8]] = len(nivel1Dic)-1		
				nivel1Train.append(nivel1Dic[row[8]])

				# Si la categoría nivel 2 no está en el diccionario nivel2Dic, agregarla
				if (row[9] not in nivel2Dic):
					nivel2Dic[row[9]] = len(nivel2Dic)-1	
				nivel2Train.append(nivel2Dic[row[9]])

				# Si la categoría nivel 3 no está en el diccionario nivel3Dic, agregarla
				if (row[10] not in nivel3Dic):
					nivel3Dic[row[10]] = len(nivel3Dic)-1		
				nivel3Train.append(nivel3Dic[row[10]])

				# # Si la categoría nivel 4 no está en el diccionario nivel4Dic, agregarla
				# if (row[11] not in nivel4Dic):
				# 	nivel4Dic[row[11]] = len(nivel4Dic)-1		
				# nivel4Train.append(nivel4Dic[row[11]])

			# Si el tipo es EVENT
			elif (row[6] == 'EVENT'):
				# Si la categoría nivel 1 no está en el diccionario nivel1Dic, agregarla
				if (row[12] not in nivel1Dic):
					nivel1Dic[row[12]] = len(nivel1Dic)-1		
				nivel1Train.append(nivel1Dic[row[12]])

				# Si la categoría nivel 2 no está en el diccionario nivel2Dic, agregarla
				if (row[13] not in nivel2Dic):
					nivel2Dic[row[13]] = len(nivel2Dic)-1		
				nivel2Train.append(nivel2Dic[row[13]])

				# Si la categoría nivel 3 no está en el diccionario nivel3Dic, agregarla
				if (row[14] not in nivel3Dic):
					nivel3Dic[row[14]] = len(nivel3Dic)-1		
				nivel3Train.append(nivel3Dic[row[14]])

				# # Si la categoría nivel 4 no está en el diccionario nivel4Dic, agregarla
				# if (row[15] not in nivel4Dic):
				# 	nivel4Dic[row[15]] = len(nivel4Dic)-1		
				# nivel4Train.append(nivel4Dic[row[15]])

			# Si es un tipo desconocido
			else:
				print('Nuevo tipo distinto')
				break

			## Si el ID temporal es diferente al actual, agregar la longitud a la lista lenTrain
			#Comprueba si el id de la fila actual es diferente al de la fila anterior
			if (tempId != row[0] ):
				# Actualiza el id temporal al de la fila actual
				tempId = row[0]
				# Agrega el número de eventos en la sesión actual a la lista lenTrain
				lenTrain.append(int(row[3]))
			
			#Agrega el tipo de evento actual a la lista typesTrain, usando el diccionario typesDic
			typesTrain.append(typesDic[row[6]])

	#llevar un registro del número de filas que se han procesado en el bucle
	i+=1


# Recorre cada elemento en la lista nivel1Train y agrega un '0' al principio si el número es de un solo dígito
# o convierte el número en una cadena si tiene más de un dígito.
for n, q in enumerate(nivel1Train):
	if len(str(q)) == 1:
		nivel1Train[n] = '0'+ str(nivel1Train[n])
	else:
		nivel1Train[n] = str(nivel1Train[n])

# Repite lo mismo para la lista nivel2Train.
for n, q in enumerate(nivel2Train):
	if len(str(q)) == 1:
		nivel2Train[n] = '0'+ str(nivel2Train[n])
	else:
		nivel2Train[n] = str(nivel2Train[n])

# Repite lo mismo para la lista nivel3Train, con la diferencia de que agrega dos '0' al principio si el número es de un solo dígito
# y un '0' al principio si el número tiene dos dígitos.
for n, q in enumerate(nivel3Train):
	if len(str(q)) == 1:
		nivel3Train[n] = '00'+ str(nivel3Train[n])
	elif len(str(q)) == 2:
		nivel3Train[n] = '0'+ str(nivel3Train[n])
	else:
		nivel3Train[n] = str(nivel3Train[n])

# Repite lo mismo para la lista nivel4Train, con la diferencia de que agrega tres '0' al principio si el número es de un solo dígito
# y dos '0' al principio si el número tiene dos dígitos.
""" for n, q in enumerate(nivel4Train):
	if len(str(q)) == 1:
		nivel4Train[n] = '00'+ str(nivel4Train[n])
	elif len(str(q)) == 2:
		nivel4Train[n] = '0'+ str(nivel4Train[n])
	else:
		nivel4Train[n] = str(nivel4Train[n]) """


# Crea una lista llamada pathTrain que contiene una cadena de texto que representa el camino seguido a través de los niveles de cada usuario.
# El camino se crea concatenando las cadenas de nivel1Train, nivel2Train, nivel3Train y nivel4Train correspondientes a cada elemento de la lista typesTrain.
# La cadena resultante se convierte a un número entero y se agrega a la lista pathTrain.
for n in range (len(nivel1Train)):
	nivel = str(typesTrain[n]) + nivel1Train[n] + nivel2Train[n] + nivel3Train[n] #+ nivel4Train[n]
	pathTrain.append(int(nivel))

# Crea un arreglo numpy a partir de la lista pathTrain.
seq = np.array([pathTrain])

# Crea una lista de tres probabilidades.
prob = [0.25, 0.5, 0.75]


""" Realiza un bucle anidado tres veces. En cada iteración, crea un modelo de HMM con diferentes parámetros (número de componentes ocultas,
inercia de bordes y inercia de distribución) utilizando el algoritmo Baum-Welch y ajusta el modelo a los datos de entrenamiento.
El modelo se guarda en la variable model. """

# Realiza un bucle que itera sobre los valores del 1 al 7 para el número de componentes ocultas del modelo de HMM.
for h in range (1,8):
	
	# Crea una lista de tres probabilidades, utilizadas para ajustar los parámetros de la inercia de bordes y la inercia de distribución en el modelo de HMM.
	# La lista de probabilidades se utiliza en los bucles anidados siguientes para ajustar estos parámetros.
	prob = [0.25, 0.5, 0.75]

	# Realiza un bucle anidado para ajustar la inercia de bordes en el modelo de HMM. 
	# La inercia de bordes se utiliza para ajustar la importancia relativa de la estructura del modelo existente versus la información proporcionada por los datos.
	for l in prob:
		
		# Realiza un bucle anidado para ajustar la inercia de distribución en el modelo de HMM.
		# La inercia de distribución se utiliza para ajustar la importancia relativa de los datos versus la información previa sobre los parámetros de distribución de probabilidad.
		for k in prob:
			
			# Crea un modelo de HMM utilizando la función from_samples de la biblioteca pomegranate. 
			# El modelo se ajusta a los datos de entrenamiento y se utiliza el algoritmo Baum-Welch.
			# Los parámetros para el número de componentes ocultas, la inercia de bordes y la inercia de distribución son proporcionados por los bucles anidados.
			model = HiddenMarkovModel.from_samples(NormalDistribution, n_components=h, X=seq, algorithm='baum-welch', edge_inertia=l, distribution_inertia=k)
			
			# Se "bake" el modelo, lo que significa que se realiza una inferencia de la estructura del modelo y se establecen las distribuciones de probabilidad de los estados.
			model.bake()

""" 
Este código ajusta un modelo de HMM a los datos de entrenamiento mediante el algoritmo Baum-Welch. 
El número de componentes ocultas, la inercia de bordes y la inercia de distribución se ajustan mediante bucles anidados. 
Se crean un total de 63 modelos (7 x 3 x 3) para todos los posibles valores de estos parámetros.
 """