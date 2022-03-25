import re
from functools import reduce
import pandas as pd
def extraer():
    lista = []
    
    archivo = open("texto.txt","r")
    for linea in archivo :
        dato = re.search("[\d.]{1,4}[\s]{0,1}?((l)|(k)|(cc)|(lt)|(ml)|(gr)|(g))",linea)
        if dato != None:
            print (dato)
        
        
def extraer_unidades (cadena):
    
    print (cadena)


validar = lambda x: '0' if x == None else re.search ("[\d]{1,2}",x.group()).group()
 
def extraer_unidades (df):
    
    lista = list (map(lambda x: validar (re.search("((x[\s]{0,1}[\d]{1})\s|([\d]{1}x[\d])|(pack x\s[\d]{1}\s)|(x pack [\d]{1})|(\s[\d]{1}\s[un]{1,2})|(\([\d]{2} unidades\)))",x)),df["DescripcionLargaDelArticulo"]))
    df["cantidad"] = lista
    
    return df
     
cadena = "pack linea coca cola x500cc (12 unidades)"



######programa principal#####
#dato = re.search("\([\d]{1,2} unidades\)",cadena)
data = pd.read_csv("unidades.csv")
df =extraer_unidades(data)
print (df.head(50))
#extraer()