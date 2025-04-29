from flask import Blueprint, render_template, request, make_response, flash, redirect

from .models import Users, Dishes, Orders, Comments
from app.extensions import db, cache
from .context import read_context

users_bp = Blueprint('users', __name__, template_folder='templates')


def create_new_user() -> int:
    last_user = db.session.query(Users).order_by(Users.id.desc()).first()
    new_user_id = last_user.user_id + 1 if last_user else 1
    new_user = Users(user_id=new_user_id)
    db.session.add(new_user)
    db.session.commit()

    return new_user_id


@users_bp.route('/')
@cache.cached(timeout=600)
def index():
    title = "Кафе"
    comments_to_template = [(c.user_name, c.comment_date_time, c.comment_text) for c in Comments.query]

    return render_template('cafe_web.html', title=title, comments=comments_to_template)


@users_bp.route('/choice-dish/')
@cache.cached(timeout=3600)
def choice_of_dishes():
    title = "Вибір замовлення"
    context = read_context()
    user_id = request.cookies.get('user_id')
    if not user_id:
        new_user_id = str(create_new_user())
        response = make_response(
            render_template('choice_dish.html', title=title, **context))
        response.set_cookie('user_id', new_user_id, max_age=60 * 60 * 24 * 365)
        return response

    return render_template('choice_dish.html', title=title, **context)


@users_bp.route('/dish/<dish_code>')
def display_dish(dish_code: str):
    title = "Опис страви"
    selected_dish = Dishes.query.filter_by(dish_code=dish_code).first()
    selected_dish.views += 1
    db.session.commit()

    return render_template('dish_describe.html', title=title, id=selected_dish.id, describe=selected_dish.describe,
                           img=selected_dish.image_link, likes=selected_dish.likes, views=selected_dish.views)


@users_bp.route('/post-order', methods=['POST'])
def get_order_from_client():
    if request.method == "POST":
        try:
            order = request.get_json()
            if 'fish' in order:
                wait = '35'
            elif 'soup' in order or 'steak' in order:
                wait = '25'
            else:
                wait = '15'
            user_id = int(request.cookies.get('user_id'))
            order_sum = int(order.pop('sum'))
            table_num = order.pop('table_number')
            if not user_id:
                print('user not found')
                user_id = 0

            add_order = Orders(
                user_id=user_id,
                table_number=table_num,
                order_sum=order_sum,
                order=order
            )
            db.session.add(add_order)

            update_user_stat = Users.query.filter_by(user_id=user_id).first()
            update_user_stat.sessions += 1
            update_user_stat.total_sum += order_sum

            db.session.commit()
            resp = make_response(render_template('finish.html'))
            resp.set_cookie('order', 'ok', max_age=10)
            resp.set_cookie('wait', wait, max_age=10)

        except Exception as e:
            flash(f"{e}")
            resp = make_response(render_template('finish.html'))
            resp.set_cookie('order', 'trouble')
        return resp

    return render_template('cafe_web.html')


@users_bp.route('/post-order-like', methods=['POST'])
def post_order_like():
    if request.method == "POST":
        like_id = request.get_json()
        add_like = Dishes.query.filter_by(id=like_id).first()
        add_like.likes += 1
        db.session.commit()

    return render_template('cafe_web.html')


@users_bp.route("/upload-comment", methods=['POST'])
def upload_comment():
    user_id = int(request.cookies.get('user_id'))
    if request.method == "POST":
        comm_name = request.form['comm_name']
        comm_text = request.form['comm_text']
        comment = Comments(
            user_id=user_id,
            user_name=comm_name,
            comment_text=comm_text
        )
        db.session.add(comment)
        db.session.commit()

    return redirect('/')


@users_bp.route('/finish')
def finish_ok():
    title = "Замовлення"
    message_ok = ''
    m_d = ''
    wait = ''
    message_fault = ''
    success_order = request.cookies.get('order')
    if success_order == 'ok':
        wait = request.cookies.get('wait')
        message_ok = f'Дякуємо. Ваше замовлення прийняте і буде готове через - {wait} хвилин.'
        m_d = '(Час виконання замовлення розраховується автоматично відповідно до вибраних вами страв)'
    else:
        message_fault = 'При відправленні замовлення сталася помилка (.'

    return render_template('finish.html', title=title, message_ok=message_ok, m_d=m_d, message_fault=message_fault,
                           wait=wait)
