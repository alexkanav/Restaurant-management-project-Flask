from flask import Blueprint, render_template, request, make_response, flash, abort, jsonify

from .models import User, Dish, Order, Comment
from app.extensions import cache, logger, safe_commit
from .context import read_context
from config import carousel_img, contacts, working_days, opening_hours
from app.forms import CommentForm


users_bp = Blueprint('users', __name__, template_folder='templates')


@users_bp.route('/')
@cache.cached(timeout=600)
def index():
    title = "Кафе"
    try:
        comments = Comment.query.order_by(Comment.comment_date_time.desc()).limit(10).all()
        comments_to_template = [(c.user_name, c.comment_date_time, c.comment_text) for c in comments]
    except Exception as e:
        logger.error("Comment query failed: %s", e, exc_info=True)
        comments_to_template = []

    return render_template(
        'home.html',
        title=title,
        carousel_img=carousel_img,
        comments=comments_to_template,
        contacts=contacts,
        working_days=working_days,
        opening_hours=opening_hours
    )


@users_bp.route('/choice-dish/')
@cache.cached(timeout=3600, unless=lambda: not request.cookies.get('user_id'))
def choice_of_dishes():
    title = "Вибір замовлення"
    context = read_context()
    user_id = request.cookies.get('user_id')
    html = render_template('choice_dish.html', title=title, **context)
    if not user_id:
        new_user_id = str(User.create_new_user())
        response = make_response(html)
        response.set_cookie('user_id', new_user_id, max_age=60 * 60 * 24 * 365)
        return response

    return html


@users_bp.route('/dish/<dish_code>')
def display_dish(dish_code: str):
    title = "Опис страви"
    dish = Dish.query.filter(Dish.dish_code == dish_code).first()

    if dish is None:
        abort(404)

    dish.views += 1
    if not safe_commit():
        logger.error("Could not update dish views.")

    return render_template(
        'dish_description.html',
        title=title,
        id=dish.id,
        describe=dish.describe,
        image_path=dish.image_link,
        likes=dish.likes,
        views=dish.views
    )


@users_bp.route('/post-order', methods=['POST'])
def get_order_from_client():
    try:
        order = request.get_json()
        if not order:
            raise ValueError("No order data received")

        user_id_cookie = request.cookies.get('user_id')
        try:
            user_id = int(user_id_cookie)
        except (TypeError, ValueError):
            logger.warning("Invalid or missing user_id cookie")
            user_id = 0

        order_sum = int(order.pop('sum', 0))
        table_num = order.pop('table_number', 0)

        Order.add_order(user_id, table_num, order_sum, order)

        User.update(user_id, order_sum)

        return jsonify({"processed": True}), 200

    except Exception as e:
        logger.error("Order not processed: %s", e, exc_info=True)
        return jsonify({"processed": False}), 400


@users_bp.route('/post-order-like', methods=['POST'])
def post_order_like():
    try:
        data = request.get_json()
        like_id = data.get("like_id")
        if not like_id:
            raise ValueError("Missing like_id in request")

        Dish.query.filter_by(id=like_id).update({Dish.likes: Dish.likes + 1})
        if not safe_commit():
            logger.error("Could not update dish views.")

        return jsonify({"success": True}), 200

    except Exception as e:
        logger.error("Like update error: %s", e, exc_info=True)
        return jsonify({"success": False}), 400


@users_bp.route("/upload-comment", methods=['GET', 'POST'])
def upload_comment():
    form = CommentForm()
    if form.validate_on_submit():
        user_id_raw = request.cookies.get('user_id')
        if not user_id_raw or not user_id_raw.isdigit():
            flash("Ви не зареєстровані, можливо, у вашому браузері блокуються cookie", "error")
            return render_template("faulty.html")

        user_id = int(user_id_raw)
        Comment.add_comment(user_id, form.comm_name.data, form.comm_text.data)
        flash("Дякуємо за ваш комент! Він з'явиться після модерації.", "success")
        return render_template("gratitude.html")

    return render_template("upload_comment.html", form=form)


@users_bp.route('/faulty')
def faulty():
    return render_template('faulty.html')

