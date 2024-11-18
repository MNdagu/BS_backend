from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Users Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = db.relationship('Order', backref='user')
    cart = db.relationship('Cart', uselist=False, backref='user')

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# Products Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    buying_price = db.Column(db.Numeric, nullable=False)
    selling_price = db.Column(db.Numeric, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('Category', backref='products')
    order_items = db.relationship('OrderItem', backref='product')
    cart_items = db.relationship('CartItem', backref='product')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "buying_price": float(self.buying_price),
            "selling_price": float(self.selling_price),
            "stock": self.stock,
            "category_id": self.category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# Categories Model
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


# Orders Model
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='order')
    payment = db.relationship('Payment', uselist=False, backref='order')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_price": float(self.total_price),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# Order Items Model
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price)
        }


# Carts Model
class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart_items = db.relationship('CartItem', backref='cart')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


# Cart Items Model
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }


# Payments Model
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    billing_address = db.Column(db.String, nullable=False)
    total_amount = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sale = db.relationship('Sale', uselist=False, backref='payment')

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "billing_address": self.billing_address,
            "total_amount": float(self.total_amount),
            "created_at": self.created_at
        }


# Sales Model
class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "sale_date": self.sale_date,
            "amount": float(self.amount)
        }


# Suppliers Model
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)

    purchase_orders = db.relationship('PurchaseOrder', backref='supplier')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }


# Purchase Orders Model
class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, default=datetime.utcnow)
    cost = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "order_date": self.order_date,
            "cost": float(self.cost)
        }
