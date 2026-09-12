import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",  # Replace with environment variable or placeholder
        database="price_tracker",
    )


def add_product(name, url, target_price):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO products (name, url, target_price) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, url, target_price))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[+] Product added: {name}")


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def update_product_price(product_id, current_price, is_in_stock):
    conn = get_connection()
    cursor = conn.cursor()

    # Update current status in products table
    update_query = """
        UPDATE products 
        SET current_price = %s, is_in_stock = %s 
        WHERE product_id = %s
    """
    cursor.execute(update_query, (current_price, is_in_stock, product_id))

    # Log entry into price_history table
    history_query = (
        "INSERT INTO price_history (product_id, price) VALUES (%s, %s)"
    )
    cursor.execute(history_query, (product_id, current_price))

    conn.commit()
    cursor.close()
    conn.close()
