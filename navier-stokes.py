import numpy as np
import matplotlib.pyplot as pl
alto=50
ancho=50
#incognitas
x0=np.zeros(alto*alto)
#sistema de ecuaciones despues de discretizar
sistema=[]
#vector de terminos independientes
Ti=np.zeros(ancho*ancho)
U = np.zeros((alto, ancho))
diferencia=np.ones( ancho*ancho,dtype= float)
Uinicial=2
u=5
v=5
#barra
altoBarra=20
anchoBarra=4
posXBarra=25

#establece la veocidad inicial (La primera columna de la matriz)
for i in range(0,alto-1):
    U[i,0]=Uinicial


#llena la matriz con numeros iniciales

for i in range(alto):
  for j in range(1,ancho):
    U[i,j]=U[i,j-1]-1/ancho

#celdas relacionadas a la barra en 0
for i in range(alto-altoBarra,alto):
  for j in range(posXBarra-int(anchoBarra/2),posXBarra+int(anchoBarra/2)):
    U[i,j]=0



#linea EA u=0  w=o
for j in range(ancho):
    U[alto-1,j]=0


#Lado detrás de la viga B

for i in range(alto-altoBarra,alto-1):
  j=posXBarra+int(anchoBarra/2)
  U[i,j]=0


#Lado arriba de la viga C


for j in range(posXBarra-int(anchoBarra/2),posXBarra+int(anchoBarra/2)):
  i=alto-altoBarra
  U[i,j]=0

#Lado frontal de la viga D

for i in range(alto-altoBarra,alto-1):
  j=posXBarra-int(anchoBarra/2)-1
  U[i,j]=0
 


#Inlet (entrada) F
for i in range(alto-1):
  j=0
  U[i,j]=Uinicial

#Surface G
for i in range(alto-altoBarra-anchoBarra):
  for j in range(ancho):
    U[i,j]=Uinicial



#Outlet (salida) H

for i in range(alto):
  j=alto-1
  U[i,j]=U[i,j-1]

#determina donde esta ubicada una ecuacion
def puesto(i,j):
  p=0
  for x in range(alto):
    for y in range(ancho):
      if x==i and y==j:
        return p
      else:
        p=p+1


#se encarga de generar las ecuaciones
def ecuacion(i,j):
 
  ecu=np.zeros(ancho*ancho)
  ecu[puesto(i,j)]=-4
  if i < alto-1:
      ecu[puesto(i+1,j)]=(1-u/2)
  if i > 0:
      ecu[puesto(i-1,j)]=(1-u/2)
  if j < ancho-1:
      ecu[puesto(i,j+1)]=(1-v/2)
  if j != 0:
      ecu[puesto(i,j-1)]=(1-v/2)
  return ecu


##################################################
#armamos el sistema resultante
for i in range(alto):
  for j in range(ancho):
    sistema.append(ecuacion(i,j))

sis=np.zeros((alto*alto,ancho*ancho))
for i in range(alto*alto):
  for j in range(ancho*ancho):
    sis[i,j]=sistema[i][j]
sistema=sis
#################################################

#establecemos las condiciones iniciales con ls terminos independientes
for i in range(alto):
  for j in range(ancho):
    Ti[puesto(i,j)]=U[i,j]

def seidel():

  it=5 #numero de iteraciones
  while it > 0:
    suma=0
    for i in range(alto*alto):
      suma=0
      for j in range(ancho*ancho):
        if ( j!= i):
          suma=suma+sistema[i,j]*x0[j]
      nuevo=(Ti[i]-suma)/-sistema[i,i]
      x0[i]=nuevo
    it=it-1



#armar u
def armar_U():
  u=0

  for i in range(alto):
    for j in range(ancho):
      U[i,j]=x0[u]
      u=u+1


seidel()
armar_U()

print(Ti)
print(sistema)

colormap=pl.imshow(U)
pl.colorbar(colormap)

