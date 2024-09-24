from flask import Flask, render_template, request, jsonify
from models import db, Product, Order, FAQ
import spacy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({'response': "I'm sorry, I didn't understand that."})

    response = process_query(user_input)
    return jsonify({'response': response})

def process_query(query):
    # Check if the query is related to order status
    order_response = check_order_status(query)
    if order_response != "No valid order ID found in the query." and order_response != "Order ID not found.":
        return order_response

    # Check if the query is related to product search
    product_response = search_product(query)
    if product_response != "No products found matching your query.":
        return product_response

    # Check if the query is related to FAQ
    faq_response = search_faq(query)
    return faq_response

def search_product(query):
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    if products:
        response = 'Here are the products I found:\n'
        for product in products:
            response += f"- {product.name}: ${product.price}\n"
    else:
        response = "No products found matching your query."
    return response

def check_order_status(query):
    try:
        # Extract order ID from the query
        order_id_str = ''.join(filter(str.isdigit, query))
        if order_id_str:
            order_id = int(order_id_str)
            order = Order.query.filter_by(order_id=order_id).first()
            if order:
                response = f"Order {order.order_id} is currently '{order.order_status}'."
            else:
                response = "Order ID not found."
        else:
            response = "No valid order ID found in the query."
    except Exception as e:
        response = f"Error retrieving order status: {str(e)}"
    return response

def search_faq(query):
    try:
        faqs = FAQ.query.all()
        if not faqs:
            return "No FAQs available at the moment."

        nlp_query = nlp(query)
        highest_score = 0
        best_answer = "I'm sorry, I don't have an answer to that question."
        for faq in faqs:
            nlp_faq = nlp(faq.question)
            similarity = nlp_query.similarity(nlp_faq)
            if similarity > highest_score:
                highest_score = similarity
                best_answer = faq.answer
        
        return best_answer
    except Exception as e:
        return f"Error retrieving FAQ: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
