import pandas as pd
import pyodbc


def mostrar_filas (data,filtro):
    
    
    data = data[filtro]
    data = data[["IdPersona","Ticket"]]
    for columna,fila in data.iterrows():
        
        print (fila,"----",columna)

def conector_db ():
    
   
    
    
    server = 'raizenarbidwaz.database.windows.net' 
    database = 'raizenarbidw' 
    username = 'raizenadmin' 
    password = 'RaizenArgentina2020' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    """
    cursor = cnxn.cursor()
    cursor.execute ("SELECT TOP(10) *  FROM [raizenarbidw].[fid].[DIM_Socios]")
    rows = cursor.fetchall()
    #rows = cursor.tables()
    for row in rows:
        print(row)
    """
    return cnxn
   
#########programa principal#######
consulta = """SELECT 
       socios.[IdPersona]
      ,[Nombre]
      ,[Apellido]
      ,[Correo]
      ,[FechaNacimiento]
      ,[Genero]
      ,[RecibeCorreo]
      ,[NumeroCuenta]
      ,[FechaRegistro]
      ,[Tarjeta]
      ,[Baja]
      ,[Año]
      ,[Desuscripto]
      ,[Vehiculo]
      ,[NumeroTelefono]
      ,[Documento]
      ,[FechaPerdido]
	  ,compras.[IdPersona] as ID_PERSONA
	  ,compras.[Producto]
	  ,compras.[Litros]
	  ,compras.[Boca]
	  ,compras.[OperationCode]
	  ,CONCAT(transacciones.[LocCodigo],transacciones.[TDCodigo],transacciones.[DocNroInt]) as ticket_concat
	  
	  
	  FROM [raizenarbidw].[fid].[DIM_Socios] socios 
      INNER JOIN [raizenarbidw].[fid].[FACT_Compras] Compras ON socios.IdPersona = Compras.IdPersona
      INNER JOIN [raizenarbidw].[dom].[SLP_Transacciones] transacciones ON transacciones.SLPNroAutorizacion = Compras.OperationCode
    """

consulta_2 = """SELECT
               ventas.[LocCodigo]
              ,ventas.[ArtCodigo]
              ,ventas.[TotalFacturado]
              ,ventas.[Ticket]
              ,ventas.[DocFecha]
              ,ventas.[DocHora]
              ,articulos.[FMCodigo]
              ,articulos.[ArtTipo]
              ,familia.[Level2]
              ,familia.[Level3]
              ,familia.[Category]
              ,familia.[Subcategory]
              ,locales.[LocDirecc]
              ,locales.[Loclocali]
              ,locales.[Id_Base]
              ,locales.[ProCodigo]
              ,for_pago.[FPDescrip]
              ,compras_tarjeta.[DocNumeroPrefijo] as tarjeta_DocNumeroFijo
              ,compras_tarjeta.[DocNumero] as tarjeta_doc_numero
              ,compras_tarjeta.[FPCodigo] as tarjeta_fp_codigo
              ,compras_tarjeta.[TTUltimos4] as tarjeta_TT_ultimos_4
              ,compras_tarjeta.[TTImporte] as tarjeta_importe
              ,margen_ventas.[TotalFacturado] as margen_ventas_total
              ,margen_ventas.[VenCodigo]
              ,margen_ventas.[CantidadFacturada]
            
              FROM  [raizenarbidw].[dom].[fact_domino_ventas] ventas   
              INNER JOIN [raizenarbidw].[dom].[DIM_Articulos] articulos ON ventas.ArtCodigo = articulos.ArtCodigo
              INNER JOIN [raizenarbidw].[dom].[DIM_Familias_Prisma] familia ON articulos.FMCodigo = familia.FMCodigo
              INNER JOIN [raizenarbidw].[dom].[DIM_LOCALES] locales ON locales.LocCodigo = ventas.LocCodigo
              INNER JOIN [raizenarbidw].[dom].[TicketFormaPago] for_pago ON for_pago.ticket = ventas.Ticket
              INNER JOIN [raizenarbidw].[dom].[Fact_Compras_Tarjeta] compras_tarjeta ON compras_tarjeta.Ticket = ventas.Ticket
              INNER JOIN [raizenarbidw].[dom].[fact_domino_ventasMargen] margen_ventas ON margen_ventas.Ticket = ventas.Ticket
              
             
       
"""
"""
conector = conector_db()
df = pd.read_sql_query(consulta,conector)
df.to_csv("tabla_1.csv")
"""
conector = conector_db()
df_2 = pd.concat([x for x in pd.read_sql(consulta_2, conector, chunksize=10**5)],
                   ignore_index=True)
#conector.close()
print (df_2.head(10))
#df_2 = pd.read_sql_query(consulta_2,conector)
df_2.to_csv("tabla_2.csv")