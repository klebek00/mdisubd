from ...db.connection import get_connection
from ...db.queries.userQ import CHECK_USER_EXISTS, INSERT_NEW_USER, CHECK_USER_CREDENTIALS
from ...db.queries.medQ import (
    GET_ALL_MEDICINES,
    SEARCH_MEDICINES_BY_NAME,
    GET_MEDICINE_DETAILS,
)
from ...db.queries.categoryQ import (
    GET_ALL_CATEGORIES,
)
from ...db.queries.departQ import (
    GET_ALL_DEPARTMENTS,
)
from datetime import datetime

def format_time_to_minutes(time_obj):
    """
    Форматирует время в формате 'HH:MM'.
    """
    if time_obj:  # Проверяем, что время не None
        return time_obj.strftime("%H:%M")  # Вызываем метод strftime для объекта time
    return None



def view_medicines():
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
                            view_medicine_details(medicine_id)
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

def view_medicine_details(medicine_id):
    """
    Получение детальной информации о медикаменте по его ID.
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
            else:
                print("Медикамент не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


def view_category():
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


def view_depart():
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

