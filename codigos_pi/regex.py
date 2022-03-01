import re
def extraer():
    lista = []
    
    archivo = open("texto.txt","r")
    for linea in archivo :
        dato = re.search("[\d.]{1,4}[\s]{0,1}?((l)|(k)|(cc)|(lt)|(ml)|(gr)|(g))",linea)
        if dato != None:
            print (dato)
        
        
    
        



######programa principal#####
        
extraer()