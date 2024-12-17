from ...db.connection import get_connection
from ...db.queries.userQ import CHECK_USER_EXISTS, INSERT_NEW_USER, CHECK_USER_CREDENTIALS
from ...db.queries.medQ import (
    GET_ALL_MEDICINES,
    SEARCH_MEDICINES_BY_NAME,
    GET_MEDICINE_DETAILS,
)
from ...db.queries.orderQ import (
    ALL_ORDER,
    ORDER_MED
)
from ...db.queries.reviewQ import (
    REV,
    ADD_REV
)
from ...db.queries.categoryQ import (
    GET_ALL_CATEGORIES,
)
from ...db.queries.departQ import (
    GET_ALL_DEPARTMENTS,
)
from ...db.queries.cartQ import (
    GET_CART,
    GET_ITEM
)
from datetime import datetime

def format_time_to_minutes(time_obj):
    """
    Форматирует время в формате 'HH:MM'.
    """
    if time_obj:  # Проверяем, что время не None
        return time_obj.strftime("%H:%M")  # Вызываем метод strftime для объекта time
    return None



def user_view_medicines(user_id):
    """Вывод всех медикаментов с возможностью поиска и получения дополнительной информации."""
    conn = get_connection()
    try:
        while True:
            print("\n1. Показать все медикаменты")
            print("2. Искать медикамент по названию")
            print("0. Назад в меню")
            
            choice = input("Введите ваш выбор (1/2/0): ").strip()
            
            if choice == "1":
                with conn.cursor() as cursor:
                    cursor.execute(GET_ALL_MEDICINES)
                    medicines = cursor.fetchall()
                    if medicines:
                        print("\nСписок медикаментов:")
                        for medicine in medicines:
                            print(f"{medicine['id']}. {medicine['name']}")
                        print("\nВведите ID медикамента для получения дополнительной информации или 0 для возврата.")
                        
                        medicine_id = input("Введите ID: ").strip()
                        if medicine_id == "0":
                            continue
                        else:
                            user_view_medicine_details(medicine_id, user_id)
                    else:
                        print("Медикаменты отсутствуют в базе данных.")
            elif choice == "2":
                search_term = input("Введите название медикамента для поиска: ").strip()
                with conn.cursor() as cursor:
                    cursor.execute(SEARCH_MEDICINES_BY_NAME, (f"%{search_term}%",))
                    medicines = cursor.fetchall()
                    if medicines:
                        print("\nРезультаты поиска:")
                        for medicine in medicines:
                            print(f"{medicine['id']}. {medicine['name']}")
                    else:
                        print("Медикаменты не найдены.")
            elif choice == "0":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

def user_view_medicine_details(medicine_id, user_id):
    """
    Получение детальной информации о медикаменте по его ID и возможность добавить в корзину.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(GET_MEDICINE_DETAILS, (medicine_id,))
            medicine = cursor.fetchone()
            if medicine:
                print("\nИнформация о медикаменте:")
                print(f"Название: {medicine['medicine_name']}")
                print(f"Код: {medicine['medicine_code']}")
                print(f"Описание: {medicine['medicine_description']}")
                print(f"Инструкция: {medicine['medicine_instructions']}")
                print(f"Цена: {medicine['medicine_price']} руб.")
                print(f"Поставщики: {medicine['supplier_name']}")
                print(f"Категория: {medicine['category_name']}")
                print("-" * 20)

                # Запросить добавление в корзину
                add_to_cart = input("Хотите добавить этот медикамент в корзину? (да/нет): ").strip().lower()
                if add_to_cart == 'да':
                    quantity = input("Введите количество: ").strip()
                    if quantity.isdigit() and int(quantity) > 0:
                        quantity = int(quantity)
                        try:
                            cursor.execute("CALL add_to_cart(%s, %s, %s);", (user_id, medicine_id, quantity))
                            conn.commit()
                            print(f"{medicine['medicine_name']} добавлен(ы) в корзину в количестве {quantity}.")
                        except Exception as e:
                            print(f"Ошибка при добавлении в корзину: {e}")
                    else:
                        print("Количество должно быть положительным числом.")
                elif add_to_cart == 'нет':
                    print("Медикамент не был добавлен в корзину.")
                else:
                    print("Неверный ввод.")
            else:
                print("Медикамент не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()



def user_view_category():
    """Вывод списка категорий медикаментов."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(GET_ALL_CATEGORIES)
            categories = cursor.fetchall()
            if categories:
                print("\nСписок категорий:")
                for category in categories:
                    print(f"{category['id']}. {category['name']}")
            else:
                print("Категории отсутствуют в базе данных.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


def user_view_depart():
    """Вывод всех отделений аптеки с информацией о них."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(GET_ALL_DEPARTMENTS)
            departments = cursor.fetchall()
            if departments:
                print("\nСписок отделений:")
                for dept in departments:
                    open_time = format_time_to_minutes(dept['open'])
                    close_time = format_time_to_minutes(dept['close'])
                    print(f"Отделение № {dept['no']}")
                    print(f"Адрес: {dept['address']}")
                    print(f"C {open_time} до {close_time}")
                    print("-" * 20)
            else:
                print("Отделения отсутствуют в базе данных.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

def view_promocodes():
    """
    Функция для просмотра списка промокодов.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Запрос на выборку всех промокодов
            cursor.execute("SELECT id, code, discount FROM promocode;")
            promocodes = cursor.fetchall()

            if promocodes:
                print("\nСписок промокодов:")
                print(f"{'ID':<5} {'Код':<15} {'Скидка':<10}")
                print("-" * 30)
                for promo in promocodes:
                    print(f"{promo['id']:<5} {promo['code']:<15} {promo['discount']}%")
            else:
                print("Промокоды отсутствуют.")
    except Exception as e:
        print(f"Ошибка при получении промокодов: {e}")
    finally:
        conn.close()

from ...db.connection import get_connection

def view_reviews():
    """
    Функция для просмотра списка отзывов.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(REV)
            reviews = cursor.fetchall()

            if reviews:
                print("\nСписок отзывов:")
                print(f"{'':<20} {'Заголовок':<20} {'Оценка':<8} {'Дата':<30} {'Текст'}")
                print("-" * 100)
                for review in reviews:
                    # Ограничим длину текста (например, 50 символами)
                    review_text = review['text'] if len(review['text']) <= 50 else review['text'][:50] + '...'
                    # Преобразуем дату в строковый формат (если нужно)
                    formatted_date = review['date'].strftime("%Y-%m-%d %H:%M:%S") if review['date'] else "N/A"

                    # Выводим данные с форматированием
                    print(f"{review['name']:<20} {review['title']:<20} {review['rating']:<8} {formatted_date:<30} {review_text}")
            else:
                print("Отзывы отсутствуют.")
    except Exception as e:
        print(f"Ошибка при получении отзывов: {e}")
    finally:
        conn.close()


def add_review(user_id):
    """
    Функция для добавления отзыва пользователем.
    """
    print("\n--- Написать отзыв ---")
    
    title = input("Введите заголовок отзыва: ").strip()
    rating = input("Введите рейтинг (1-5): ").strip()
    text = input("Введите текст отзыва: ").strip()

    # Проверка валидности рейтинга
    if not rating.isdigit() or int(rating) not in range(1, 6):
        print("Ошибка: Рейтинг должен быть числом от 1 до 5.")
        return

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Запрос для добавления нового отзыва
            cursor.execute(ADD_REV, (user_id, title, int(rating), text))
            conn.commit()

            print("Отзыв успешно добавлен!")
    except Exception as e:
        print(f"Ошибка при добавлении отзыва: {e}")
    finally:
        conn.close()

def view_cart(user_id):
    """
    Функция для просмотра содержимого корзины пользователя и оформления заказа.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Получаем id корзины пользователя
            cursor.execute(GET_CART, (user_id,))
            cart = cursor.fetchone()

            if not cart:
                print("У вас нет активной корзины.")
                return

            cart_id = cart['id']

            # Получаем содержимое корзины
            cursor.execute(GET_ITEM, (cart_id,))
            cart_items = cursor.fetchall()

            if not cart_items:
                print("Ваша корзина пуста.")
                return

            # Выводим содержимое корзины
            print("\nСодержимое вашей корзины:")
            print(f"{'Название':<25} {'Количество':<10} {'Цена':<10} {'Сумма'}")
            print("-" * 60)

            total_cost = 0
            for item in cart_items:
                total_item_cost = item['quantity'] * item['price']
                total_cost += total_item_cost
                print(f"{item['name']:<25} x{item['quantity']:<10} {item['price']:<10} {total_item_cost:.2f}")

            print("-" * 60)
            print(f"{'Общая стоимость:':<45} {total_cost:.2f}")

            # Спрашиваем, хочет ли пользователь оформить заказ
            order_confirm = input("\nХотите оформить заказ? (да/нет): ").strip().lower()
            if order_confirm == 'да':
                place_order(cart_id, user_id, total_cost)
            else:
                print("Корзина не была оформлена.")

    except Exception as e:
        print(f"Ошибка при просмотре корзины: {e}")
    finally:
        conn.close()


def place_order(cart_id, user_id, total_cost):
    """
    Функция для оформления заказа с проверкой наличия медикаментов в выбранном отделении.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Запрашиваем у пользователя номер отделения для оформления заказа
            department_id = input("Введите номер отделения для оформления заказа: ").strip()

            # Проверяем, есть ли указанные медикаменты в выбранном отделении
            cursor.execute("""
                SELECT ci.medic_id, ci.quantity
                FROM cartitem ci
                JOIN medicines m ON ci.medic_id = m.id
                WHERE ci.cart_id = %s;
            """, (cart_id,))
            cart_items = cursor.fetchall()

            all_items_available = True
            for item in cart_items:
                # Проверка наличия медикамента в отделении
                cursor.execute("""
                    SELECT quantity
                    FROM department_medicine
                    WHERE depart_id = %s AND medic_id = %s;
                """, (department_id, item['medic_id']))

                stock = cursor.fetchone()
                if not stock or stock['quantity'] < item['quantity']:
                    print(f"В отделении {department_id} нет достаточного количества {item['medic_id']} ({item['quantity']} шт.).")
                    all_items_available = False

            if not all_items_available:
                print("Не все медикаменты доступны в выбранном отделении. Пожалуйста, выберите другое отделение.")
                return

            # Если все медикаменты доступны, оформляем заказ
            cursor.execute("CALL process_purchase(%s, %s)", (user_id, department_id))

            # Здесь можно добавить логику для добавления заказа в таблицу заказов

            conn.commit()
            print(f"Ваш заказ на сумму {total_cost:.2f} успешно оформлен в отделении {department_id}!")

    except Exception as e:
        print(f"Ошибка при оформлении заказа: {e}")
    finally:
        conn.close()

def view_user_orders(user_id):
    """
    Функция для вывода информации о всех заказах пользователя.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Получаем список заказов пользователя
            cursor.execute(ALL_ORDER, (user_id,))
            orders = cursor.fetchall()

            if orders:
                print(f"\nСписок заказов пользователя:")
                # Форматируем заголовок
                print(f"{'Номер':<10} {'Дата':<20} {'Сумма':<12} {'Номер отделения':<15}")
                print("-" * 60)

                for order in orders:
                    # Форматируем вывод
                    order_date = order['date'].strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату
                    total_cost = f"{order['price']:.2f}"  # Форматируем сумму

                    # Выводим информацию о заказе
                    print(f"{order['id']:<10} {order_date:<20} {total_cost:<12} {order['department_id']:<15}")

                    # Получаем товары для каждого заказа
                    cursor.execute(ORDER_MED, (order['id'],))
                    order_items = cursor.fetchall()

                    print("Продукты в заказе:")
                    for item in order_items:
                        # Выводим информацию о каждом товаре
                        print(f"    {item['name']:<20} x{item['quantity']} - {item['price']:.2f} руб.")
                    print("-" * 60)
            else:
                print("У пользователя нет заказов.")

    except Exception as e:
        print(f"Ошибка при получении заказов: {e}")
    finally:
        conn.close()
