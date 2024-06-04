import dateparser
import re
import arrow
from datetime import datetime
import qrcode
import mysql.connector

class BeautyProduct:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT * FROM BeautyProducts")
        products = []
        for row in cursor.fetchall():
            id, name, price = row
            products.append(cls(id, name, price))
        return products

    @classmethod
    def add_product(cls, cursor, name, price):
        query = "INSERT INTO BeautyProducts (name, price) VALUES (%s, %s)"
        cursor.execute(query, (name, price))
        return cursor.lastrowid

    @classmethod
    def update_product(cls, cursor, product_id, name=None, price=None):
        query = "UPDATE BeautyProducts SET "
        values = []

        if name:
            query += "name = %s, "
            values.append(name)

        if price:
            query += "price = %s, "
            values.append(price)

        query = query.rstrip(", ") + " WHERE id = %s"
        values.append(product_id)

        cursor.execute(query, values)

    @classmethod
    def delete_product(cls, cursor, product_id):
        query = "DELETE FROM BeautyProducts WHERE id = %s"
        cursor.execute(query, (product_id,))

class Haircare(BeautyProduct):
    def __init__(self, id, name, price, hair_type):
        super().__init__(id, name, price)
        self.hair_type = hair_type

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT bp.id, bp.name, bp.price, h.hair_type FROM BeautyProducts bp JOIN Haircare h ON bp.id = h.product_id")
        products = []
        for row in cursor.fetchall():
            id, name, price, hair_type = row
            products.append(cls(id, name, price, hair_type))
        return products

    @classmethod
    def add_product(cls, cursor, name, price, hair_type):
        product_id = BeautyProduct.add_product(cursor, name, price)
        query = "INSERT INTO Haircare (product_id, hair_type) VALUES (%s, %s)"
        cursor.execute(query, (product_id, hair_type))
        return product_id

    @classmethod
    def update_product(cls, cursor, product_id, name=None, price=None, hair_type=None):
        BeautyProduct.update_product(cursor, product_id, name, price)
        if hair_type:
            query = "UPDATE Haircare SET hair_type = %s WHERE product_id = %s"
            cursor.execute(query, (hair_type, product_id))

    @classmethod
    def delete_product(cls, cursor, product_id):
        query = "DELETE FROM Haircare WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        BeautyProduct.delete_product(cursor, product_id)
        

class Skincare(BeautyProduct):
    def __init__(self, id, name, price, skin_type):
        super().__init__(id, name, price)
        self.skin_type = skin_type

    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT bp.id, bp.name, bp.price, s.skin_type FROM BeautyProducts bp JOIN Skincare s ON bp.id = s.product_id")
        products = []
        for row in cursor.fetchall():
            id, name, price, skin_type = row
            products.append(cls(id, name, price, skin_type))
        return products

    @classmethod
    def add_product(cls, cursor, name, price, skin_type):
        product_id = BeautyProduct.add_product(cursor, name, price)
        query = "INSERT INTO Skincare (product_id, skin_type) VALUES (%s, %s)"
        cursor.execute(query, (product_id, skin_type))
        return product_id

    @classmethod
    def update_product(cls, cursor, product_id, name=None, price=None, skin_type=None):
        BeautyProduct.update_product(cursor, product_id, name, price)
        if skin_type:
            query = "UPDATE Skincare SET skin_type = %s WHERE product_id = %s"
            cursor.execute(query, (skin_type, product_id))

    @classmethod
    def delete_product(cls, cursor, product_id):
        query = "DELETE FROM Skincare WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        BeautyProduct.delete_product(cursor, product_id)
        

class Treatment:
    def __init__(self, id, name, description, duration, price):
        self.id = id
        self.name = name
        self.description = description
        self.duration = duration
        self.price = price
    
    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT id, name, description, duration, price FROM Treatments")
        Treatment = []
        for row in cursor.fetchall():
            id, name, description, duration, price = row
            Treatment.append(cls(id, name, description,duration, price))
        return Treatment
    @classmethod
    def add_treatment(cls, cursor, name, description, duration, price):
        query = "INSERT INTO Treatments (name, description, duration, price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, description, duration, price))

    @classmethod
    def update_treatment(cls, cursor, treatment_id, name, description, duration, price):
        query = "UPDATE Treatments SET name=%s, description=%s, duration=%s, price=%s WHERE id=%s"
        cursor.execute(query, (name, description, duration, price, treatment_id))

    @classmethod
    def delete_treatment(cls, cursor, treatment_id):
        query = "DELETE FROM Treatments WHERE id=%s"
        cursor.execute(query, (treatment_id,))

class Doctor:
    def __init__(self, id, name, specialties):
        self.id = id
        self.name = name
        self.specialties = specialties

    
    @classmethod
    def get_all(cls, cursor):
        cursor.execute("SELECT id, name, specialties FROM Doctors")
        Doctor = []
        for row in cursor.fetchall():
            id, name, specialties= row
            Doctor.append(cls(id, name, specialties))
        return Doctor

    @classmethod
    def add_doctor(cls, cursor, name, specialties):
        query = "INSERT INTO Doctors (name, specialties) VALUES (%s, %s)"
        cursor.execute(query, (name, ','.join(specialties)))

    @classmethod
    def update_doctor(cls, cursor, doctor_id, name, specialties):
        query = "UPDATE Doctors SET name=%s, specialties=%s WHERE id=%s"
        cursor.execute(query, (name, ','.join(specialties), doctor_id))

    @classmethod
    def delete_doctor(cls, cursor, doctor_id):
        checkquery = "SELECT COUNT(*) FROM Schedules WHERE doctor_id=%s"
        cursor.execute(checkquery, (doctor_id,))
        result = cursor.fetchone()
        num_schedules = result[0]

        if num_schedules > 0:
            print("This doctor has schedules associated with them. You cannot delete the doctor.")
        else:
            query = "DELETE FROM Doctors WHERE id=%s"
            cursor.execute(query, (doctor_id,))

    @classmethod
    def add_doctor_schedule(cls, cursor, doctor_id, date, duration):
        query = "INSERT INTO Schedules (doctor_id, date, duration) VALUES (%s, %s, %s)"
        cursor.execute(query, (doctor_id, date, duration))

class Schedule:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def view_doctor_schedules(self, doctor_id=None):
        self.cursor.execute("SELECT s.id, d.name, s.date, s.duration FROM Schedules s JOIN Doctors d ON s.doctor_id = d.id WHERE s.id NOT IN (SELECT schedule_id FROM Appointments)")
        schedules = self.cursor.fetchall()
        if not schedules:
            print("No doctor schedules available.")
        else:
            print("\nDoctor Schedules:")
            print("{:<5} {:<20} {:<25} {:<10}".format("ID", "Doctor Name", "Date and Time", "Duration"))
            print("-" * 65)
            for schedule in schedules:
                date_time_str = schedule[2].strftime("%Y-%m-%d %H:%M:%S")  # Include time component
                print("{:<5} {:<20} {:<25} {:<10}".format(schedule[0], schedule[1], date_time_str, f"{schedule[3]} minutes"))

    def delete_doctor_schedules(self):
        try:
            schedule_id = int(input("Enter the ID of the schedule to delete: "))
            confirm = input(f"Are you sure you want to delete the schedule? (yes/no): ").lower()
            if confirm == "yes":
                self.cursor.execute("DELETE FROM Schedules WHERE id=%s", (schedule_id,))
                self.db.commit()
                print("Schedule deleted successfully.")
            else:
                print("Deletion canceled.")
        except ValueError:
            print("Invalid ID. Please enter a valid integer.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @classmethod
    def add_doctor_schedule(cls, cursor, doctor_id, date, duration):
        query = "INSERT INTO Schedules (doctor_id, date, duration) VALUES (%s, %s, %s)"
        cursor.execute(query, (doctor_id, date, duration))

    @classmethod
    def update_doctor_schedule(cls, cursor, schedule_id, doctor_id=None, date=None, duration=None):
        query = "UPDATE Schedules SET "
        values = []

        if doctor_id is not None:
            query += "doctor_id = %s, "
            values.append(doctor_id)

        if date is not None:
            query += "date = %s, "
            values.append(date)

        if duration is not None:
            query += "duration = %s, "
            values.append(duration)

        query = query.rstrip(", ") + " WHERE id = %s"
        values.append(schedule_id)

        cursor.execute(query, values)
class Appointment:
    def __init__(self,id, user, doctor, schedule):
        self.id = id
        self.user = user
        self.doctor = doctor
        self.schedule = schedule


    def book_appointment(self, user_id, doctor_id, schedule_id):
        query = "INSERT INTO Appointments (user_id, doctor_id, schedule_id) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user_id, doctor_id, schedule_id))
        self.db.commit()

    @classmethod
    def get_all(cls, cursor, user_id=None):
        query = "SELECT Appointments.id, Users.username, Doctors.name, Schedules.date FROM Appointments JOIN Users ON Appointments.user_id = Users.id JOIN Doctors ON Appointments.doctor_id = Doctors.id JOIN Schedules ON Appointments.schedule_id = Schedules.id WHERE Appointments.user_id = %s"

        cursor.execute(query, (user_id,))
        appointments = []
        for row in cursor.fetchall():
            id, user, doctor, schedule = row
            datetime_str = schedule.strftime("%Y-%m-%d %H:%M:%S")
            appointments.append(cls(id, user, doctor, datetime_str))
        return appointments
    
    @classmethod
    def delete_appointment(self, cursor, appointment_id):
        query = "DELETE FROM Appointments WHERE id=%s"
        cursor.execute(query, (appointment_id,))
    

class Cart:
    def __init__(self, cursor, user, db):
        self.cursor = cursor
        self.user = user
        self.db = db
        self.items = []

    def load_cart_items(self):
        self.items.clear()
        if self.user.cart_id:
            query = """
                SELECT bp.id, bp.name, bp.price, ci.quantity, h.hair_type, s.skin_type
                FROM CartItems ci
                JOIN BeautyProducts bp ON ci.product_id = bp.id
                LEFT JOIN Haircare h ON bp.id = h.product_id
                LEFT JOIN Skincare s ON bp.id = s.product_id
                WHERE ci.cart_id = %s
            """
            self.cursor.execute(query, (self.user.cart_id,))
            for row in self.cursor.fetchall():
                product_id, name, price, quantity, hair_type, skin_type = row
                category = "Haircare" if hair_type else "Skincare" if skin_type else None
                if category == "Haircare":
                    product = Haircare(product_id, name, price, hair_type)
                elif category == "Skincare":
                    product = Skincare(product_id, name, price, skin_type)
                else:
                    product = BeautyProduct(product_id, name, price)
                self.items.append(CartItem(product, quantity))
    
    def display_cart(self):
        if not self.items:
            print("\nShopping cart is empty.")
        else:
            print("\nCart:")
            print("=" * 30)
            for i, item in enumerate(self.items, start=1):
                print(f"{i}. {item.quantity} x {item.product.name} - ${item.product.price}")
                if isinstance(item.product, Haircare):
                    print(f"Hair Type: {item.product.hair_type}")
                elif isinstance(item.product, Skincare):
                    print(f"Skin Type: {item.product.skin_type}")
            print("=" * 30)
            print()

    def add_item(self, product_id, quantity):
        self.cursor.execute(f"SELECT * FROM BeautyProducts WHERE id = {product_id}")
        product_data = self.cursor.fetchone()

        if product_data:
            id, name, price = product_data
            product = BeautyProduct(id, name, price)

            self.cursor.execute(f"SELECT hair_type FROM Haircare WHERE product_id = {product_id}")
            hair_type = self.cursor.fetchone()
            if hair_type:
                product = Haircare(id, name, price, hair_type[0])

            self.cursor.execute(f"SELECT skin_type FROM Skincare WHERE product_id = {product_id}")
            skin_type = self.cursor.fetchone()
            if skin_type:
                product = Skincare(id, name, price, skin_type[0])

            # Check if the product is already in the cart
            existing_item = next((item for item in self.items if item.product.id == product.id), None)
            if existing_item:
                # Update the quantity of the existing item
                existing_item.quantity += quantity
                self.update_cart_item(existing_item.product.id, existing_item.quantity)
            else:
                # Add the new item to the cart
                self.add_cart_item(product.id, quantity)
        else:
            print(f"Product with ID {product_id} not found.")

    def add_cart_item(self, product_id, quantity):
        if not self.user.cart_id:
            self.user.create_cart()

        query = "INSERT INTO CartItems (cart_id, product_id, quantity) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (self.user.cart_id, product_id, quantity))
        self.db.commit()

    def update_cart_item(self, product_id, quantity):
        if self.user.cart_id:
            query = "UPDATE CartItems SET quantity = %s WHERE cart_id = %s AND product_id = %s"
            self.cursor.execute(query, (quantity, self.user.cart_id, product_id))
            self.db.commit()

    def remove_item(self, index):
        if 1 <= index <= len(self.items):
            removed_item = self.items.pop(index - 1)
            print("item has been removed from the cart.")

            if self.user.cart_id:
                query = "DELETE FROM CartItems WHERE cart_id = %s AND product_id = %s"
                self.cursor.execute(query, (self.user.cart_id, removed_item.product.id))
                self.db.commit()
        else:
            print("Please select a valid item number.")

    def clear_cart(self):
        self.items.clear()
        if self.user.cart_id:
            query = "DELETE FROM CartItems WHERE cart_id = %s"
            self.cursor.execute(query, (self.user.cart_id,))
            self.db.commit()

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items)
        total_qty = sum(item.quantity for item in self.items)
        final_total = total
        print()
        print(f"Total: ${total}")
        print(f"Final Total: ${final_total:.2f}")
        print()
        return final_total

    def generate_receipt(self, total_amount):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt = []
        receipt.append("===== Transaction Receipt =====")
        receipt.append(f"Date: {current_time}")
        receipt.append(f"Customer: {self.user.username}")
        receipt.append("\nItems Purchased:")
        for item in self.items:
            product_details = f"{item.quantity} x {item.product.name} - ${item.product.price * item.quantity:.2f}"
            if isinstance(item.product, Haircare):
                product_details += f" (Hair Type: {item.product.hair_type})"
            elif isinstance(item.product, Skincare):
                product_details += f" (Skin Type: {item.product.skin_type})"
            receipt.append(product_details)
        receipt.append("\nTotal Amount: ${:.2f}".format(total_amount))
        receipt.append("==============================")
        receipt = "\n".join(receipt)
        print(receipt)

    def generate_qr_code(self, total_amount):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Total amount to pay: ${total_amount:.2f}")
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.show()

    def checkout(self):
        if not self.items:
            print("\nShopping cart is empty.")
        else:
            print()
            print("Transaction Details:")
            total_amount = self.calculate_total()
            confirm = input("Are you sure you want to checkout? (y/n) ").lower()
            if confirm == "y":
                self.generate_qr_code(total_amount)
                self.generate_receipt(total_amount)
                self.items.clear()
                self.clear_cart()
                print("Shopping cart has been cleared.")
                print()
                print("Thank you for shopping!")
            else:
                print("Checkout canceled.")

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity

    def _str_(self):
        return f"Quantity: {self.quantity} {self.product.name} x ${self.product.price}"

class BeautyCatalog:
    def __init__(self, cursor):
        self.cursor = cursor
        self.haircare_products = Haircare.get_all(self.cursor)
        self.skincare_products = Skincare.get_all(self.cursor)

    def display_catalog(self, cart):
        print("\nBeauty Products Catalog:")
        print("=" * 30)
        print("Haircare Products:")
        for product in self.haircare_products:
            print(f"{product.id}. {product.name} - ${product.price} ({product.hair_type})")
        print("\nSkincare Products:")
        for product in self.skincare_products:
            print(f"{product.id}. {product.name} - ${product.price} ({product.skin_type})")
        print("=" * 30)
        self.catalog_menu(cart)


    def catalog_menu(self, cart):
        while True:
            choice = input("\nEnter the product ID to add to the cart (or 'q' to quit): ").lower()
            if choice == "q":
                break
            elif choice.isdigit():
                product_id = int(choice)
                quantity = int(input("Enter the quantity: "))
                cart.add_item(product_id, quantity)
            else:
                print("Invalid choice. Please try again.")

class Admin:
    def __init__(self, cursor, db, username=None, password=None):
        self.cursor = cursor
        self.db = db
        self.username = username
        self.password = password
        self.id = None

    def authenticate(self, username, password):
        query = "SELECT id FROM Admins WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            self.id = result[0]
            self.username = username
            self.password = password
            return True
        return False
        

class User:
    def __init__(self, cursor, db, username=None, password=None):
        self.cursor = cursor
        self.db = db
        self.username = username
        self.password = password
        self.id = None
        self.cart_id = None
        self.appointment_id = None

    def authenticate(self, username, password):
        query = "SELECT id, cart_id, appointment_id FROM Users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            self.id, self.cart_id, self.appointment_id = result
            self.username = username
            self.password = password
            return True
        return False

    def create_user(self, username, password):
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.id = self.cursor.lastrowid
        self.username = username
        self.password = password
        self.cart_id = None
        self.appointment_id = None
        self.db.commit()

    def create_cart(self):
        query = "INSERT INTO Carts (user_id) VALUES (%s)"
        self.cursor.execute(query, (self.id,))
        self.cart_id = self.cursor.lastrowid
        self.db.commit()

        query = "UPDATE Users SET cart_id = %s WHERE id = %s"
        self.cursor.execute(query, (self.cart_id, self.id))
        self.db.commit()

class BeautyClinic:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clinic"
        )
        self.cursor = self.db.cursor()
        self.admin = None
        self.user = None
        self.catalog = None
        self.cart = None

    def get_treatments(self):
        return Treatment.get_all(self.cursor)

    def get_doctors(self):
        return Doctor.get_all(self.cursor)

    def get_haircare_products(self):
        return Haircare.get_all(self.cursor)

    def get_skincare_products(self):
        return Skincare.get_all(self.cursor)

    def add_treatment(self, name, description, duration, price):
        Treatment.add_treatment(self.cursor, name, description, duration,price)

    def add_doctor(self, name, specialties):
        Doctor.add_doctor(self.cursor, name, specialties)

    def add_haircare_product(self, name, price, hair_type):
        Haircare.add_product(self.cursor, name, price, hair_type)

    def add_skincare_product(self, name, price, skin_type):
        Skincare.add_product(self.cursor, name, price, skin_type)

    def add_appointment(self, user_id, doctor_id, schedule_id):
        appointment = Appointment(None, None, None, None)
        appointment.cursor = self.cursor
        appointment.db = self.db
        appointment.book_appointment(user_id, doctor_id, schedule_id)
    
    def delete_appointment(self, appointment_id):
        appointment = Appointment(None, None, None, None)
        appointment.cursor = self.cursor
        appointment.db = self.db
        appointment.delete_appointment(self.cursor, appointment_id)


    
    def loginUser(self):
        print("===== User Login =====")
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = User(self.cursor, self.db)
        if user.authenticate(username, password):
            print("Login successful!")
            self.user = user
            self.catalog = BeautyCatalog(self.cursor)
            self.cart = Cart(self.cursor, self.user, self.db)
            self.user_menu()
        else:
            print("Invalid credentials. Please try again.")
            

    def loginAdmin(self):
        print("===== Admin Login =====")
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        admin = Admin(self.cursor, self.db)
        if admin.authenticate(username, password):
            print("Admin login successful!")
            self.admin = admin
            self.admin_menu()
        else:
            print("Invalid admin credentials. Please try again.")

    def register(self):
        print("===== User Registration =====")
        while True:
            username = input("Enter a username: ")
            if username:
                break
            else:
                print("Username cannot be empty. Please try again.")
        while True:
            password = input("Enter a password: ")
            if password:
                break
            else:
                print("Password cannot be empty. Please try again.")

        user = User(self.cursor, self.db)
        if not user.authenticate(username, password):
            user.create_user(username, password)
            print("Registration successful!")
            self.user = user
            self.catalog = BeautyCatalog(self.cursor)
            self.cart = Cart(self.cursor, self.user, self.db)
            self.user_menu()
        else:
            print("Username already exists. Please choose a different one.")
            self.register()
    
    def user_menu(self):
        while True:
            print("\nUser Menu:")
            print("1. Beauty Product Shop")
            print("2. Beauty Treatment Appointment")
            print("0. Logout")
            choice = input("Enter your choice (0-2): ")

            if choice == "1":
                self.user_shop_menu()
            elif choice == "2":
                self.user_appointment_menu()
            elif choice == "0":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def user_appointment_menu(self):
        while True:
            print("\nAppointment Menu:")
            print("1. View Treatments")
            print("2. View Doctors")
            print("3. View Doctor Schedules")
            print("4. Book Appointment")
            print("5. View Appointments")
            print("6. Cancel Appointment")
            print("0. Back to User Menu")
            choice = input("Enter your choice (0-5): ")

            if choice == "1":
                self.view_treatments()
            elif choice == "2":
                self.view_doctors()
            elif choice == "3":
                self.view_doctor_schedules()
            elif choice == "4":
                self.book_appointment_menu()
            elif choice == "5":
                self.view_appointments()
            elif choice == "6":
                self.cancel_appointment_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def book_appointment_menu(self):
        user_id = self.user.id
        self.view_doctor_schedules()
        while True:
            try:
                schedule_id = int(input("Enter the ID of the appointment schedule: "))
                self.cursor.execute("SELECT doctor_id FROM Schedules WHERE id = %s", (schedule_id,))
                result = self.cursor.fetchone()
                if result:
                    doctor_id = result[0]
                    break
                else:
                    print("Invalid schedule ID.")
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
            
        self.add_appointment(user_id, doctor_id, schedule_id)
        self.db.commit()
    
    def cancel_appointment_menu(self):
        self.view_appointments()
        while True:
            try:
                appointment_id = int(input("Enter the ID of the appointment to cancel: "))
                break
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
        confirm = input(f"Are you sure you want to cancel the appointment? (yes/no): ").lower()
        if confirm == "yes":
            self.delete_appointment(appointment_id)
            self.db.commit()
            print("Appointment canceled successfully.")
        elif confirm == "no":
            print("Cancellation canceled.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    def view_appointments(self):
        appointments = Appointment.get_all(self.cursor, self.user.id)
        if not appointments:
            print("No appointments available.")
        else:
            print("\nAppointments:")
            print("{:<20} {:<20} {:<20} {:<25}".format("ID", "User", "Doctor", "Date and Time"))
            print("-" * 75)
            for appointment in appointments:
                print("{:<20} {:<20} {:<20} {:<25}".format(appointment.id,appointment.user, appointment.doctor, appointment.schedule))

    
    def manage_treatments(self):
        while True:
            print("\nTreatments Menu:")
            print("1. Add Treatment")
            print("2. Update Treatment")
            print("3. View Treatments")
            print("4. Delete Treatment")
            print("0. Back to Admin Menu")
            choice = input("Enter your choice (0-4): ")

            if choice == "1":
                self.add_treatment_menu()
            elif choice == "2":
                self.update_treatment_menu()
            elif choice == "3":
                self.view_treatments()
            elif choice == "4":
                self.delete_treatment_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_treatment_menu(self):
        while True:
            try:
                name = input("Enter treatment name: ")
                if not name or not name.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)
        
        while True:
            try:
                description = input("Enter treatment description: ")
                if not description or not description.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)

        while True:
            duration_input = input("Enter treatment duration (in minutes): ")
            if duration_input.isdigit():  
                duration = int(duration_input)
                if duration <= 0:
                    print("Duration must be a positive integer.")
                else:
                    break  
            else:
                print("Please enter a valid positive integer for duration.")
        while True:
            price_input = input("Enter treatment price: ")
            if price_input.replace('.', '', 1).isdigit():  
                price = float(price_input)
                if price <= 0:
                    print("Price must be a positive number.")
                else:
                    break  
            else:
                print("Please enter a valid positive number for price.")
        self.add_treatment(name, description, duration, price)
        self.db.commit()
        print("Treatment added successfully.")

    def update_treatment_menu(self):
        try:
            self.view_treatments()  # Assuming this method displays the treatments
            treatment_id = int(input("Enter the ID of the treatment to update: "))
            
            # Input validation for name
            while True:
                name = input("Enter new treatment name: ")
                if name.replace(' ', '').isalpha():
                    break  # Break the loop if the name is valid
                else:
                    print("Please enter alphabetic characters only.")

            # Input validation for description
            while True:
                description = input("Enter new treatment description: ")
                if description.replace(' ', '').isalpha():
                    break  # Break the loop if the name is valid
                else:
                    print("Please enter alphabetic characters only.")

            # Input validation for duration
            while True:
                try:
                    duration_input = input("Enter new treatment duration (in minutes): ")
                    duration = int(duration_input)
                    if duration <= 0:
                        print("Duration must be a positive integer.")
                    else:
                        break  # Break the loop if the duration is valid
                except ValueError:
                    print("Please enter a valid positive integer for duration.")

            # Input validation for price
            while True:
                try:
                    price_input = input("Enter treatment price: ")
                    price = float(price_input)
                    if price <= 0:
                        print("Price must be a positive number.")
                    else:
                        break  # Break the loop if the price is valid
                except ValueError:
                    print("Please enter a valid positive number for price.")

            Treatment.update_treatment(self.cursor, treatment_id, name, description, duration, price)
            self.db.commit()
            print("Treatment updated successfully.")
        except ValueError as ve:
            print("Error:", ve)
        except Exception as e:
            print("An unexpected error occurred:", e)

    def view_treatments(self):
        treatments = self.get_treatments()
        if not treatments:
            print("No treatments available.")
        else:
            print("\nTreatments:")
            print("{:<5} {:<20} {:<50} {:<10} {:<10}".format("ID", "Name", "Description", "Duration", "Price"))
            print("-" * 115)
            for treatment in treatments:
                print("{:<5} {:<20} {:<50} {:<10} {:<10}".format(treatment.id, treatment.name, treatment.description, f"{treatment.duration} minutes", treatment.price))

    def delete_treatment_menu(self):
        self.view_treatments()
        while True:
            try:
                treatment_id = int(input("Enter the ID of the treatment to delete: "))
                break
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
        confirm = input(f"Are you sure you want to delete the treatment? (yes/no): ").lower()
        if confirm == "yes":
            Treatment.delete_treatment(self.cursor, treatment_id)
            self.db.commit()
            print("Treatment deleted successfully.")
        elif confirm == "no":
            print("Deletion canceled.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


    def user_shop_menu(self):
        while True:
            print("\nUser Menu:")
            print("1. Open Catalog")
            print("2. See Cart")
            print("3. Checkout")
            print("4. Back to User Menu")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.catalog.display_catalog(self.cart)
            elif choice == "2":
                self.cart.load_cart_items()
                self.display_cart()
                self.cart_menu()
            elif choice == "3":
                self.cart.checkout()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def logout(self):
        self.user = None
        self.catalog = None
        self.cart = None
        print("Logged out successfully.")
    

    def admin_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. Manage Beauty Product")
            print("2. Manage Treatments")
            print("3. Manage Doctors")
            print("4. Manage Doctor Schedules")
            print("0. Logout")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.manage_beauty_products()
            elif choice == "2":
                self.manage_treatments()
            elif choice == "3":
                self.manage_doctors()
            elif choice == "4":
                self.manage_doctor_schedules()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_doctors(self):
        while True:
            print("\nDoctors Menu:")
            print("1. Add Doctor")
            print("2. Update Doctor")
            print("3. View Doctors")
            print("4. Delete Doctor")
            print("0. Back to Admin Menu")
            choice = input("Enter your choice (0-4): ")

            if choice == "1":
                self.add_doctor_menu()
            elif choice == "2":
                self.update_doctor_menu()
            elif choice == "3":
                self.view_doctors()
            elif choice == "4":
                self.delete_doctor_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_doctor_menu(self):
        while True:
            try:
                name = input("Enter doctor name: ")
                if not name or not name.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)

        while True:
            try:
                specialties_input = input("Enter doctor specialties (comma separated): ")
                specialties = [specialty.strip() for specialty in specialties_input.split(',')]
                if not specialties or not all(specialty.isalpha() for specialty in specialties):
                    raise ValueError("Please enter alphabetic characters only for specialties.")
                break  
            except ValueError as ve:
                print(ve)
        self.add_doctor(name, specialties)
        self.db.commit()
        print("Doctor added successfully.")

    def update_doctor_menu(self):
        try:
            self.view_doctors()
            doctor_id = int(input("Enter the ID of the doctor to update: "))
            
            while True:
                name = input("Enter new doctor name: ")
                if not name or not name.replace(' ', '').isalpha():
                    print("Please enter alphabetic characters only for name.")
                else:
                    break  # Break the loop if the name is valid
            
            while True:
                try:
                    specialties_input = input("Enter new doctor specialties (comma separated): ")
                    specialties = [specialty.strip() for specialty in specialties_input.split(',')]
                    if not specialties or not all(specialty.isalpha() for specialty in specialties):
                        raise ValueError("Please enter alphabetic characters only for specialties.")
                    break  
                except ValueError as ve:
                    print(ve)

            
            Doctor.update_doctor(self.cursor, doctor_id, name, specialties)
            self.db.commit()
            print("Doctor updated successfully.")
        except ValueError as ve:
            print("Error:", ve)
        except Exception as e:
            print("An unexpected error occurred:", e)

    def view_doctors(self):
        doctors = self.get_doctors()
        if not doctors:
            print("No doctors available.")
        else:
            print("\nDoctors:")
            print("{:<5} {:<20} {:<50}".format("ID", "Name", "Specialties"))
            print("-" * 75)
            for doctor in doctors:
                print("{:<5} {:<20} {:<50}".format(doctor.id, doctor.name, doctor.specialties))

    def delete_doctor_menu(self):
        self.view_doctors()
        while True:
            try:
                doctor_id = int(input("Enter the ID of the doctor to delete: "))
                break
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
        confirm = input(f"Are you sure you want to delete the doctor? (yes/no): ").lower()
        if confirm == "yes":
            Doctor.delete_doctor(self.cursor, doctor_id)
            self.db.commit()
            print("Doctor deleted successfully.")
        elif confirm == "no":
            print("Deletion canceled.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    def manage_beauty_products(self):
        while True:
            print("\nBeauty Products Menu:")
            print("1. Add Haircare Product")
            print("2. Add Skincare Product")
            print("3. Update Beauty Product")
            print("4. View Beauty Products")
            print("5. Delete Beauty Product")
            print("0. Back to Admin Menu")
            choice = input("Enter your choice (0-5): ")

            if choice == "1":
                self.add_haircare_product_menu()
            elif choice == "2":
                self.add_skincare_product_menu()
            elif choice == "3":
                self.update_beauty_product_menu()
            elif choice == "4":
                self.view_beauty_products()
            elif choice == "5":
                self.delete_beauty_product_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_haircare_product_menu(self):
        while True:
            try:
                name = input("Enter product name: ")
                if not name or not name.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)

        while True:
            price_input = input("Enter product price: ")
            if price_input.replace('.', '', 1).isdigit():
                price = float(price_input)
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                break  # Break the loop if the price is valid
            else:
                print("Please enter a valid positive number for price.")
        
        while True:
            try:
                hair_type = input("Enter hair type: ")
                if not hair_type or not hair_type.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)
        self.add_haircare_product(name, price, hair_type)
        self.db.commit()
        print("Haircare product added successfully.")

    def add_skincare_product_menu(self):
        while True:
            try:
                name = input("Enter product name: ")
                if not name or not name.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)

        while True:
            price_input = input("Enter product price: ")
            if price_input.replace('.', '', 1).isdigit():
                price = float(price_input)
                if price <= 0:
                    raise ValueError("Price must be a positive number.")
                break  # Break the loop if the price is valid
            else:
                print("Please enter a valid positive number for price.")

        while True:
            try:
                skin_type = input("Enter skin type: ")
                if not skin_type or not skin_type.replace(' ', '').isalpha():
                    raise ValueError("Please enter alphabetic characters only.")
                break  
            except ValueError as ve:
                print(ve)
        self.add_skincare_product(name, price, skin_type)
        self.db.commit()
        print("Skincare product added successfully.")

    def update_beauty_product_menu(self):
        self.view_beauty_products()
        while True:
            try:
                product_id = int(input("Enter the ID of the product to update: "))
                break
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
                continue
        name = input("Enter new product name (leave blank to keep the current name): ")
        price = input("Enter new product price (leave blank to keep the current price): ")

        if not name:
            name = None
        else:
            name = name.strip()

        if not price:
            price = None
        else:
            try:
                price = float(price)
            except ValueError:
                print("Invalid price format. Please enter a valid number.")
                return

        category = input("Enter new product category (Haircare or Skincare, leave blank to keep the current category): ").lower()
        if category == "haircare":
            hair_type = input("Enter new hair type: ")
            Haircare.update_product(self.cursor, product_id, name, price, hair_type)
        elif category == "skincare":
            skin_type = input("Enter new skin type: ")
            Skincare.update_product(self.cursor, product_id, name, price, skin_type)
        else:
            BeautyProduct.update_product(self.cursor, product_id, name, price)

        self.db.commit()
        print("Product updated successfully.")

    def view_beauty_products(self):
        haircare_products = self.get_haircare_products()
        skincare_products = self.get_skincare_products()

        print("\nHaircare Products:")
        print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Name", "Price", "Hair Type"))
        print("-" * 45)
        for product in haircare_products:
            print("{:<5} {:<20} {:<10} {:<10}".format(product.id, product.name, product.price, product.hair_type))

        print("\nSkincare Products:")
        print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Name", "Price", "Skin Type"))
        print("-" * 45)
        for product in skincare_products:
            print("{:<5} {:<20} {:<10} {:<10}".format(product.id, product.name, product.price, product.skin_type))

    def delete_beauty_product_menu(self):
        self.view_beauty_products()
        while True:
            try:
                product_id = int(input("Enter the ID of the product to delete: "))
                break
            except ValueError:
                print("Invalid ID. Please enter a valid integer.")
        
        # Check if the product exists in the Haircare or Skincare tables
        is_haircare = self.is_product_in_haircare(product_id)
        is_skincare = self.is_product_in_skincare(product_id)
        
        if not is_haircare and not is_skincare:
            print("Product ID not found in Haircare or Skincare.")
            return

        confirm = input(f"Are you sure you want to delete the product? (yes/no): ").lower()
        if confirm == "yes":
            if is_haircare:
                Haircare.delete_product(self.cursor, product_id)
            if is_skincare:
                Skincare.delete_product(self.cursor, product_id)
            self.db.commit()
            print("Product deleted successfully.")
        elif confirm == "no":
            print("Deletion canceled.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
        
    def is_product_in_haircare(self, product_id):
        query = "SELECT COUNT(*) FROM Haircare WHERE product_id = %s"
        self.cursor.execute(query, (product_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def is_product_in_skincare(self, product_id):
        query = "SELECT COUNT(*) FROM Skincare WHERE product_id = %s"
        self.cursor.execute(query, (product_id,))
        result = self.cursor.fetchone()
        return result[0] > 0


    def manage_doctor_schedules(self):
        while True:
            print("\nDoctor Schedules Menu:")
            print("1. Add Doctor Schedule")
            print("2. Update Doctor Schedule")
            print("3. View Doctor Schedules")
            print("4. Delete Doctor Schedule")
            print("0. Back to Admin Menu")
            choice = input("Enter your choice (0-4): ")

            if choice == "1":
                self.add_doctor_schedule_menu()
            elif choice == "2":
                self.update_doctor_schedule_menu()
            elif choice == "3":
                self.view_doctor_schedules()
            elif choice == "4":
                self.delete_doctor_schedule_menu()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_doctor_schedule_menu(self):
        self.view_doctors()
        
        # Validate doctor ID
        while True:
            try:
                doctor_id = int(input("Enter doctor ID: "))
                if not self.is_valid_doctor_id(doctor_id):
                    raise ValueError("Doctor ID does not exist.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid doctor ID.")
        
        # Validate date
        while True:
            date = input("Enter schedule date (YYYY-MM-DD): ")
            if re.match(r"\d{4}-\d{2}-\d{2}", date):
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")
            else:
                print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
        
        # Validate time
        while True:
            time = input("Enter schedule time (HH:MM:SS): ")
            if re.match(r"\d{2}:\d{2}:\d{2}", time):
                try:
                    datetime.strptime(time, "%H:%M:%S")
                    break
                except ValueError:
                    print("Invalid time. Please enter a valid time in HH:MM:SS format.")
            else:
                print("Invalid time format. Please enter a time in HH:MM:SS format.")
        
        # Validate duration
        while True:
            try:
                duration = int(input("Enter schedule duration (in minutes): "))
                if duration <= 0:
                    raise ValueError("Duration must be a positive integer.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid duration in minutes.")
        
        date_time_str = f"{date} {time}"
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        
        Schedule.add_doctor_schedule(self.cursor, doctor_id, date_time_obj, duration)
        self.db.commit()
        print("Doctor schedule added successfully.")

    def is_valid_doctor_id(self, doctor_id):
        query = "SELECT COUNT(*) FROM Doctors WHERE id = %s"
        # print(f"Executing query: {query} with doctor_id: {doctor_id}")  # Debug output
        self.cursor.execute(query, (doctor_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def update_doctor_schedule_menu(self):
        self.view_doctor_schedules()
        
        # Validate schedule ID
        while True:
            try:
                schedule_id = int(input("Enter the ID of the schedule to update: "))
                if not self.is_valid_schedule_id(schedule_id):
                    raise ValueError("Schedule ID does not exist.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid schedule ID.")
        
        # Validate doctor ID (if provided)
        doctor_id = input("Enter new doctor ID (leave blank to keep the current ID): ")
        if doctor_id:
            while True:
                try:
                    doctor_id = int(doctor_id)
                    if not self.is_valid_doctor_id(doctor_id):
                        raise ValueError("Doctor ID does not exist.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a valid doctor ID or leave blank.")
                    doctor_id = input("Enter new doctor ID (leave blank to keep the current ID): ")
        else:
            doctor_id = None
        
        # Validate date (if provided)
        date = input("Enter new schedule date (YYYY-MM-DD) (leave blank to keep the current date): ")
        if date:
            while True:
                if re.match(r"\d{4}-\d{2}-\d{2}", date):
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")
                else:
                    print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
                date = input("Enter new schedule date (YYYY-MM-DD) (leave blank to keep the current date): ")
        else:
            date = None

        # Validate time (if provided)
        time = input("Enter new schedule time (HH:MM:SS) (leave blank to keep the current time): ")
        if time:
            while True:
                if re.match(r"\d{2}:\d{2}:\d{2}", time):
                    try:
                        datetime.strptime(time, "%H:%M:%S")
                        break
                    except ValueError:
                        print("Invalid time. Please enter a valid time in HH:MM:SS format.")
                else:
                    print("Invalid time format. Please enter a time in HH:MM:SS format.")
                time = input("Enter new schedule time (HH:MM:SS) (leave blank to keep the current time): ")
        else:
            time = None
        
        # Validate duration (if provided)
        duration = input("Enter new schedule duration (in minutes) (leave blank to keep the current duration): ")
        if duration:
            while True:
                try:
                    duration = int(duration)
                    if duration <= 0:
                        raise ValueError("Duration must be a positive integer.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a valid duration in minutes or leave blank.")
                    duration = input("Enter new schedule duration (in minutes) (leave blank to keep the current duration): ")
        else:
            duration = None
        
        # Prepare datetime object if date or time is provided
        if date or time:
            date_time_str = f"{date} {time}"
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        else:
            date_time_obj = None

        Schedule.update_doctor_schedule(self.cursor, schedule_id, doctor_id, date_time_obj, duration)
        self.db.commit()
        print("Doctor schedule updated successfully.")

    def is_valid_schedule_id(self, schedule_id):
        query = "SELECT COUNT(*) FROM Schedules WHERE id = %s"
        self.cursor.execute(query, (schedule_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def view_doctor_schedules(self, doctor_id=None):
        schedule = Schedule(self.cursor, self.db)
        schedule.view_doctor_schedules(doctor_id)

    def delete_doctor_schedule_menu(self):
        schedule = Schedule(self.cursor, self.db)
        schedule.delete_doctor_schedules()


    def show_menu(self):
        print("===== Beauty Clinic =====")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Register User")
        print("4. Exit Program")

    def beauty_product_menu(self):
        while True:
            print("\nBeauty Product Shop Menu:")
            print("1. Open Catalog")
            print("2. See Cart")
            print("3. Checkout")
            print("4. Back to Main Program")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.catalog.display_catalog(self.cart)
            elif choice == "2":

                self.cart.load_cart_items()
                self.cart_menu()
            elif choice == "3":
                self.cart.checkout()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def display_cart(self):
        self.cart.display_cart()

    def cart_menu(self):
        while True:
            print("\nShopping Cart Menu:")
            print("1. Remove Item from shopping cart")
            print("2. Checkout")
            print("3. Back to main menu")
            choice = input("Enter your choice (1-3): ").lower()

            if choice == "1":
                if not self.cart.items:
                    print("Your cart is empty.")
                else:
                    index = int(input("Enter the number of the item to remove: "))
                    self.cart.remove_item(index)
                    break
            elif choice == "2":
                self.cart.checkout()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                self.loginUser()
            elif choice == "2":
                self.loginAdmin()
            elif choice == "3":
                self.register()
            elif choice == "4":
                self.db.close()
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please try again.")

clinic = BeautyClinic()
clinic.run()