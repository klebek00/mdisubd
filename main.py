# main.py

from app.services.auth.main_menu import register, login, guest_menu

def main_menu():
    """
    Главное меню приложения.
    """
    while True:
        print("\nДобро пожаловать! Выберите действие:")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Войти как неавторизованный пользователь")

        print("0. Выйти")

        choice = input("Введите ваш выбор (1/2/0): ").strip()

        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            guest_menu()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
