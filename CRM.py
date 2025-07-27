import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QTextEdit , QTableWidget ,QTableWidgetItem
)

# ---------------------- Main CRM Application -------------------------

class CRMApplication(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------- SQL Connection ----------------

        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dheena',
            database='customers_db'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS crelation(
                name VARCHAR(20),
                email VARCHAR(50),
                phone VARCHAR(20),
                address VARCHAR(100)
            )
        """)
        self.connection.commit()

        # ---------------- GUI Setup ---------------------


        self.setWindowTitle("Customer Relationship Management")
        self.setGeometry(200, 200, 300, 300)

        # ----------------------- Buttons -------------------------

        self.add_button = QPushButton("Add Customer")
        self.view_button = QPushButton("View Customers")
        self.search_button = QPushButton("Search Customers")
        self.update_button = QPushButton("Update Customers")
        self.delete_button = QPushButton("Delete Customers")

        # -------------------------- Label ------------------------


        self.message_label = QLabel("Choose an option:")

        # ---------------------------- Layout -----------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.add_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

        # --------------------------- Button connections ------------------

        self.add_button.clicked.connect(self.open_add_btn)
        self.view_button.clicked.connect(self.open_view_btn)
        self.search_button.clicked.connect(self.open_search_btn)
        self.update_button.clicked.connect(self.open_update_btn)
        self.delete_button.clicked.connect(self.open_delete_btn)


    def open_add_btn(self):
        self.add_window = AddCustomerWindow(self.connection, self.cursor)
        self.add_window.show()

    def open_view_btn(self):
        self.view_window = ViewCustomerWindow(self.connection, self.cursor)
        self.view_window.show()

    def open_search_btn(self):
        self.search_window = SearchCustomerWindow(self.connection, self.cursor)
        self.search_window.show()

    def open_update_btn(self):
        self.update_window = UpdateCustomerWindow(self.connection, self.cursor)
        self.update_window.show()

    def open_delete_btn(self):
        self.delete_window = DeleteCustomerWindow(self.connection, self.cursor)
        self.delete_window.show()


# -------------------- Add Customer Window ----------------------

class AddCustomerWindow(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.setWindowTitle("Add Customer")
        self.connection = connection
        self.cursor = cursor

        # --------------------- Inputs -------------------------

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()

        # --------------------- Labels  -------------------

        self.name_label = QLabel("Enter your name:")
        self.email_label = QLabel("Enter your email:")
        self.phone_label = QLabel("Enter your phone number:")
        self.address_label = QLabel("Enter your address:")

        # ------------------------------ Add Button ----------------------

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_cus)

        # ------------------------------ Layout -------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    # --------------------- button handling ---------------------------

    def add_cus(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()

        if not name or not email or not phone or not address:
            QMessageBox.warning(self, "Warning","Please fill in all fields.")
            return

        self.cursor.execute(
            "INSERT INTO crelation (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (name, email, phone, address)
        )
        self.connection.commit()
        QMessageBox.information(self,"Successful", "Customer added successfully!")
        self.close()


# ------------------ View Customer Windows ----------------------

class ViewCustomerWindow(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.setWindowTitle("View Customers")
        self.connection = connection
        self.cursor = cursor

        # ----------------- Table widget creation --------------------

        self.table_creation = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.table_creation)
        self.setLayout(layout)
        self.view_cus()


    def view_cus(self):
        self.cursor.execute("SELECT * FROM crelation")
        rows = self.cursor.fetchall()
        self.table_creation.setRowCount(len(rows))
        self.table_creation.setColumnCount(4)
        self.table_creation.setHorizontalHeaderLabels(["Name", "Phone", "Email", "Address"])
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.table_creation.setItem(i, j, QTableWidgetItem(str(col)))


# ------------------ Search Customer Windows ----------------------


class SearchCustomerWindow(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.setWindowTitle("Search Customers")
        self.connection = connection
        self.cursor = cursor

        # ---------------------- Label ---------------------

        self.search_label = QLabel("Enter the customer name you want to search:")

        # ---------------------- Input ---------------------

        self.search_input = QLineEdit()

        # --------------------- Button ---------------------

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_cus)

        # --------------------- Results Box ---------------------

        self.final_result = QTextEdit()
        self.final_result.setReadOnly(False)

        # -------------------- Layout ---------------------

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.final_result)
        self.setLayout(layout)

    def search_cus(self):
        name = self.search_input.text()

        if not name:
            QMessageBox.warning(self,"Warning" ,"Please enter the customer name.")
            return

        query = "SELECT name, phone, email, address FROM crelation WHERE name LIKE %s"
        self.cursor.execute(query,(name,))
        results = self.cursor.fetchall()

        if not results:
            QMessageBox.warning(self, "Warning ","No customer found!")
            return

        # --------------------- Final Results ---------------------

        customer_info = ""
        for row in results:
            customer_info = (
                f"Name: {row[0]}\n"
                f"Phone: {row[1]}\n"
                f"Email: {row[2]}\n"
                f"Address: {row[3]}\n"
            )

        self.final_result.setText(customer_info)


# ------------------ Update Customer Windows ----------------------

class UpdateCustomerWindow(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.setWindowTitle("Update Customers")
        self.connection = connection
        self.cursor = cursor

        # ---------------- label ---------------------------

        self.topic = QLabel("Enter the customer name you want to update")
        self.prev_name = QLabel("Enter the prev name :")
        self.new_cus_name = QLabel("Enter the name :")
        self.new_cus_phone = QLabel("Enter the number :")
        self.new_cus_email = QLabel("Enter the email :")
        self.new_cus_address = QLabel("Enter the address :")

        # ---------------- input -------------------------------

        self.prev_input_name = QLineEdit()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        # ---------------- button ------------------------

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_cus)

        # ---------------- layout -------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.prev_name)
        layout.addWidget(self.prev_input_name)
        layout.addWidget(self.new_cus_name)
        layout.addWidget(self.name_input)
        layout.addWidget(self.new_cus_phone)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.new_cus_email)
        layout.addWidget(self.email_input)
        layout.addWidget(self.new_cus_address)
        layout.addWidget(self.address_input)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def update_cus(self):
        previous_name = self.prev_input_name.text()
        new_name = self.name_input.text()
        new_phone = self.phone_input.text()
        new_email = self.email_input.text()
        new_address = self.address_input.text()

        if not previous_name:
            QMessageBox.warning(self, "Warning","Please enter the previous customer name.")
            return

        self.cursor.execute(
            "SELECT name, phone, email, address FROM crelation WHERE name = %s",
            (previous_name,)
        )
        existing = self.cursor.fetchone()

        if not existing:
            QMessageBox.information(self, "Warning","No customer found with that name.")
            return

        updated_name = new_name or existing[0]
        updated_phone = new_phone or existing[1]
        updated_email = new_email or existing[2]
        updated_address = new_address or existing[3]

        query = """
            UPDATE crelation
            SET name = %s, phone = %s, email = %s, address = %s
            WHERE name = %s
        """
        values = (updated_name, updated_phone, updated_email, updated_address, previous_name)
        self.cursor.execute(query, values)
        self.connection.commit()

        if self.cursor.rowcount == 0:
            QMessageBox.warning(self, "Warning","Customer data was already up-to-date.")
        else:
            QMessageBox.information(self, "Successful","Customer updated successfully.")
            self.prev_input_name.clear()
            self.name_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.address_input.clear()


# ------------------ Delete Customer Windows ----------------------

class DeleteCustomerWindow(QWidget):
    def __init__(self, connection, cursor):
        super().__init__()
        self.setWindowTitle("Delete Customers")
        self.connection = connection
        self.cursor = cursor

        # ------------------ label -------------------------------

        self.delete_name = QLabel("Enter the customer name you want to delete:")

        # -------------------- input -------------------------------------

        self.delete_input = QLineEdit()

        # -------------------- button -----------------------------------

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_cus)

        # ----------------------- Layout --------------------------------

        layout = QVBoxLayout()
        layout.addWidget(self.delete_name)
        layout.addWidget(self.delete_input)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

    # ------------------- button handler -----------------------------

    def delete_cus(self):
        name = self.delete_input.text()

        if not name:
            QMessageBox.warning(self,"Warning", "Please enter a customer name.")
            return

        self.cursor.execute("SELECT * FROM crelation WHERE name = %s", (name,))
        result = self.cursor.fetchone()

        if not result:
            QMessageBox.information(self,"Warning", "No customer found with that name.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM crelation WHERE name = %s", (name,))
            self.connection.commit()
            QMessageBox.information(self, "Successful ","Customer deleted successfully.")
            self.delete_input.clear()
        else:
            QMessageBox.information(self, "Warning","Customer was not deleted.")


# ---------------------- Run Application -------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRMApplication()
    window.show()
    sys.exit(app.exec_())

