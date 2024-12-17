ALL_ORDER = """SELECT id, date, price, department_id
                FROM sale
                WHERE user_id = %s
                ORDER BY date;
            """
ORDER_MED = """ SELECT oi.medic_id, m.name, oi.quantity, m.price
                        FROM saleitem oi
                        JOIN medicines m ON oi.medic_id = m.id
                        WHERE oi.sale_id = %s;"""