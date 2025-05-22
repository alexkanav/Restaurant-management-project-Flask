from app.blueprints.admin.models import Price, Category
from app.blueprints.users.models import Dish
from config import table_numbers, menu_add, menu_add_ua, category_icons


def read_context() -> dict:
    price = Price.query.first().price
    menu = {i.category: i.names for i in Category.query}
    dish_attributes = {i.dish_code: [i.name_ua, i.describe, i.image_link, i.likes] for i in Dish.query}
    categories_number = len(menu)
    context = {
        'table_numbers': table_numbers,
        'menu_add': menu_add,
        'menu_add_ua': menu_add_ua,
        'category_icons': category_icons,
        'menu': menu,
        'dish_attributes': dish_attributes,
        'price': price,
        'categories_number': categories_number
    }
    return context
