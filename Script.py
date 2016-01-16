# Universidad Central de Venezuela
# Jefferson Santiago, 22.540.515
# Mineria de Datos. Tarea 1

import csv as csv 
import numpy as np
import os
import re

os.getcwd() # obtener dir

csv_file_object = csv.reader(open('data.csv', 'rb')) 
header = csv_file_object.next()  # comando para quitar la primera columna

data=[]                          # Create a variable called 'data'.
age =[]                          # Arreglo para guardar las edades.
date = []                        # Arreglo para almacenar la fecha de nacimiento.
average = []                     # Arreglo para almacenar el promedio ponderado.
efficiency = []                  # Arreglo para almacenar la eficiencia.
teg = []
entry_mode = [] 
period = []                      # Arreglo para almacenar el período 
monthly_income = []              # Arreglo para almacenar el ingreso mensual   
other_income = []                # Arreglo para almacenar otros ingresos del responsable económico            
civil_state = []
sex = []
school = []
semester = []
for row in csv_file_object:      # Run through each row in the csv file,
    data.append(row[1:])             # Agregamos toda la fila en el arreglo menos la primera columna
    age.append(row[4])               #Guardamos en "age" tods los registros de las edades.
    date.append(row[3])              #Guardamos en "date" todos los registros de la fecha de nacimiento
    average.append(row[17])            # Guardamos en "average" el Promedio ponderado aprobado
    efficiency.append(row[18])
    teg.append(row[21])               # Guardamos si la persona realiza trabajo especial de grado.
    entry_mode.append(row[9])
    period.append(row[1])
    monthly_income.append(row[51])
    other_income.append(row[52])
    civil_state.append(row[5])
    sex.append(row[6])
    school.append(row[7])
    semester.append(row[10])
data = np.array(data) 	         # Then convert from a list to an array

# SIGUIENTE PASO, ESTANDARIZAR LA EDAD A SOLO NUMEROS

age2=[]                             # Arreglo para almacenar las edades sin la palabra AÑO
for row in age:                       # Recorremos el arreglo age
    age2.append(row[0:2])               # separamos los primeros 2 caracteres de cada registro
age2 = np.array(age2)                   # convertimos a arreglo a age2

data [0::,3] = age2                 #En este punto ya se tienen los años de manera numérica
#data [0::,3]

#SIGUIENTE PASO, ESTANDARIZAR LA FECHA DE NACIMIENTO

date2 = []                           # Arreglo para almacenar date de manera formateada
for row in date:
    if "/" in row:                   # Verificamos si el caracter "/" se encuentra en "row"
        rowSplit = row.split("/")    # Separamos la columna por "/" y almacenamos en un arreglo "rowSplit"
        if len(rowSplit[2]) == 2:    # Verificamos si en la posicion "2" de rowSplit hay es de tamaño 2.
            date2.append(rowSplit[0]+"/"+rowSplit[1]+"/"+"19"+rowSplit[2]) # Si es de tamaño 2 se concatena al año un "19" como prefijo
            continue                                                       # y se integra en el arreglo date2. Si llega al "continue" sigue el bucle "for"
        else:
            if len(rowSplit[1]) == 1:                                        # Las siguientes 3 lineas son con el fin de ESTANDARIZAR los años que tengan los meses con un solo digito
                rowSplit[1] = "0"+rowSplit[1]                                # Se hace sólo en este caso por el dataSet que nos dan y no se pide una solucion genérica 
                date2.append(rowSplit[0]+"/"+rowSplit[1]+"/"+rowSplit[2])
                continue
            date2.append(row)        # Si no, se integra al arreglo date2
            continue
    if "-" in row:                  # Verificamos si el caracter "-" se encuentra en "row"
        rowSplit = row.split("-")
        if len(rowSplit[2]) == 2:
            date2.append(rowSplit[0]+"/"+rowSplit[1]+"/"+"19"+rowSplit[2])
            continue
        else:
            date2.append(row.replace("-","/"))
            continue
    if " " in row:                  # Verificamos si el caracter " " se encuentra en "row"
        rowSplit = row.split(" ")
        if len(rowSplit[2]) == 4:
            date2.append(row.replace(" ","/"))
            continue
        else:
            date2.append(rowSplit[0]+"/"+rowSplit[1]+"/"+"19"+rowSplit[2])
            continue
    if " " not in row and "/" not in row and "-" not in row:              # Las sentencias siguientes son para ESTANDARIZAR las fechas que tienen solo numeros,
        if len(row) == 7:                                               # aunque se tendrán que remover todo el registro de algunas por que no tienen sentido.
            row = "0"+row
        anio = row[4:8]
        mes = row[2:4]
        dia = row[0:2]
        date2.append(dia+"/"+mes+"/"+anio)
        continue
date2 = np.array(date2)
data [0::,2] = date2

# SIGUIENTE PASO, ESTANDARIZAR PROMEDIO PONDERADO
average2=[]                            # Arreglo para guardar el promedio ponderado de manera estructurada
for row in average:                      
    if "." in row:
        average2.append(row)
    else:
        if len(row) == 2:
            average2.append(row)
        else:
            average2.append(row[0:2]+"."+row[2:len(row)]) # Separamos los 2 primeros caracteres, concatenamos un punto y luego el resto de caracteres
average2 = np.array(average2)                   # convertimos a arreglo a average2

data [0::,16] = average2               

# SIGUIENTE PASO, ESTANDARIZAR LA EFICIENCIA
efficiency2 = []
for row in efficiency:
    if row == "1":
        efficiency2.append(row)
        continue
    if "0." in row:
        efficiency2.append(row)
    else:
        efficiency2.append("0."+row)
efficiency2 = np.array(efficiency2)

data[0::,17] = efficiency2

# SIGUIENTE PASO, ESTANDARIZAR LA COLUMNA  QUE DICE SI ESTA REALIZANDO TESIS UNIENDO LA SIGUIENTE QUE
# ESPECIFICA SI ES PRIMERA VEZ QUE HACE TESIS, EN CASO AFIRMATIVO. EN CASO NEGATIVO SE COLOCA CERO
# para la primera vez 1, segunda 2 y mas de 2, 3.
teg2 = []
aux = 0
for row in teg:
    aux += 1
    if "S" in row:
        if len(data[aux-1,21]) == 0:              # dice que hace tesis pero no coloca si es por primera vez o mas
            teg2.append("0")
            continue
        if 'Pri' in data[aux-1,21]:
            teg2.append('1')
            continue
        if 'Seg' in data[aux-1,21]:
            teg2.append('2')
            continue
        if 'de' in data[aux-1,21]:
            teg2.append('3')
            continue
    else:
        if len(data[aux-1,21]) > 0:               # Si dice que no hace tesis pero dice que es primera vez o mas. asumo que se equivoca 
            if 'Pri' in data[aux-1,21]:
                teg2.append('1')
                continue
            if 'Seg' in data[aux-1,21]:
                teg2.append('2')
                continue
            if 'de' in data[aux-1,21]:
                teg2.append('3')
                continue            
            teg2.append(data[aux-1,21])           # al colocar No y tomo como que colocó si        
        else:
            teg2.append("0")
teg2 = np.array(teg2)
data[0::,20] = teg2

# SIGUIENTE PASO. SE REALIZARÁ UNA TRANSFORMACION DE NUMERACION 1-de-1 A
# LOS DATOS DE LA COLUMNA MODALIDAD DE INGRESO DONDE:
# EL VALOR "0" SE REFERIRÁ A LOS INGRESADOS POR OPSU, EL VALOR "1" A LOS INGRESADOS POR PRUEBA INTERNA
# EL VALOR "2" A LOS INGRESADOS POR CONVENIOS INTERNOS
entry_mode2 = []
for row in entry_mode:
    if "OPSU" in row:
        entry_mode2.append("0")
    else:
        if "Prueba" in row:
            entry_mode2.append("1")
        else:
            if "Convenios" in row:
                entry_mode2.append("2")
entry_mode2 = np.array(entry_mode2)
data[0::,8] = entry_mode2

# SIGUIENTE PASO, ESTANDARIZAR EL PERIODO ACADEMICO
period2 = []
#period3 = []

for row in period:
    m = re.search('[I]{1,2}-[2][0][0-99]{2}',row)
    if m and 'PRI' not in row:
        period2.append(row)
        continue
    if 'Pri' in row or 'PRI' in row or 'pri' in row:
        if (row[len(row)-4:len(row)]).isdigit():
            period2.append('I-'+row[len(row)-4:len(row)])
            continue
        else:
            if '2014' in row:
                period2.append(row)
                continue
            else:
                period2.append('I-2015')
                continue        
    if '2015-1' in row or row == '2015' or '2015-01' in row or '2015-s1' in row or 'I- 2015' in row or '1- periodo 2015' in row:
        period2.append('I-2015')
        continue
    if row == '2014':
        period2.append('I-2014')
        continue        
    if 'Seg' in row or 'SEG' in row or 'seg' in row:
        if (row[len(row)-4:len(row)]).isdigit():
            period2.append('II-'+row[len(row)-4:len(row)])
            continue
        else:
            if (row[len(row)-2:len(row)]).isdigit():
                period2.append('II-2014')
                continue
    if '2015-2' in row or '2015-02' in row or '30-03-15' in row:
        period2.append('II-2015')
        continue
    if '2014-II' in row or '2014-2' in row or '2014-02' in row or 'II- 2014' in row or '2014_2015' in row or 'sec-14' in row or '2014 II' in row:
        period2.append('II-2014')
        continue    
    period2.append('?')
period2 = np.array(period2)
data[0::,0] = period2

# SIGUIENTE PASO, ESTANDARIZAR EL INGRESO MENSUAL DEL RESPONSABLE ECONOMICO
monthly_income2 = []
for row in monthly_income:
    if not row.isdigit():
        if 'bs' in row:
            rowSinBs = row[0:len(row)-2]                        #Quitamos los bs
            if ' ' in rowSinBs:
                rowSinBs = rowSinBs[0:len(rowSinBs)-1]        # Para quitarle el esppacio
            if '.' in rowSinBs:
                rowSplit = rowSinBs.split('.')                  # Para quitar un punto que tiene un valor dado
                rowSinBs = rowSplit[0]+rowSplit[1] 
            monthly_income2.append(rowSinBs)   
            continue
        
        if ' ' in row:                                         # Caso para los numeros que tienen espacios despues del punto
            rowSplit = row.split(' ')
            rowSplit = rowSplit[0]+rowSplit[1]
            rowSplit = rowSplit.split(',')
            rowSplit = rowSplit[0]+'.'+rowSplit[1]
            monthly_income2.append(rowSplit)
            continue

        if row.find('.') == len(row)-3 or row.find('.') == len(row)-2:
            rowSplit = row.split(',')
            if len(rowSplit) == 1:
                monthly_income2.append(rowSplit[0])
                continue
            if len(rowSplit) == 2:
                monthly_income2.append(rowSplit[0]+rowSplit[1])
                continue
            
        if len(row.split(',')) == 3:
                rowSplit = row.split(',')
                monthly_income2.append(rowSplit[0]+rowSplit[1]+'.'+rowSplit[2])
                continue
    monthly_income2.append(row)
            
monthly_income2 = np.array(monthly_income2)
data[0::,50] = monthly_income2

# SIGUIENTE PASO, ESTANDARIZAR OTROS INGRESOS DEL RESPONSABLE ECONOMICO
other_income2 = []
for row in other_income:
    if row == '' or row == 'No':
        other_income2.append('0')
        continue
    if 'bs' in row:
        other_income2.append(row[0:len(row)-2])
        continue
    other_income2.append(row)

other_income2 = np.array(other_income2)
data[0::,51] = other_income2

# SIGUIENTE PASO, ESTANDARIZAR ESTADO CIVIL
# Se ESTANDARIZARá la columna de estado civil de la siguiente manera
# el valor '0' para Soltero, el valor '1' para casado, el valor '2' para Unido, el valor '3' para Viudo
civil_state2 = []
for row in civil_state:
    if 'Soltero' in row:
        civil_state2.append('0')
        continue
    if 'Casado' in row:
        civil_state2.append('1')
        continue
    if 'Unido' in row:
        civil_state2.append('2')
        continue
    if 'Viudo' in row:
        civil_state2.append('3')
        continue
civil_state2 = np.array(civil_state2)
data[0::,4] = civil_state2

# SIGUIENTE PASO, ESTANDARIZAR SEXO
# Se ESTANDARIZARá la columna de sexo de la siguiente manera
# el valor '0' para Masculino, el valor '1' para Femenino
sex2 = []
for row in sex:
    if 'Femenino' in row:
        sex2.append('1')
        continue
    if 'Masculino' in row:
        sex2.append('0')
        continue
sex2 = np.array(sex2)
data[0::,5] = sex2

# SIGUIENTE PASO, ESTANDARIZAR ESCUELA
# Se ESTANDARIZARá la columna de escuela de la siguiente manera
# el valor '0' para Bioanálisis, el valor '1' para Femenino
school2 = []
for row in school:
    if 'Bioa' in row:
        school2.append('1')
        continue
    if 'Enfer' in row:
        school2.append('0')
        continue
school2 = np.array(school2)
data[0::,6] = school2

# SIGUIENTE PASO, ESTANDARIZAR SEMESTRE QUE CURSA
# Se ESTANDARIZARá la columna de semestre que cursa de la siguiente manera
# Se toma el primer valor del string. si es un 1, se toma el segundo y si el segundo es un numero se coloca '10'
semester2 = []
for row in semester:
    if row[0:1] != '1':
        semester2.append(row[0:1])
        continue
    else:
        if row[1:2] == '0':
            semester2.append('10')
            continue
        semester2.append('1')
semester2 = np.array(semester2)
data[0::,9] = semester2

# SIGUIENTE PASO, ESTANDARIZAR LA COLUMNA "HA CAMBIADO USTED DE DIREECION"
# Se ESTANDARIZARá la columna de la siguiente manera:
# de ser afirmativo se inserta el valor de la columna donde se indica el motivo
change_adress = []
aux = 0
for row in data[0::,10]:
    aux += 1
    if row == 'Si':
        change_adress.append(data[aux-1,11])
        continue
    else:
        change_adress.append('0')
change_adress = np.array(change_adress)
data[0::,10] = change_adress

# SIGUIENTE PASO, UNIR LAS COLUMNAS AB(26) y AS(43) solo valores aceptables y si es 
# habitacion alquilada o residencia estudiantil
tipo = data[0::,25]
#renta1 = data[0::,26]
#renta2 = data[0::,43]
tipo2 = []
aux = 0
for row in tipo:
    aux += 1
    if 'alquilada' in row or 'Residencia' in row:
        if data[aux-1,26].isdigit():
            tipo2.append(data[aux-1,26])
            continue
        if data[aux-1,43].isdigit():
            tipo2.append(data[aux-1,43])
            continue
    tipo2.append('0')
tipo2 = np.array(tipo2)
data[0::,26] = tipo2

#SIGUIENTE PASO, UNIR FILAS AE CON AF. EN CASO DE SER 'SI' EN LA COLUMNA AE, SUSTITUIRLA POR EL VALOR DE AF

benefit = data[0::,29]
benefit2 = []
aux = 0
for row in benefit:
    aux += 1
    if 'S' in row:
        benefit2.append(data[aux-1,30])
        continue
    benefit2.append('0')
benefit2 = np.array(benefit2)
data[0::,29] = benefit2   

#SIGUIENTE PASO, UNIR FILAS AG CON AH. EN CASO DE SER 'SI' EN LA COLUMNA AG, SUSTITUIRLA POR EL VALOR DE AH

activity_income = data[0::,31]
activity_income2 = []

aux = 0
for row in activity_income:
    aux += 1
    if 'S' in row:
        activity_income2.append(data[aux-1,32])
        continue
    activity_income2.append('0')
activity_income2 = np.array(activity_income2)
data[0::,31] = activity_income2

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA APORTE MENSUAL DEL RESPONSABLE ECONOMICO A '0'

monthly_contribution = data[0::,34]
monthly_contribution2 = []

for row in monthly_contribution:
    if 'NA' in row:
        monthly_contribution2.append('0')
    else:
        monthly_contribution2.append(row)
monthly_contribution2 = np.array(monthly_contribution2)
data[0::,34] = monthly_contribution2 
        
# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA APORTE MENSUAL DE familiares A '0'

monthly_contribution_family = data[0::,35]
monthly_contribution_family2 = []

for row in monthly_contribution_family:
    if 'NA' in row:
        monthly_contribution_family2.append('0')
    else:
        monthly_contribution_family2.append(row)
monthly_contribution_family2 = np.array(monthly_contribution_family2)
data[0::,35] = monthly_contribution_family2 

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA APORTE MENSUAL POR ACTIVIDADES A '0'

monthly_contribution_activities = data[0::,36]
monthly_contribution_activities2 = []

for row in monthly_contribution_activities:
    if 'NA' in row:
        monthly_contribution_activities2.append('0')
    else:
        monthly_contribution_activities2.append(row)
monthly_contribution_activities2 = np.array(monthly_contribution_activities2)
data[0::,36] = monthly_contribution_activities2 

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA ALIMENTACIÓN A '0'

feeding = data[0::,38]
feeding2 = []

for row in feeding:
    if 'NA' in row:
        feeding2.append('0')
    else:
        feeding2.append(row)
feeding2 = np.array(feeding2)
data[0::,38] = feeding2 

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA TRANSPORTE PUBLICO A '0'

public_transport = data[0::,39]
public_transport2 = []

for row in public_transport:
    if 'NA' in row:
        public_transport2.append('0')
    else:
        public_transport2.append(row)
public_transport2 = np.array(public_transport2)
data[0::,39] = public_transport2 

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA GASTOS MEDICOS A '0'

medical_expenses = data[0::,40]
medical_expenses2 = []

for row in medical_expenses:
    if 'NA' in row:
        medical_expenses2.append('0')
    else:
        medical_expenses2.append(row)
medical_expenses2 = np.array(medical_expenses2)
data[0::,40] = medical_expenses2 

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA GASTOS ODONTOLOGICOS A '0'

dental_expenses = data[0::,41]
dental_expenses2 = []

for row in dental_expenses:
    if 'NA' in row:
        dental_expenses2.append('0')
    else:
        dental_expenses2.append(row)
dental_expenses2 = np.array(dental_expenses2)
data[0::,41] = dental_expenses2

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA GASTOS ODONTOLOGICOS A '0'

personal_expenses = data[0::,42]
personal_expenses2 = []

for row in personal_expenses:
    if 'NA' in row:
        personal_expenses2.append('0')
    else:
        personal_expenses2.append(row)
personal_expenses2 = np.array(personal_expenses2)
data[0::,42] = personal_expenses2

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA GASTOS DE MATERIALES DE ESTUDIO A '0'

study_materials_expenses = data[0::,44]
study_materials_expenses2 = []

for row in study_materials_expenses:
    if 'NA' in row:
        study_materials_expenses2.append('0')
    else:
        study_materials_expenses2.append(row)
study_materials_expenses2 = np.array(study_materials_expenses2)
data[0::,44] = study_materials_expenses2

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA GASTOS DE RECREACION A '0'

recreation_expenses = data[0::,45]
recreation_expenses2 = []

for row in recreation_expenses:
    if 'NA' in row:
        recreation_expenses2.append('0')
    else:
        recreation_expenses2.append(row)
recreation_expenses2 = np.array(recreation_expenses2)
data[0::,45] = recreation_expenses2

# SIGUIENTE PASO, CAMBIAR LOS NA DE LA COLUMNA OTROS GASTOS A '0'

other_expenses = data[0::,46]
other_expenses2 = []

for row in other_expenses:
    if 'NA' in row:
        other_expenses2.append('0')
    else:
        other_expenses2.append(row)
other_expenses2 = np.array(other_expenses2)
data[0::,46] = other_expenses2


# SIGUIENTE PASO, FORMATEAR LOS GASTOS POR VIVIENDA

living_place_expenses = data[0::, 53]
living_place_expenses2 = []
for row in living_place_expenses:
    if row.isdigit() or row == '':
        if row == '':
            living_place_expenses2.append('0')
            continue
        living_place_expenses2.append(row)
        continue
    if ', ' in row:
        living_place_expenses2.append(row.replace(', ','.'))
        continue
    if 'como' in row:
        living_place_expenses2.append('0')
living_place_expenses2 = np.array(living_place_expenses2)
data[0::,53] = living_place_expenses2
        
# SIGUIENTE PASO, ESTANDARIZAR GASTOS POR ALIMENTACIÓN

feeding_expenses = data[0::,54]
feeding_expenses2 = []
for row in feeding_expenses:
    if row.isdigit():
        feeding_expenses2.append(row)
        continue
    else:
        if 'bs' in row:
            feeding_expenses2.append(re.sub("\D","",row))
feeding_expenses2 = np.array(feeding_expenses2)
data[0::,54] = feeding_expenses2

# SIGUIENTE PASO, ESTANDARIZAR LOS GASTOS DE TRANSPORTE

transportation_expenses = data[0::,55]
transportation_expenses2 = []
for row in transportation_expenses:
    if row.isdigit():
        transportation_expenses2.append(row)
        continue
    else:
        if 'bs' in row:
            transportation_expenses2.append(re.sub("\D","",row))
transportation_expenses2 = np.array(transportation_expenses2)
data[0::,55] = transportation_expenses2

# SIGUIENTE PASO, ESTANDARIZAR GASTOS MEDICOS DEL REPRESENTANTE ECONÓMICO.

medical_e = data[0::,56]
medical_e2 = []

for row in medical_e:
    if row.isdigit():
        medical_e2.append(row)
        continue
    if '.' in row:
        medical_e2.append(row)
        continue
    if 'bs' in row:
        medical_e2.append(re.sub("\D","",row))
        continue
    if row == '':
        medical_e2.append('0')
medical_e2 = np.array(medical_e2)
data[0::,56] = medical_e2

# SIGUIENTE PASO, ESTANDARIZAR GASTOS ODONTOLÓGICOS
dental_e = data[0::,57]
dental_e2 = []

for row in dental_e:
    if row.isdigit():
        dental_e2.append(row)
        continue
    if row == '':
        dental_e2.append('0')
        continue
    dental_e2.append('0')
dental_e2 = np.array(dental_e2)
data[0::,57] = dental_e2

# SIGUIENTE PASO, ESTANDARIZAR GASTOS EDUCATIVOS
educational_e = data[0::,58]
educational_e2 = []

for row in educational_e:
    if row.isdigit():
        educational_e2.append(row)
        continue
    if 'NA' in row:
        educational_e2.append('0')
        continue    
educational_e2 = np.array(educational_e2)
data[0::,58] = educational_e2

# SIGUIENTE PASO, ESTANDARIZAR GASTOS SERVICIO PUBLICO
public_e = data[0::,59]
public_e2 = []

for row in public_e:
    if row.isdigit():
        public_e2.append(row)
        continue
    if 'bs' in row:
        public_e2.append(re.sub("\D","",row))
        continue 
    if row == '':
        public_e2.append('0')
        continue 
public_e2 = np.array(public_e2)
data[0::,59] = public_e2

# SIGUIENTE PASO, ESTANDARIZAR GASTOS DE CONDOMINIO
condominium_e = data[0::,60]
condominium_e2 = []

for row in condominium_e:
    if row.isdigit():
        condominium_e2.append(row)
        continue
    if 'bs' in row:
        condominium_e2.append(re.sub("\D","",row))
        continue 
    if row == '':
        condominium_e2.append('0')
        continue
    if '.' in row:
        condominium_e2.append(row)
        continue
condominium_e2 = np.array(condominium_e2)
data[0::,60] = condominium_e2

# SIGUIENTE PASO, FORMATEAR OTROS GASTOS REFERENTE AL RESPONSABLE ECONOMICO
other_e = data[0::,61]
other_e2 = []

for row in other_e:
    if row.isdigit():
        other_e2.append(row)
        continue
    if '.' in row:
        other_e2.append(row)
        continue    
    if 'NA' in row:
        other_e2.append('0')
        continue 
other_e2 = np.array(other_e2)
data[0::,61] = other_e2

#ESTO PARA QUITAR EL MAS EN MATERIAS PASADAS
mp = data[0::,13]
mp2 = []

for row in mp:
    if row.isdigit():
        mp2.append(row)
        continue
    mp2.append(re.sub("\D","",row))
mp2 = np.array(mp2)
data[0::,13] = mp2

delete = np.s_[11,21,27,28,30,32,37,43,47,51,52,62,64]   #columnas a eliminar
data2 = np.delete(data, delete, 1) #eliminamos las columnas

header = ['Periodo Académico a renovar','Cedula de identidad','Fecha de Nacimiento','Edad','Estado Civil','Sexo','Escuela','Año de ingreso a la Ucv','Modalidad de ingreso a la UCV','Semestre que cursa','Ha cambiado usted de dirección','Número de materias incritas en el semestre o año anterior','Número de materias aprobadas en el semestre o año anterior','Número de materias retiradas en el semestre o año anterior','Numero de materias reprobadas en el semestre o año anterior','Promedio ponderado aprobado','Eficiencia','Si reprobó una o más materias indique el motivo','Número de materias inscritas en el semestre en curso','Estás realizando TEG o pasantías de grado','Procedencia','Lugar donde reside mientras estudia en la Universidad','Personas con las cuales usted vive mientras estudia en la Universidad','Tipos de vivienda donde reside mientras estudia en la Universidad','En caso de vivir en habitación alquilada o residencia estudiantil, indique el monto mensual','Ha solicitado algún otro beneficio a la Universidad u otra institución','Se encuentra usted realizando alguna actividad que le genere ingresos, cual?','Monto mensual de la beca','Aporte mensual que le brinda su responsable económico','Aporte mensual que recibe de familiares o amigos','ingreso mensual que recibe por actividades a destajo o por horas','Gastos de alimentación','Gastos de transporte público','Gastos médicos','Gastos odontológicos','Gastos personales','Gastos de materiales de estudio','Gastos de recreación','Otros gastos','Indique quien es su responsable económico','Carga familiar de su responsable económico','Ingreso mensual de su responsable económico','Gastos de vivienda','Gastos de Alimentación','Gastos de Transporte','Gastos médicos','Gastos odontológicos','Gastos educativos','Gastos de Servicios publicos(agua, luz, teléfono, gas)','Gastos de condominio','Otros gastos','Deseamos conocer la opinion de nuestros usuarios para mejorar la calidad de los servicios ofrecidos por el Dpto de trabajo social OBE']
#data2 = np.insert(data2, 0, header, 0) #para agregarle el header al data2
#np.savetxt("minable.csv", data2, fmt='%.18e', delimiter=";")

# Lo siguiente es para guardar data2 en un csv
outfile = open('minable.csv', 'wb')
writer = csv.writer(outfile)

writer.writerow(header)
for row in data2:
    writer.writerow(row)
outfile.close()


