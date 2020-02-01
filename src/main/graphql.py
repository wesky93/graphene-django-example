import base64

import graphene
import math


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


class PageType(graphene.ObjectType):
    page_number = graphene.Int()
    after = graphene.String()


class PaginationType(graphene.ObjectType):
    last_page = graphene.Field(PageType)
    pages = graphene.Field(graphene.List(PageType))

    @classmethod
    def pagination(cls, all_count, page_size, start_page=1):
        start_page = start_page - 1
        page_count = math.ceil(all_count / page_size)
        all_pages = [PageType(page_number=1)]
        if page_count > 1:
            all_pages += [PageType(
                page_number=i,
                after=stringToBase64(f"arrayconnection:{page_size * (i - 1) - 1}"),
            ) for i in range(2, page_count + 1)]
        return PaginationType(last_page=all_pages[-1], pages=all_pages[start_page: start_page + 10])
