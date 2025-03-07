# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

# Define the tables

# Junction table for realistic many-to-many relationships
order_product_association = Table(
    'order_product_association', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class Customer(Base):
    """description: Stores information about each customer, including balance and credit limit."""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, nullable=False)

class Order(Base):
    """description: Represents customer orders containing multiple items, including an optional notes field."""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    date_shipped = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    amount_total = Column(Float, default=0.0)  # To be derived

class Item(Base):
    """description: Contains details about each item in an order, such as quantity and unit price."""
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # To be copied from product
    amount = Column(Float, default=0.0)  # To be derived as quantity * unit_price

class Product(Base):
    """description: Stores products with their unit prices."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)

class Supplier(Base):
    """description: Represents suppliers providing products."""
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Inventory(Base):
    """description: Manages inventory details, tracking stock levels for each product."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity_in_stock = Column(Integer, default=0)

class Address(Base):
    """description: Holds address information for customers."""
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

class Category(Base):
    """description: Categorizes products for better organization."""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class ProductCategory(Base):
    """description: Links products to categories."""
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

class Payment(Base):
    """description: Records payment transactions for orders."""
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)

class Employee(Base):
    """description: Represents employees managing orders and customer service."""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)

class Department(Base):
    """description: Organizes employees into departments."""
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Employment(Base):
    """description: Links employees to departments."""
    __tablename__ = 'employment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))

# Create database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Sample Data Seeding
Session = sessionmaker(bind=engine)
session = Session()

# Adding sample data
customers = [
    Customer(name="John Doe", balance=300.0, credit_limit=1000.0),
    Customer(name="Jane Smith", balance=150.0, credit_limit=500.0),
    Customer(name="Alice Johnson", balance=200.0, credit_limit=800.0)
]

products = [
    Product(name="Widget A", unit_price=10.0),
    Product(name="Widget B", unit_price=20.0),
    Product(name="Widget C", unit_price=30.0)
]

orders = [
    Order(customer_id=1, date_shipped=None, notes="Urgent order", amount_total=100.0),
    Order(customer_id=2, date_shipped=datetime.datetime.now(), notes=None, amount_total=50.0)
]

items = [
    Item(order_id=1, product_id=1, quantity=5, unit_price=10.0, amount=50.0),  # quantity * unit_price = amount
    Item(order_id=1, product_id=2, quantity=5, unit_price=20.0, amount=100.0)
]

suppliers = [
    Supplier(name="Globex Corporation"),
    Supplier(name="Soylent Corp")
]

inventory = [
    Inventory(product_id=1, quantity_in_stock=100),
    Inventory(product_id=2, quantity_in_stock=200)
]

addresses = [
    Address(customer_id=1, street="123 Elm Street", city="Example City", postal_code="12345"),
    Address(customer_id=2, street="456 Oak Avenue", city="Sampletown", postal_code="67890")
]

categories = [
    Category(name="Electronics"),
    Category(name="Appliances")
]

product_categories = [
    ProductCategory(product_id=1, category_id=1),
    ProductCategory(product_id=2, category_id=2),
]

payments = [
    Payment(order_id=1, amount=100.0),  # Total payment for the order
    Payment(order_id=2, amount=50.0)
]

employees = [
    Employee(name="Emily Davis", position="Manager"),
    Employee(name="Michael Brown", position="Sales")
]

departments = [
    Department(name="Sales"),
    Department(name="Customer Service")
]

employment = [
    Employment(employee_id=1, department_id=1),
    Employment(employee_id=2, department_id=2)
]

# Add all records to the session
tables_data = [customers, products, orders, items, suppliers, inventory, addresses, categories, product_categories, payments, employees, departments, employment]
for data in tables_data:
    session.add_all(data)

# Commit the transactions
session.commit()

# Close session
session.close()

def declare_logic():
    # LogicBank rules according to the requirements
    Rule.sum(derive=Customer.balance, as_sum_of=Order.amount_total, where=lambda row: row.date_shipped is None)
    Rule.sum(derive=Order.amount_total, as_sum_of=Item.amount)
    Rule.formula(derive=Item.amount, as_expression=lambda row: row.quantity * row.unit_price)
    Rule.copy(derive=Item.unit_price, from_parent=Product.unit_price)
    Rule.constraint(
        validate=Customer,
        as_condition=lambda row: row.balance <= row.credit_limit,
        error_msg="Customer balance ({row.balance}) exceeds credit limit ({row.credit_limit})"
    )
