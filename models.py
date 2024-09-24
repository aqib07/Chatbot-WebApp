from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    stock_quantity = db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    order_status = db.Column(db.String(50))
    date_ordered = db.Column(db.DateTime)
    total_amount = db.Column(db.Numeric(10, 2))

class FAQ(db.Model):
    __tablename__ = 'faqs'
    faq_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    category = db.Column(db.String(100))
