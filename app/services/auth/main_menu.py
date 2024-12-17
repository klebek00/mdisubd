from ...db.connection import get_connection
from ...db.queries.userQ import CHECK_USER_EXISTS, INSERT_NEW_USER, CHECK_USER_CREDENTIALS
from .guest_menu_def import view_category, view_depart, view_medicines
from .user_menu_def import user_view_category, user_view_medicines, user_view_depart, view_promocodes, view_reviews, add_review, view_cart, view_user_orders

# Глобальная переменная для хранения ID текущего пользователя
current_user_id = None

def login():
    """Функция для входа пользователя в систему."""
    global current_user_id  # Используем глобальную переменную для хранения ID пользователя
    
    login = input("Введите ваш логин: ").strip()
    password = input("Введите ваш пароль: ").strip()

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Выполним запрос для получения пользователя по логину и паролю
            cursor.execute("""
                SELECT id, name, isadmin, isuser, isstaff
                FROM users
                WHERE login = %s AND password = %s;
            """, (login, password))
            user = cursor.fetchone()

            if user:
                print(f"Добро пожаловать, {user['name']}!")
                current_user_id = user['id']  # Сохраняем ID текущего пользователя

                # Перенаправление в зависимости от роли пользователя
                if user['isadmin']:
                    admin_menu()  # Вызов меню администратора
                elif user['isuser']:
                    user_menu(current_user_id)  # Вызов меню пользователя с передачей ID
                else:
                    print("У вас нет доступа к функционалу.")
            else:
                print("Неверный логин или пароль!")
    except Exception as e:
        print(f"Ошибка при входе: {e}")
    finally:
        conn.close()

def user_menu(user_id):
    """Меню пользователя."""
    print("\nВы вошли как пользователь.")
    while True:
        print("\nМеню пользователя:")
        print("1. Просмотр препаратов")
        print("2. Просмотр категорий")
        print("3. Просмотр отделений аптеки")
        print("4. Корзина")
        print("5. Мои заказы")
        print("6. Промокоды")
        print("7. Отзывы")
        print("8. Оставить отзывы")
        print("0. Выйти из системы")

        choice = input("Введите ваш выбор: ").strip()

        if choice == "1":
            user_view_medicines(user_id)  # Передаем ID пользователя
        elif choice == "2":
            user_view_category()  # Аналогично передаем ID пользователя
        elif choice == "3":
            user_view_depart()
        elif choice == "4":
            view_cart(user_id)
        elif choice == "5":
            view_user_orders(user_id)
        elif choice == "6":
            view_promocodes()
        elif choice == "7":
            view_reviews()
        elif choice == "8":
            add_review(user_id)
        elif choice == "0":
            print("Выход из системы...")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


def admin_menu():
    """Меню администратора."""
    print("\nВы вошли как администратор.")
    # while True:
    #     print("\nМеню администратора:")
    #     print("1. Управление пользователями")
    #     print("2. Просмотр отчетов")
    #     print("0. Выйти из системы")

    #     choice = input("Введите ваш выбор: ").strip()

    #     if choice == "1":
    #         manage_users()  # Функция для управления пользователями
    #     elif choice == "2":
    #         view_reports()  # Функция для просмотра отчетов
    #     elif choice == "0":
    #         print("Выход из системы...")
    #         break
    #     else:
    #         print("Неверный ввод. Попробуйте снова.")


def guest_menu():
    """Гостевое меню."""

    print("\nВы вошли как гость.")
    while True:
        print("\nМеню пользователя:")
        print("1. Просмотр препаратов")
        print("2. Просмотр категорий")
        print("3. Просмотр отделений аптеки")
        print("0. Выйти из системы")

        choice = input("Введите ваш выбор: ").strip()

        if choice == "1":
            view_medicines()  # Функция для просмотра препаратов
        elif choice == "2":
            view_category()  # Функция для оформления заказа
        elif choice == "3":
            view_depart()
        elif choice == "0":
            print("Выход из системы...")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")




def register():
    """
    Логика регистрации нового пользователя.
    """
    print("\n--- Регистрация ---")
    name = input("Введите ваше имя: ").strip()
    login = input("Введите логин: ").strip()
    password = input("Введите пароль: ").strip()
    email = input("Введите email: ").strip()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Проверка существования пользователя
            cursor.execute(CHECK_USER_EXISTS, (login,))
            if cursor.fetchone():
                print("Пользователь с таким логином уже существует.")
                return

            # Вставка нового пользователя
            cursor.execute(INSERT_NEW_USER, (name, login, password, email))
            connection.commit()
            print("Регистрация успешно завершена!")
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
    finally:
        connection.close()

def guest_mode():
    """
    Логика входа в режим гостя.
    """
    print("\n--- Гостевой режим ---")
    print("Вы вошли как гость. Некоторые функции могут быть недоступны.")
    guest_menu()

