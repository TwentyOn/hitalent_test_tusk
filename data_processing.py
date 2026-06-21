def filter_data(products, categories):
    """
    Пайплайн фильтрации данных
    :param products:
    :param categories:
    :return:
    """

    categories = list(filter(lambda c: c.get('is_active'), categories))
    categories.sort(key=lambda c: c['id'])
    products = filter(filter_product, products)
    products = list(filter(lambda p: p.get('category_id') in [c['id'] for c in categories], products))
    products.sort(key=lambda p: p['id'])

    return products, categories


def filter_product(product):
    if any((
        not product.get('is_active'),
        not float(product.get('price')) > 0.0 or product.get('name').strip() == '',
        not product.get('image_url') or not product.get('image_url').startswith(('http', 'https'))
    )):
        return False
    else:
        return True


def check_price(old_price: int, price: int):
    if not old_price or price > old_price:
        return False
    return True
