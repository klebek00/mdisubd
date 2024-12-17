# db/queries.py

# Запрос для проверки существования пользователя по логину
CHECK_USER_EXISTS = "SELECT * FROM users WHERE login = %s;"

# Запрос для регистрации нового пользователя
INSERT_NEW_USER = """
INSERT INTO users (name, login, password, email, isuser, isadmin, isstaff)
VALUES (%s, %s, %s, %s, TRUE, FALSE, FALSE);
"""


# Запрос для проверки логина и пароля
CHECK_USER_CREDENTIALS = "SELECT * FROM users WHERE login = %s AND password = %s;"
