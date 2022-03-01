import pandas as pd
from math import nan
import re


def buscar_porcion_item (lista_marca:list , lista_item:list):
    
    
    for posicion in range (len(lista_item)):
        
        
        if len (lista_marca) == 1 and len (lista_item)>=1 and posicion < len (lista_item):
            #print ("marca: ",lista_marca[0],"---"," item:",lista_item[posicion])
            
            if lista_marca[0] == lista_item[posicion]:
                
                
                return lista_marca[0]
        
        if len (lista_marca) == 2 and len (lista_item)>=2 and posicion+1< len (lista_item):
            
            
            
            if lista_marca[0]== lista_item[posicion] and lista_marca[1] == lista_item[posicion+1]:
                #print ("marca: ",lista_marca[0],lista_marca[1],"---"," item:",lista_item[posicion],lista_item[posicion+1])
                
                return lista_marca[:]
        
        if len (lista_marca) == 3 and len (lista_item)>=3 and posicion+2 < len(lista_item):
            #print ("marca: ",lista_marca[0],lista_marca[1],lista_marca[2],"---"," item:",lista_item[posicion],lista_item[posicion+1],lista_item[posicion+2])
            if lista_marca[0] == lista_item[posicion] and lista_marca[1] == lista_item[posicion+1] and lista_marca[2]==lista_item[posicion+2]:
                return lista_marca[:]
            
            
    
    
    
    
###### funcion #########
def buscar_marca(maestro : pd.DataFrame,scrap:pd.DataFrame):

    lista = []
    flag = 0

    for item in maestro["item"]:

        for marca in scrap["marca"]:

            item_x = re.sub("[\"]*|\sx\s[\d]{1,}\s[\w]{1,}|\s[\d]{1,}[\w]{1,}|\sx\s[\d]{1,}|\sx|\scc|c\/","", str (item) )
            item_x= item_x.split(" ")
            marca_z = marca.split(" ")
            marca_x = buscar_porcion_item(marca_z,item_x)
            if marca_x != None:
                marca_x = "".join(marca_x)
                print (item,"  marca_encontrada :---> ", marca_x )
                break
        
        if marca_x != None:
            lista.append(marca_x)
        else :
            lista.append("sin marca")
            
    
    return lista
     
   
     

#######################
    

data_scrap = pd.read_csv('scrap_ordenado.csv', sep=';')
data_maestro = pd.read_csv('maestro_ordenado.csv', sep=';')
#data_scrap = data_scrap.sort_values("marca")
data_scrap = data_scrap.drop_duplicates()
#data_maestro = data_maestro.sort_values("item")
#data_scrap = data_scrap.sort_values("marca")
#data_scrap.to_excel("scrap_ordenado.xlsx")
#data_maestro.to_excel("maestro_ordenado.xlsx")
data_scrap["marca"]= data_scrap["marca"].str.lower()
data_maestro["item"]= data_maestro["item"].str.lower()
#data_scrap.to_excel("scrap_ordenado.xlsx")
#data_maestro.to_excel("maestro_ordenado.xlsx")
#extraer_indices(data_maestro,data_scrap) 

lista = buscar_marca(data_maestro,data_scrap)
data_maestro["columna_marca"] = pd.Series (lista)

data_maestro.head()
#data_maestro.to_excel("salida_tabla.xlsx")




