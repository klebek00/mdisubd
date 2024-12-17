REV = """SELECT r.id, r.user_id, r.title, r.rating, r.text, r.date, u.name
                FROM review r
                JOIN users u ON r.user_id = u.id
                ORDER BY r.date DESC;"""

ADD_REV = """INSERT INTO review (user_id, title, rating, text, date)
                VALUES (%s, %s, %s, %s, NOW());"""