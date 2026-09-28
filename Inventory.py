import sqlite3

DATABASE = "inventory.db"


def connect():
    return sqlite3.connect(DATABASE)


def setup_database():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                supplier TEXT
            )
        """)


def add_product():
    print("\n--- Add Product ---")

    name = input("Product name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))
    supplier = input("Supplier name: ")

    with connect() as con:
        con.execute("""
            INSERT INTO products
            (name, category, price, quantity, supplier)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, price, quantity, supplier))

    print("\nProduct added successfully!")


def view_products():
    print("\n--- Inventory ---")

    with connect() as con:
        products = con.execute("""
            SELECT id, name, category, price, quantity, supplier
            FROM products
            ORDER BY id DESC
        """).fetchall()

    if not products:
        print("No products found.")
        return

    for product in products:
        print("\n----------------------------")
        print("ID:", product[0])
        print("Product:", product[1])
        print("Category:", product[2])
        print("Price:", product[3])
        print("Quantity:", product[4])
        print("Supplier:", product[5])


def update_stock():
    print("\n--- Update Stock ---")

    product_id = input("Enter product ID: ")
    quantity = int(input("Enter new quantity: "))

    with connect() as con:
        cursor = con.execute("""
            UPDATE products
            SET quantity = ?
            WHERE id = ?
        """, (quantity, product_id))

    if cursor.rowcount > 0:
        print("Stock updated successfully!")
    else:
        print("Product not found.")


def delete_product():
    print("\n--- Delete Product ---")

    product_id = input("Enter product ID: ")

    with connect() as con:
        cursor = con.execute("""
            DELETE FROM products
            WHERE id = ?
        """, (product_id,))

    if cursor.rowcount > 0:
        print("Product deleted successfully!")
    else:
        print("Product not found.")


def search_product():
    print("\n--- Search Product ---")

    keyword = input("Enter product name or category: ")

    with connect() as con:
        products = con.execute("""
            SELECT id, name, category, price, quantity
            FROM products
            WHERE name LIKE ?
            OR category LIKE ?
        """, (
            "%" + keyword + "%",
            "%" + keyword + "%"
        )).fetchall()

    if not products:
        print("No products found.")
        return

    for product in products:
        print(
            f"ID: {product[0]} | "
            f"Product: {product[1]} | "
            f"Category: {product[2]} | "
            f"Price: {product[3]} | "
            f"Quantity: {product[4]}"
        )


def low_stock():
    print("\n--- Low Stock Products ---")

    with connect() as con:
        products = con.execute("""
            SELECT id, name, category, quantity
            FROM products
            WHERE quantity <= 5
            ORDER BY quantity ASC
        """).fetchall()

    if not products:
        print("No low-stock products.")
        return

    for product in products:
        print(
            f"ID: {product[0]} | "
            f"Product: {product[1]} | "
            f"Category: {product[2]} | "
            f"Quantity: {product[3]}"
        )


def show_statistics():
    print("\n--- Inventory Statistics ---")

    with connect() as con:
        total_products = con.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        total_quantity = con.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM products"
        ).fetchone()[0]

        inventory_value = con.execute(
            "SELECT COALESCE(SUM(price * quantity), 0) FROM products"
        ).fetchone()[0]

        low_stock_count = con.execute(
            "SELECT COUNT(*) FROM products WHERE quantity <= 5"
        ).fetchone()[0]

    print("Total products:", total_products)
    print("Total quantity:", total_quantity)
    print("Total inventory value:", inventory_value)
    print("Low stock products:", low_stock_count)


def main():
    setup_database()

    while True:
        print("\n==============================")
        print("    INVENTORY MANAGEMENT")
        print("==============================")

        print("1. Add Product")
        print("2. View Products")
        print("3. Update Stock")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. View Low Stock")
        print("7. View Statistics")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            update_stock()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            search_product()

        elif choice == "6":
            low_stock()

        elif choice == "7":
            show_statistics()

        elif choice == "8":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()