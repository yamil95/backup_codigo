CREATE PROCEDURE TICKETS_FP( @cant_ticket INT, @cant_forma_pago INT)
AS
BEGIN

		with c 

		as(

		SELECT ticket,count (distinct([FPDescrip])) as cantidad_de_f_d_pago,count(ticket)as cant_tickets_repetidos

		FROM [dom].[TicketFormaPago]

		GROUP BY ticket
		)

		select * from c where  cant_tickets_repetidos >=@cant_ticket and cantidad_de_f_d_pago >= @cant_forma_pago 
END 