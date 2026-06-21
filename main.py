import html
from datetime import datetime
import xml.etree.ElementTree as ET

CATEGORIES = [
    {
        "id": 1,
        "name": "Чай",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Посуда",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Подарочные наборы",
        "is_active": False,
    },
]

PRODUCTS = [
    {
        "id": 101,
        "name": 'Чай "Лес & травы" <сбор №1>',
        "slug": "les-i-travy",
        "category_id": 1,
        "price": "490.00",
        "old_price": "590.00",
        "stock": 12,
        "description": "Вкус: мята & чабрец > классический чай",
        "image_url": "https://example.test/media/tea-101.jpg",
        "is_active": True,
    },
    {
        "id": 102,
        "name": "Чайник стеклянный",
        "slug": "glass-teapot",
        "category_id": 2,
        "price": "1500.00",
        "old_price": "1400.00",
        "stock": 0,
        "description": "Стеклянный чайник объёмом 800 мл",
        "image_url": "https://example.test/media/teapot-102.jpg",
        "is_active": True,
    },
    {
        "id": 103,
        "name": "Скрытый товар",
        "slug": "hidden-product",
        "category_id": 1,
        "price": "350.00",
        "old_price": None,
        "stock": 5,
        "description": "Товар отключён администратором",
        "image_url": "https://example.test/media/product-103.jpg",
        "is_active": False,
    },
    {
        "id": 104,
        "name": "Пробник чая",
        "slug": "tea-sample",
        "category_id": 1,
        "price": "0.00",
        "old_price": None,
        "stock": 30,
        "description": "Бесплатный пробник",
        "image_url": "https://example.test/media/product-104.jpg",
        "is_active": True,
    },
    {
        "id": 105,
        "name": "Чашка фарфоровая",
        "slug": "porcelain-cup",
        "category_id": 2,
        "price": "700.00",
        "old_price": "900.00",
        "stock": 4,
        "description": "Фарфоровая чашка",
        "image_url": None,
        "is_active": True,
    },
    {
        "id": 106,
        "name": "Подарочный набор",
        "slug": "gift-set",
        "category_id": 3,
        "price": "2500.00",
        "old_price": "3000.00",
        "stock": 2,
        "description": "Товар находится в неактивной категории",
        "image_url": "https://example.test/media/product-106.jpg",
        "is_active": True,
    },
    {
        "id": 107,
        "name": "Чай улун молочный",
        "slug": "milk-oolong",
        "category_id": 1,
        "price": "700.50",
        "old_price": None,
        "stock": 3,
        "description": "",
        "image_url": "https://example.test/media/product-107.jpg",
        "is_active": True,
    },
]


def build_yml(products, categories, generated_at):
    products, categories = filter_data(products, categories)

    root = ET.Element('yml_catalog', date=generated_at.strftime('%Y-%m-%d %H:%M:%S'))
    shop = ET.SubElement(root, 'shop')

    ET.SubElement(shop, "name").text = "Test Shop"
    ET.SubElement(shop, "company").text = "Test Company"
    ET.SubElement(shop, "url").text = "https://example.test"

    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", id='RUB', rate='1')

    categories_elem = ET.SubElement(shop, "categories")
    for product in list({item['category_id']: item for item in products}.values()):
        category = next(
            category
            for category in categories
            if category["id"] == product["category_id"]
        )
        cat_elem = ET.SubElement(categories_elem, 'category', id=str(category.get('id')))
        cat_elem.text = category.get('name')

    offers_elem = ET.SubElement(shop, "offers")
    for product in products:
        offer_elem = ET.SubElement(offers_elem, 'offer')
        offer_elem.set('id', str(product.get('id')))
        offer_elem.set('available', 'true' if product["stock"] else 'false')

        ET.SubElement(offer_elem, 'url').text = f'https://example.test/products/{product["slug"]}/'

        price = product.get('price')
        ET.SubElement(offer_elem, 'price').text = price

        if check_price(product["old_price"], price):
            ET.SubElement(offer_elem, 'oldprice').text = product.get('old_price')

        ET.SubElement(offer_elem, 'currencyId').text = 'RUB'
        ET.SubElement(offer_elem, 'categoryId').text = str(product.get("category_id"))

        ET.SubElement(offer_elem, 'picture').text = product["image_url"]
        ET.SubElement(offer_elem, 'name').text = html.escape(product.get("name"))

        description = product.get('description')
        if description:
            ET.SubElement(offer_elem, 'description').text = html.escape(description)

    return ET.tostring(root, encoding='utf-8')


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


if __name__ == "__main__":
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(2026, 6, 18, 12, 0),
    )

    print(result)
    print(ET.fromstring(result).tag)

    with open("docs/output.xml", "wb") as f:
        f.write(result)
