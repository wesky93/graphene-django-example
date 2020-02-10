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


class CustomGrapheneFilter:
    """
    django-filter를 대체하는 Graphene 전용 필터입니다.
    커넥션 필드 생성시 사용한 인자 이름으로 메소드를 생성한뒤 원하는 쿼리셋을 추가하시면
    최종 쿼리셋 요청 단계에서 필터가 체이닝되어 적용이 됩니다.
    만약 모든 필터에 항상 적용해야될 경우 get_queryset메소드를 오버라이딩 하시면 모든 쿼리셋에 해당 필터를 적용할수 있습니다.
    """

    def __init__(self, base_queryset, info, *args, **kwargs):
        self.info = info
        self.request = self.info.context
        self.arguments = kwargs
        self._qs: QuerySet = base_queryset

    @property
    def is_anonymous_user(self) -> bool:
        if hasattr(self.request, 'user') is False or self.request.user.is_anonymous:
            return True
        return False

    def get_queryset(self):
        for key, value in self.arguments.items():
            if hasattr(self, key):
                self._qs = getattr(self, key)(self._qs, value)
        return self._qs


class enforce_first_or_last(object):

    def __init__(self, max_limit=None):
        self.max_limit = max_limit or settings.GRAPHENE['DEFAULT_MAX_LIMIT']

    def __call__(self, func, *args, **kwargs):
        max_limit = self.max_limit

        def wrapper(*args, **kwargs):
            first = kwargs.get('first')
            last = kwargs.get('last')
            info = args[1]
            assert first or last, (
                'You must provide a `first` or `last` value to properly paginate the `{}` connection.'
            ).format(args[1].field_name)

            if first:
                assert first <= max_limit, (
                    'Requesting {} records on the `{}` connection exceeds the `first` limit of {} records.'
                ).format(first, info.field_name, max_limit)
                kwargs['first'] = min(first, max_limit)

            if last:
                assert last <= max_limit, (
                    'Requesting {} records on the `{}` connection exceeds the `last` limit of {} records.'
                ).format(first, info.field_name, max_limit)
                kwargs['last'] = min(last, max_limit)

            return func(*args, **kwargs)

        return wrapper
