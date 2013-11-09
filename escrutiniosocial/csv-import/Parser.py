import csv

# Carga de documento csv
fd = open('electoral-2013-departamentos.csv', mode='r')

reader = csv.reader(fd)
lista = []

# Se levanta la lista de keys
for rows in reader:
	lista.append(rows)
keys = lista[0]

# Se sacan las keys y se cargan los valores en diccionarios
lista.pop(0)
lista_final =[]
for elem in lista:
	dicc = {}
	for x in range(len(keys)):
		dicc[keys[x]]=elem[x]
	lista_final.append(dicc)
print lista_final
