from datetime import datetime
from werkzeug.security import generate_password_hash
from models import db, User, Product, Category, Order, OrderItem, Cart, CartItem, Payment, Sale, Supplier, PurchaseOrder
from app import create_app  # Assuming you have a function to create your Flask app

# Initialize data to populate the database
def seed_data():
    # Create sample categories
    category1 = Category(name="Skincare", description="Products for skincare routines")
    category2 = Category(name="Makeup", description="Makeup products for all skin types")
    db.session.add_all([category1, category2])

    # Create sample suppliers
    supplier1 = Supplier(name="Beauty Supplies Inc.", location="New York")
    supplier2 = Supplier(name="Glamour Distributors", location="Los Angeles")
    db.session.add_all([supplier1, supplier2])

    # Commit to the database to assign IDs
    db.session.commit()

    # Create sample products
    product1 = Product(
        name="Moisturizer",
        description="A hydrating facial moisturizer.",
        buying_price=5.50,
        selling_price=10.99,
        stock=100,
        category=category1
    )
    product2 = Product(
        name="Foundation",
        description="Liquid foundation with SPF.",
        buying_price=8.00,
        selling_price=20.99,
        stock=150,
        category=category2
    )
    db.session.add_all([product1, product2])

    # Commit to assign IDs for products
    db.session.commit()

    # Create sample users
    user1 = User(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        password_digest=generate_password_hash("password123"),
        role="customer"
    )
    user2 = User(
        first_name="Bob",
        last_name="Johnson",
        email="bob@example.com",
        password_digest=generate_password_hash("password123"),
        role="admin"
    )
    db.session.add_all([user1, user2])

    # Commit to assign IDs for users
    db.session.commit()

    # Create a cart for the customer
    cart1 = Cart(user=user1)
    db.session.add(cart1)

    # Add cart items for the cart
    cart_item1 = CartItem(cart=cart1, product=product1, quantity=2)
    cart_item2 = CartItem(cart=cart1, product=product2, quantity=1)
    db.session.add_all([cart_item1, cart_item2])

    # Commit cart and cart items
    db.session.commit()

    # Create an order for the customer
    order1 = Order(user=user1, total_price=30.99, status="PENDING")
    db.session.add(order1)

    # Add order items for the order
    order_item1 = OrderItem(order=order1, product=product1, quantity=2, unit_price=10.99)
    order_item2 = OrderItem(order=order1, product=product2, quantity=1, unit_price=20.99)
    db.session.add_all([order_item1, order_item2])

    # Commit order and order items
    db.session.commit()

    # Create payment and sale record for the order
    payment1 = Payment(order=order1, billing_address="123 Beauty Lane", total_amount=30.99)
    sale1 = Sale(payment=payment1, sale_date=datetime.utcnow(), amount=30.99)
    db.session.add_all([payment1, sale1])

    # Commit payment and sale
    db.session.commit()

    # Create purchase orders to restock inventory
    purchase_order1 = PurchaseOrder(
        supplier_id=supplier1.id, product_id=product1.id, quantity=50, order_date=datetime.utcnow(), cost=275.0
    )
    purchase_order2 = PurchaseOrder(
        supplier_id=supplier2.id, product_id=product2.id, quantity=30, order_date=datetime.utcnow(), cost=240.0
    )
    db.session.add_all([purchase_order1, purchase_order2])

    # Commit purchase orders
    db.session.commit()

    # Success message
    print("Data seeded successfully!")

# Main entry point for seeding data
if __name__ == "__main__":
    app = create_app()  # Create the Flask app instance
    with app.app_context():  # Push the app context
        db.create_all()  # Ensure all tables are created
        seed_data()
