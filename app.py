import os, json
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from forms import RegistrationForm, LoginForm
from models import db, User, Product, Category, Cart, CartItem
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from user_routes import user_bp

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Nazwa użytkownika lub adres e-mail już istnieje', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Konto utworzone dla {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Zalogowano pomyślnie!', 'success')
            cart = Cart.query.filter_by(user_id=user.id).first()
            session['cart'] = [item.product_id for item in cart.items] if cart else []
            next_page = request.args.get('next', request.referrer or url_for('home'))
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nieprawidłowy email lub hasło', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano pomyślnie!', 'danger')
    return redirect(request.referrer or url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/products')
def products():
    categories = Category.query.all()
    cart = Cart.query.filter_by(user_id=current_user.id).first() if current_user.is_authenticated else None
    cart_items = session.get('cart', []) if current_user.is_authenticated else []
    return render_template('products.html', categories=categories, cart=cart)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()

    session['cart'] = [item.product_id for item in cart.items]

    total_items = sum(item.quantity for item in cart.items)
    return jsonify({
        'message': 'Produkt dodany do koszyka!',
        'category': 'success',
        'total_items': total_items,
        'product': {
            'id': product.id,
            'name': product.name,
            'quantity': cart_item.quantity,
            'price': product.price
        }
    })
    
@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=item_id).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                db.session.delete(cart_item)
            db.session.commit()
            session['cart'] = [item.product_id for item in cart.items]
            total_items = sum(item.quantity for item in cart.items)
            print(f"Produkt {item_id} został usunięty z koszyka.")
            return jsonify({'message': 'Produkt usunięty z koszyka!', 'category': 'success', 'quantity': cart_item.quantity if cart_item.quantity > 0 else 0})
        else:
            print(f"Produkt o ID {item_id} nie znaleziony w koszyku.")
            return jsonify({'message': 'Produkt nie znaleziony w koszyku!', 'category': 'danger'})
    return jsonify({'message': 'Brak koszyka użytkownika!', 'category': 'danger'})

@app.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('cart.html', cart=cart)

app.register_blueprint(user_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)