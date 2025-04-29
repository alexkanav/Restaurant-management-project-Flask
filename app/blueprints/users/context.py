from app.blueprints.admin.models import Prices,Categories
from app.blueprints.users.models import Dishes
from config import table_numbers, addit, menu_add, menu_add_ua


def read_context() -> dict:
    price = Prices.query.first().price
    menu = {i.category: i.names for i in Categories.query}
    describe_dish = {i.dish_code: [i.name_ua, i.describe, i.image_link, i.likes] for i in Dishes.query}
    num_category = len(menu)
    context = {
        'table_numbers': table_numbers,
        'addit': addit,
        'menu_add': menu_add,
        'menu_add_ua': menu_add_ua,
        'menu': menu,
        'describe_dish': describe_dish,
        'price': price,
        'num_category': num_category
    }
    return context
