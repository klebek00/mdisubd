GET_CART = """SELECT id
                FROM cart
                WHERE user_id = %s;  
            """

GET_ITEM = """SELECT m.name, ci.quantity, m.price
                FROM cartitem ci
                JOIN medicines m ON ci.medic_id = m.id
                WHERE ci.cart_id = %s;
            """