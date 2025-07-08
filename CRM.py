import mysql.connector
from mysql.connector import Error

class CustomerManagementSystem():
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dheena',
            database='customers_db'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS customer (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        phone VARCHAR(15),
                        email VARCHAR(100),
                        address VARCHAR(255)
                    );
                """)
        self.connection.commit()

    def add_customer(self):
        customer_name = input("Enter the customer name :")
        customer_phone = int(input("Enter the customer phome :"))
        customer_email = input("Enter the customer email :")
        customer_address = input("Enter the customer address :")
        self.cursor.execute("INSERT INTO Customer (name,phone,email,address) VALUES (%s,%s,%s,%s)",(customer_name,customer_phone,customer_email,customer_address,))
        self.connection.commit()
        print("The Customer added Successfully !")

    def view_customer(self):
        self.cursor.execute("SELECT * FROM customer")
        for row in self.cursor.fetchall():
            print("Id :",row[0],"Name :",row[1],"Phone :",row[2],"Email :",row[3],"Address :",row[4])

    def search_customer(self):
        search_cus = input("Enter name or email of the customer: ")
        self.cursor.execute("SELECT * FROM customer WHERE name=%s OR email=%s", (search_cus, search_cus,))
        results = self.cursor.fetchall()
        if results:
            for row in results:
                print("Id:", row[0], "Name:", row[1], "Phone:", row[2], "Email:", row[3], "Address:", row[4])
        else:
            print("No customer found!..")

    def update_customer(self):
        update_name = input("Enter the name of the customer to update: ")
        self.cursor.execute("SELECT * FROM customer WHERE name = %s", (update_name,))
        result = self.cursor.fetchall()

        if result:
            new_customer_name = input("Enter the new customer name: ")
            new_customer_phone = input("Enter the new customer phone: ")
            new_customer_email = input("Enter the new customer email: ")
            new_customer_address = input("Enter the new customer address: ")

            self.cursor.execute("""
                UPDATE customer SET name = %s, phone = %s, email = %s, address = %s WHERE name = %s """, (new_customer_name, new_customer_phone, new_customer_email, new_customer_address, update_name))

            self.connection.commit()
            print("Customer Record Updated Successfully!")
        else:
            print("No customer found with that email.")

    def delete_customer(self):
        customer_name = input("Enter the name of the customer you want to delete :")
        self.cursor.execute("DELETE FROM customer WHERE name=%s",(customer_name,))
        self.connection.commit()
        print("Customer record delete successfully..!")


def main():
    fun = CustomerManagementSystem()
    while True:
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            fun.add_customer()
        elif choice == '2':
            fun.view_customer()
        elif choice == '3':
            fun.search_customer()
        elif choice == '4':
            fun.update_customer()
        elif choice == '5':
            fun.delete_customer()
        else:
            print("Invalid choice. Try again.")
            break

main()

