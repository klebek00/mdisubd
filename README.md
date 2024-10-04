# mdisubd
## Клебеко Елена Юрьевна
## гр. 253504
# Аптека
# Описание проекта
# 1. Цели проекта
## 1.1 Основные цели проекта
Онлайн магазин аптеки
# 2. Описание проекта
## 2.1 Функциональные требования
### Возможности пользователя
- Авторизация и регистрация в систему
- Поиск препаратов
- Просмотр информации о препаратах
- Просмотр категорий препаратов
- Просмотр информации о отделениях аптеки
- Просмотр информации о действующих промокодах
- Оформление заказов
- Оставление отзывово с оценкой
### Возможности администратора
- Авторизация в системе
- Управление пользователями (CRUD)
- CRUD операции с данными
- Просмотр журна действий пользователя
## 2.2 Список сущностей
### 1. User//
- id: (INT, PK, AUTO_INCREMENT)
- name: (VARCHAR(50), NOT NULL)
- login: (VARCHAR(25), NOT NULL)
- password: (VARCHAR(50), NOT NULL)
- email: (VARCHAR(255), NOT NULL)
- status: (VARCHAR(25), NOT NULL, UNIQUE)
### 2. Logs//
- id (INT, PK) 
- action_date (DATETIME)
- action (VARCHAR(200))
- user_id (INT, FK)
### 3. Medicines//
- id: (INT, PK, AUTO_INCREMENT)
- name: (VARCHAR(100), NOT NULL)
- code: (VARCHAR(10), NOT NULL)
- instructions: (TEXT, NOT NULL)
- description: (TEXT, NOT NULL)
- cost: (INT, NOT NULL)
- photo: (VARCHAR(100), NOT NULL)
- categories_id: (INT, FK)
- supplier_id: (INT, FK)
### 4. Categories//
- id: (INT, PK, AUTO_INCREMENT)
- name: (VARCHAR(100), NOT NULL)
### 5. Department//
- no: (INT, PK)
- address: (VARCHAR(200), NOT NULL)
- open: (DATETIME)
- close: (DATETIME)
### 6. Department_Medicine ??
- depart_id: INT
- medic_id:  INT
- quantity: INT
### 6. Supplier//
- id: (INT, PK)
- name: (VARCHAR(100), NOT NULL)
- address: (VARCHAR(100), NOT NULL)
### 7. Promocode
- id: (INT, PK)
- code: (VARCHAR(20), NOT NULL)
- discount: (INT, NOT NULL)
### 8. Review//
- id: (INT, PK)
- user_id (INT, FK)
- title: (VARCHAR(100), NOT NULL)
- rating (INT, NOT NULL)
- text: (TEXT)
- date: (DATETIME)
### 9. Sale
- id (INT, PK, AUTO_INCREMENT)
- user_id (INT, FK)
- department_id (INT, FK)
- promocode_id (INT, FK, NULLABLE)
- price (INT)
- date (DATETIME, NOT NULL)
### 10. SaleItem
- id: INT, PK, AUTO_INCREMENT
- sale_id: INT, FK 
- medicine_id: INT, FK
- quantity: INT, NOT NULL
- price: INT
### 11. Cart//
- id (INT, PK, AUTO_INCREMENT)
- user_id (INT, FK)
### 12. CartItem
- id (INT, PK, AUTO_INCREMENT)
- cart_id (INT, FK)
- medicine_id (INT, FK)
- quantity (INT, NOT NULL)




![Диаграмма без названия drawio (6444) drawio](https://github.com/user-attachments/assets/3cf1cd5a-bd9b-43b0-9a2c-9b097ff2f3a1)




