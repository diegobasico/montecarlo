from tkinter.filedialog import askopenfilename

path = 'indices_unificados/áreas_geográficas.txt'

regiones_por_area = []

with open(path, 'r+') as file:
    lines = file.readlines()
    for line in lines:
        área = line.split(sep=':')[0].strip()[-1]
        regiones = line.split(sep=':')[1].split(sep=',')
        for región in regiones:       
            row = área, región.strip()
            regiones_por_area.append(row)

print(regiones_por_area)