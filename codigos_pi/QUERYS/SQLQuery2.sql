CREATE VIEW  trackeo_segmentacion_6_meses
AS
SELECT  
               ventas.[LocCodigo]
              ,ventas.[ArtCodigo]
              ,ventas.[TotalFacturado]
			  ,ventas.[CantidadFacturada]
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
			  
             
            
              FROM  [raizenarbidw].[dom].[fact_domino_ventas] ventas   
              INNER JOIN [raizenarbidw].[dom].[DIM_Articulos] articulos ON ventas.ArtCodigo = articulos.ArtCodigo
              INNER JOIN [raizenarbidw].[dom].[DIM_Familias_Prisma] familia ON articulos.FMCodigo = familia.FMCodigo
              INNER JOIN [raizenarbidw].[dom].[DIM_LOCALES] locales ON locales.LocCodigo = ventas.LocCodigo
              inner JOIN [raizenarbidw].[dom].[TicketFormaPago] for_pago ON for_pago.ticket = ventas.Ticket
              INNER JOIN [raizenarbidw].[dom].[Fact_Compras_Tarjeta] compras_tarjeta ON compras_tarjeta.Ticket = ventas.Ticket
			  where  ventas.[DocFecha] > GETDATE() -180 