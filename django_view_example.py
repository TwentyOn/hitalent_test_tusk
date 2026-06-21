from datetime import datetime

# импорты Django...

from feed_task import build_yml

class MyView(ParentViewClass):
    def get(self, request, *args, **kwargs):

        xml = build_yml(PRODUCTS, CATEGORIES, datetime.today())

        return Response(xml, content_type='application/xml; charset=utf-8')