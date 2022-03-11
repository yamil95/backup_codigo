create view tickets_compuestos_y_exclusivos

AS

with c

as
(
select Ticket, count(distinct (Category))as cantidad_categorias

from [dbo].[trackeo_Segmentacion_6_meses]

group by Ticket

)

select Ticket ,cantidad_categorias,

	CASE 
		WHEN cantidad_categorias >1 then 'compuesto'
		WHEN cantidad_categorias =1 then 'unico'
    END AS 'EXCLUSIVOS'
FROM C