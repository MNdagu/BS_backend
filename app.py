from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, User, Product, Category, Order, OrderItem, Cart, CartItem, Supplier, PurchaseOrder
from auth import auth_bp  # Import auth blueprint
from datetime import timedelta, datetime
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize Flask app and configuration
def create_app():
    app = Flask(__name__)

    # Database and JWT configuration
    db_path = os.path.join(os.path.abspath(os.getcwd()), "beautyshop.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    CORS(app)

    ### Parsers for incoming JSON data ###
    product_parser = reqparse.RequestParser()
    product_parser.add_argument('name', type=str, required=True)
    product_parser.add_argument('description', type=str, required=True)
    product_parser.add_argument('price', type=float, required=True)
    product_parser.add_argument('stock', type=int, required=True)
    product_parser.add_argument('category_id', type=int, required=True)
    product_parser.add_argument('image_url', type=str, required=False)

    order_status_parser = reqparse.RequestParser()
    order_status_parser.add_argument(
        'status', type=str
    )

    ### Product Management ###
    class ProductResource(Resource):
        @jwt_required()
        def get(self, product_id=None):
            if product_id:
                product = Product.query.get(product_id)
                if product:
                    return jsonify(product.to_dict())
                return {"message": "Product not found"}, 404
            products = Product.query.all()
            return jsonify([p.to_dict() for p in products])

        @jwt_required()
        def post(self):
            args = product_parser.parse_args()
            new_product = Product(
                name=args['name'], description=args['description'],
                price=args['price'], stock=args['stock'],
                category_id=args['category_id'], image_url=args.get('image_url')
            )
            db.session.add(new_product)
            db.session.commit()
            return jsonify({"message": "Product created", "product": new_product.to_dict()}), 201

    ### Cart Management ###
    class CartCreationResource(Resource):
        @jwt_required()
        def post(self):
            user_id = get_jwt_identity()['user_id']
            existing_cart = Cart.query.filter_by(user_id=user_id).first()
            if existing_cart:
                return {"message": "Cart already exists for this user"}, 400
            cart = Cart(user_id=user_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            db.session.add(cart)
            db.session.commit()
            return {"message": "Cart created", "cart_id": cart.id}, 201

    class CartResource(Resource):
        @jwt_required()
        def get(self):
            user_id = get_jwt_identity()['user_id']
            cart = Cart.query.filter_by(user_id=user_id).first()
            if not cart:
                return {"message": "No cart found for this user"}, 404
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            return jsonify([item.to_dict() for item in cart_items]), 200

        @jwt_required()
        def post(self):
            user_id = get_jwt_identity()['user_id']
            data = request.get_json()
            cart = Cart.query.filter_by(user_id=user_id).first()
            if not cart:
                return {"message": "Cart not found, create a cart first"}, 404
            cart_item = CartItem(cart_id=cart.id, product_id=data['product_id'], quantity=data['quantity'])
            db.session.add(cart_item)
            db.session.commit()
            return {"message": "Added to cart"}, 201

    ### Order Management ###
    class OrderResource(Resource):
        @jwt_required()
        def get(self, order_id=None):
            user_id = get_jwt_identity()['user_id']
            if order_id:
                order = Order.query.get_or_404(order_id)
                if order.user_id != user_id:
                    return jsonify({"message": "Unauthorized"}), 403
                return jsonify(order.to_dict())
            orders = Order.query.filter_by(user_id=user_id).all()
            return jsonify([order.to_dict() for order in orders])

        @jwt_required()
        def post(self):
            data = request.get_json()
            user_id = get_jwt_identity()['user_id']
            order = Order(user_id=user_id, total_price=0, status='PENDING')
            db.session.add(order)
            db.session.commit()
            total_price = 0
            for item_data in data.get('order_items', []):
                product = Product.query.get(item_data['product_id'])
                if not product:
                    return {"message": f"Product {item_data['product_id']} not found"}, 404
                order_item = OrderItem(
                    order_id=order.id, product_id=product.id,
                    quantity=item_data['quantity'], price=product.price
                )
                db.session.add(order_item)
                total_price += product.price * item_data['quantity']
            order.total_price = total_price
            db.session.commit()
            return {"message": "Order and invoice created", "order_id": order.id}, 201

    ### Supplier and Purchase Order Management ###
    class SupplierResource(Resource):
        def post(self):
            data = request.get_json()
            new_supplier = Supplier(
                name=data['name'], location=data.get('location'), distribution=data.get('distribution')
            )
            db.session.add(new_supplier)
            db.session.commit()
            return {"message": "Supplier added", "supplier": new_supplier.to_dict()}, 201

        def get(self, supplier_id=None):
            if supplier_id:
                supplier = Supplier.query.get(supplier_id)
                return jsonify(supplier.to_dict()) if supplier else {"message": "Supplier not found"}, 404
            suppliers = Supplier.query.all()
            return jsonify([s.to_dict() for s in suppliers]), 200

    class PurchaseOrderResource(Resource):
        def post(self):
            data = request.get_json()
            new_po = PurchaseOrder(
                supplier_id=data['supplier_id'], product_id=data['product_id'],
                quantity=data['quantity'], order_date=datetime.utcnow(), cost=data['cost']
            )
            db.session.add(new_po)
            db.session.commit()
            return {"message": "Purchase order created", "purchase_order": new_po.to_dict()}, 201

    ### Blueprint Registration ###
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Blueprints and APIs
    product_bp = Blueprint('product', __name__)
    api_product = Api(product_bp)
    api_product.add_resource(ProductResource, '/products', '/products/<int:product_id>')

    cart_bp = Blueprint('cart', __name__)
    api_cart = Api(cart_bp)
    api_cart.add_resource(CartCreationResource, '/cart/create')
    api_cart.add_resource(CartResource, '/cart')

    order_bp = Blueprint('order', __name__)
    api_order = Api(order_bp)
    api_order.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')

    supplier_bp = Blueprint('supplier', __name__)
    api_supplier = Api(supplier_bp)
    api_supplier.add_resource(SupplierResource, '/suppliers', '/suppliers/<int:supplier_id>')

    purchase_order_bp = Blueprint('purchase_order', __name__)
    api_purchase_order = Api(purchase_order_bp)
    api_purchase_order.add_resource(PurchaseOrderResource, '/purchase_orders')

    # Register blueprints
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(supplier_bp, url_prefix='/api')
    app.register_blueprint(purchase_order_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
