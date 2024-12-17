# Запрос для получения всех медикаментов
GET_ALL_MEDICINES = "SELECT id, name FROM medicines;"

# Запрос для поиска медикаментов по названию
SEARCH_MEDICINES_BY_NAME = "SELECT id, name FROM medicines WHERE name ILIKE %s;"

# Запрос для получения детальной информации о медикаменте
GET_MEDICINE_DETAILS = '''SELECT 
                    m.id AS medicine_id,
                    m.name AS medicine_name,
                    m.code AS medicine_code,
                    m.description AS medicine_description,
                    m.instruction AS medicine_instructions,
                    m.price AS medicine_price,
                    s.name AS supplier_name,
                    c.name AS category_name
                FROM 
                    medicines m
                LEFT JOIN 
                    supplier s ON m.supplierid = s.id
                LEFT JOIN 
                    categories c ON m.categoryid = c.id
                WHERE 
                    m.id = %s;'''
