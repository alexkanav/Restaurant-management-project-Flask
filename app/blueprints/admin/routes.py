from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required, logout_user

from .models import Staff
from app.blueprints.users.models import Order
from app.extensions import login_manager, logger
from app.forms import RegisterForm, LoginForm


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

login_manager.login_view = 'admin.login'
login_manager.login_message = "Для перегляду потрібна авторизація."


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(user_id)


@admin_bp.route('/')
def admin_dashboard():
    name = current_user.username if current_user.is_authenticated else "Вхід не виконано!!!"
    return render_template('admin_dashboard.html', name=name)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Staff.query.filter(Staff.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.admin_dashboard'))
        else:
            flash('Не збігається логін-пароль. Спробуйте ще раз.')
            return redirect(url_for('admin.login'))

    return render_template('login.html', form=form)


@admin_bp.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect(url_for('admin.admin_dashboard')))
    # Delete the cookie
    resp.delete_cookie('remember_token')
    return resp


@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if Staff.query.filter(Staff.email == form.email.data).first():
            flash("Ваша Email вже зареєстрована.")
            return redirect(url_for('admin.register'))

        if Staff.add_user(form.username.data, form.email.data, form.password.data):
            flash('Ви успішно зареєстровані, увійдіть до системи.')
            return redirect(url_for('admin.login'))
        else:
            flash("При реєстрації виникла помилка.")

    return render_template('register.html', form=form)


@admin_bp.route('/order-processing')
@login_required
def order_processing():
    return render_template('order_processing.html', name=current_user.username)


@admin_bp.route('/checking-new-orders')
@login_required
def checking_new_order():
    current_order_number = Order.query.count()
    return jsonify(current_order_number)


@admin_bp.route('/update-orders')
@login_required
def update_orders():
    try:
        uncompleted_orders = Order.query.filter_by(completed='No').all()
        order_count = len(uncompleted_orders)
        new_orders = [order.to_dict() for order in uncompleted_orders]
        return render_template('order_block.html', order_count=order_count, items=new_orders)

    except Exception as e:
        logger.error("order update error: %s", e, exc_info=True)
        return "<div class='error'> Зв'язок з сервером втрачено</div>"


@admin_bp.route('/closing-order', methods=['POST'])
@login_required
def closing_order():
    data = request.get_json()

    order_id = data.get('order_id')
    if not order_id:
        return jsonify({"success": False, "error": "Missing order_id"}), 400

    try:
        Order.update(order_id, current_user.id)
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error("Order update error: %s", e, exc_info=True)
        return jsonify({"success": False, "error": "Internal server error"}), 500
