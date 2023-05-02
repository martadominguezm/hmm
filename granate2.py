import csv
import numpy as np
from pomegranate import *
import matplotlib.pyplot as plt

### Importado por Marta ###
#from hmmlearn.hmm import HiddenMarkovModel
#from hmmlearn import hmm
#from sklearn import hmm

""" 
Este código procesa cinco archivos de entrada (input1, input2, input3, input4, input5) que contienen información de la actividad de usuarios en un sitio web 
y genera tres listas (pathTrain, pathTest, pathInt) y tres listas de enteros (lenTrain, lenTest, lenInt).

Primero, el código recorre cada fila del archivo input1 y agrega el valor de la columna 1 (visitNumber) a la lista nvis1. 
Si la diferencia entre el valor de nvis1 actual y el valor de nvis1 en la primera fila es menor a 200, 
el código determina si la fila corresponde a un evento de tipo "PAGE" o "EVENT", le asigna un número a la fila según el diccionario typesDic, 
y agrega el número a la lista pathTrain. Además, si el valor de la columna 0 (visitId) es distinto al de la fila anterior, agrega el valor de la columna 3 (hits) a la lista lenTrain. 
Por último, agrega el valor del diccionario typesDic correspondiente a la fila a la lista typesTrain.

Si la diferencia es mayor a 200, agrega el valor de la columna 7 (pagePath) o 9 (pagePathLevel2 ¿?¿?) (dependiendo del tipo de evento) a la lista pathTest 
y el valor del diccionario typesDic correspondiente a la fila a la lista typesTest. Si el valor de la columna 0 es distinto al de la fila anterior, 
agrega el valor de la columna 3 (hits) a la lista lenTest.

El código repite este proceso con los archivos input2, input3, input4 e input5, pero en lugar de agregar los valores a las listas pathTrain, 
lenTrain y typesTrain, los agrega a las listas pathInt, lenInt y typesInt.

La variable nvis1 se utiliza para almacenar el valor de la columna 1 (visitNumber) de la fila actual, 
que se utiliza para calcular la diferencia con el valor de la columna 1 de la primera fila. 
La variable tempId se utiliza para almacenar el valor de la columna 0 (visitId) de la fila anterior, 
que se utiliza para determinar si el valor de la columna 0 es distinto al de la fila anterior (si es un nuevo usuario?¿?¿ en la web). deberia ser visita¿?¿?¿?
La variable i se utiliza para llevar la cuenta de las filas procesadas y se inicializa en 0 al principio de cada ciclo. 
Al final de cada ciclo, se limpia la lista nvis1. """


input1 = csv.reader(open('datos/marta/data_processed/model/Nivel-user_1qyqHPsqRSUGTHWysepdiRUfcED3.csv','r'))
input2 = csv.reader(open('datos/marta/data_processed/model/Nivel-user_dxqKsJ9Xl7SC5tHV8j1yW41KR7S2.csv','r'))
input3 = csv.reader(open('datos/marta/data_processed/model/Nivel-user_MGTOG86ByNRVU9ZjGpXPPz6GXu33.csv','r'))
""" input4 = csv.reader(open('.\\datos\\marta\\data_processed\\model\\4-Nivel-13042023.csv','r'))
input5 = csv.reader(open('.\\datos\\marta\\data_processed\\model\\5-Nivel-13042023.csv','r')) """

# Se inicializan listas y diccionarios vacíos que se usarán más adelante
pathTrain = []
pathTest = []
pathInt = []
pathDic = {}
typesTrain = []
typesTest = []
typesInt = []
typesDic = {'PAGE': 0, 'EVENT': 1}
lenTrain = []
lenTest = []
lenInt = []

nvis1 = [] # Se inicializa una lista vacía para almacenar valores de nvis1
i=0 # Se inicializa la variable i en 0
tempId = 0 # Se inicializa la variable tempId en 0

# Se recorre cada fila del archivo input1
for row in input1:
	if (i > 0):
		nvis1.append(row[1]) # Se agrega el valor de la columna 1 (nvis1) a la lista nvis1

		# Si la diferencia entre el valor de nvis1 actual y el valor de nvis1 en la primera fila es menor a 200,
		# se determina si la fila corresponde a un evento de tipo "PAGE" o "EVENT", se asigna un número a la fila según el
		# diccionario typesDic y se agrega el número a la lista pathTrain. Además, si el valor de la columna 0 (id) es distinto al de la fila anterior,
		# se agrega el valor de la columna 3 (len) a la lista lenTrain.
		if ((int(row[1])-int(nvis1[0])) < 200):
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathTrain.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathTrain.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenTrain.append(int(row[3]))

			typesTrain.append(typesDic[row[6]])

		else:
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathTest.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathTest.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenTest.append(int(row[3]))

			typesTest.append(typesDic[row[6]])

	i+=1

nvis1.clear()
i=0
tempId = 0

for row in input2:
	if (i > 0):
		nvis1.append(row[1])

		if ((int(row[1])-int(nvis1[0])) < 50):
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathInt.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathInt.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenInt.append(int(row[3]))

			typesInt.append(typesDic[row[6]])

		else:
			break
	i+=1

nvis1.clear()
i=0
tempId = 0

for row in input3:
	if (i > 0):
		nvis1.append(row[1])

		if ((int(row[1])-int(nvis1[0])) < 50):
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathInt.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathInt.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenInt.append(int(row[3]))

			typesInt.append(typesDic[row[6]])

		else:
			break

	i+=1

nvis1.clear()
i=0
tempId = 0

""" for row in input4:
	if (i > 0):
		nvis1.append(row[1])

		if ((int(row[1])-int(nvis1[0])) < 50):
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathInt.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathInt.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenInt.append(int(row[3]))

			typesInt.append(typesDic[row[6]])

		else:
			break

	i+=1

nvis1.clear()
i=0
tempId = 0

for row in input5:
	if (i > 0):
		nvis1.append(row[1])

		if ((int(row[1])-int(nvis1[0])) < 50):
			if (row[6] == 'PAGE'):
				if (row[7] not in pathDic):
					pathDic[row[7]] = len(pathDic)		
				pathInt.append(pathDic[row[7]])
			elif (row[6] == 'EVENT'):
				if (row[9] not in pathDic):
					pathDic[row[9]] = len(pathDic)		
				pathInt.append(pathDic[row[9]])
			else:
				print('Nuevo tipo distinto')
				break

			if (tempId != row[0] ):
				tempId = row[0]
				lenInt.append(int(row[3]))

			typesInt.append(typesDic[row[6]])

		else:
			break

	i+=1 """

print("lenTrain:",lenTrain) #lista con los hits de cada sesion csvNIVEL1
print("lenTest:",lenTest) #lista con los hits de cada sesion csvNIVEL1

print("typesTrain:",typesTrain) #Ahora mismo son todo 0s porque solo hay PAGE, no tenemos ningún EVENT
print("pathTrain:",pathTrain)



""" Este código entrena un modelo de Hidden Markov Model (HMM) usando el algoritmo Baum-Welch para un conjunto de datos de entrenamiento, 
y luego lo utiliza para calcular las probabilidades de las secuencias de datos en los conjuntos de entrenamiento, prueba e intrusos.

Primero, se crea una matriz de numpy seq que contiene los tipos y caminos de los datos de entrenamiento. 
Luego, se definen tres valores de probabilidad (prob) que se utilizan en los siguientes bucles for para iterar sobre diferentes valores de h, l y k.

Dentro del bucle for externo, se crea un modelo de HMM con el algoritmo Baum-Welch y se ajustan los valores de los parámetros n_components, 
edge_inertia y distribution_inertia. Luego, se "hornear" el modelo para que pueda ser usado para calcular las probabilidades de las secuencias de datos.

A continuación, se inicializan contadores y listas vacías para almacenar las puntuaciones de entrenamiento, prueba e intrusos. 
Los conjuntos de datos de entrenamiento, prueba e intrusos se recorren en bucles for, y para cada secuencia de datos, 
se calcula la puntuación de log-probabilidad usando el método log_probability del modelo y se agrega a la lista correspondiente.

Por último, se calcula la longitud de los tres conjuntos de datos (scores_Train, scores_Test y scores_Int) para poder 
graficarlos posteriormente usando la librería Matplotlib. 
Cada iteración de los bucles for externos produce una gráfica con los tres conjuntos de datos superpuestos, 
y la gráfica se guarda en un archivo PNG con un nombre específico que refleja los valores de h, l y k. """

seq = np.array((typesTrain,pathTrain)) #tipos y caminos de los datos de entrenamiento
print("seq: np.array((typesTrain,pathTrain))",seq)

# Definir una lista llamada `prob` con tres valores: 0.25, 0.5 y 0.75
prob = [0.25, 0.5, 0.75]

# Iterar sobre un rango de valores de 1 a 17 con la variable `h`
for h in range (1,18):
	# Iterar sobre cada valor en la lista `prob` con la variable `l`
	for l in prob:
        # Iterar sobre cada valor en la lista `prob` con la variable `k`
		for k in prob:

            # Crear un modelo de Hidden Markov Model (HMM) usando el algoritmo Baum-Welch
            # `n_components` se refiere al número de estados ocultos del modelo, en este caso se usa el valor de `h`
            # `X` se refiere al conjunto de observaciones, en este caso se usa el arreglo `seq`
            # `edge_inertia` se refiere al valor de inercia de los bordes
            # `distribution_inertia` se refiere al valor de inercia de la distribución
            
			#model = HiddenMarkovModel.from_samples(DiscreteDistribution, n_components=5, X=seq)
			model = HiddenMarkovModel.from_samples(NormalDistribution, n_components=h, X=seq, algorithm='baum-welch', edge_inertia=l, distribution_inertia=k)
			model.bake() # "hornear" el modelo para que pueda ser usado para calcular las probabilidades de las secuencias de datos

			#print(model.viterbi(np.array((types[0:3926],path[0:3926]))))
			# Inicializar un contador y una lista vacía para almacenar las puntuaciones de entrenamiento
			counterTrain = 0
			scores_Train = []

			# se recorre el conjunto de datos de entrenamiento
			for x in lenTrain:
				
                # Si el valor es mayor que 1, calcular la puntuación de log-probabilidad para la secuencia de datos
                # correspondiente usando el método `log_probability` del modelo y agregar la puntuación a la lista `scores_Train`
				if (int(x) > 1):
					scoreTrain = model.log_probability(np.array((typesTrain[counterTrain:counterTrain+x-1],pathTrain[counterTrain:counterTrain+x-1])))
					scores_Train.append(scoreTrain)
				counterTrain += x

            # Inicializar un contador y una lista vacía para almacenar las puntuaciones de prueba
			counterTest = 0
			scores_Test = []

			# se recorre el conjunto de datos de prueba
			for x in lenTest:
				
                # Si el valor es mayor que 1, calcular la puntuación de log-probabilidad para la secuencia de datos
                # correspondiente usando el método `log_probability` del modelo y agregar la puntuación a la lista `scores_Test`
				if (int(x) > 1):
					scoreTest = model.log_probability(np.array((typesTest[counterTest:counterTest+x-1],pathTest[counterTest:counterTest+x-1])))
					scores_Test.append(scoreTest)
				counterTest += x

			counterInt = 0
			scores_Int = []

			# se recorre el conjunto de datos de intrusos (lenInt) para obtener la puntuación de probabilidad de cada secuencia en el modelo de Markov oculto (HMM) entrenado
			for x in lenInt:
				# si la longitud de la secuencia es mayor a 1, se calcula la puntuación de probabilidad para la secuencia y se agrega a la lista de puntuaciones de intrusos (scores_Int)
				if (int(x) > 1):
					scoreInt = model.log_probability(np.array((typesInt[counterInt:counterInt+x-1],pathInt[counterInt:counterInt+x-1])))
					scores_Int.append(scoreInt)
				counterInt += x
			
			# se calcula la longitud de los tres conjuntos de datos (scores_Train, scores_Test y scores_Int) para poder graficarlos más adelante
			length_train = len(scores_Train)
			length_val = len(scores_Test) + length_train
			length_int = len(scores_Int) + length_val

			

			# crear un gráfico de dispersión que muestra los resultados de las puntuaciones de log-probabilidad del modelo para cada conjunto de datos (entrenamiento, prueba original y prueba de intruso)
			plt.figure(figsize=(9,7))
			plt.scatter(np.arange(length_train), scores_Train, c='b', label='trainset')
			plt.scatter(np.arange(length_train, length_val), scores_Test, c='r', label='testset - original')
			plt.scatter(np.arange(length_val, length_int), scores_Int, c='g', label='testset - intruso')
			plt.title(label="N comp: "+str(h)+" Edge:"+str(l)+" Distribution:"+str(k))
			plt.savefig("MARTA_imgpomeConInercia_comp"+str(h)+"_edge"+str(l)+"Dist"+str(k)+".png")
			plt.close()

plt.show()
print(model.log_probability(np.array((typesTest,pathTest))))


