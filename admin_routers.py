from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, User, Category, Product, Cart, CartItem
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin != 1:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def admin_panel():
    users = User.query.all()
    categories = Category.query.all()
    products = Product.query.all()
    carts = Cart.query.all()
    cart_items = CartItem.query.all()
    return render_template('admin_panel.html', users=users, categories=categories, products=products, carts=carts, cart_items=cart_items)

@admin_bp.route('/update-user/<int:user_id>', methods=['POST'])
@admin_required
def admin_update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.username = request.form.get('username')
    user.email = request.form.get('email')
    user.is_admin = 1 if 'is_admin' in request.form else 0
    db.session.commit()
    flash('User updated successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/update-category/<int:category_id>', methods=['POST'])
@admin_required
def admin_update_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.name = request.form.get('name')
    db.session.commit()
    flash('Category updated successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/delete-category/<int:category_id>', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/update-product/<int:product_id>', methods=['POST'])
@admin_required
def admin_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.price = request.form.get('price')
    product.image_url = request.form.get('image_url')
    product.category_id = request.form.get('category_id')
    db.session.commit()
    flash('Product updated successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/delete-product/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/delete-cart/<int:cart_id>', methods=['POST'])
@admin_required
def admin_delete_cart(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    db.session.delete(cart)
    db.session.commit()
    flash('Cart deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/update-cart-item/<int:cart_item_id>', methods=['POST'])
@admin_required
def admin_update_cart_item(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    cart_item.quantity = request.form.get('quantity')
    db.session.commit()
    flash('Cart item updated successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))

@admin_bp.route('/delete-cart-item/<int:cart_item_id>', methods=['POST'])
@admin_required
def admin_delete_cart_item(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Cart item deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_panel'))