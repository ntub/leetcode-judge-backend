from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):  # type: ignore
    page_size_query_param = "page_size"
    max_page_size = 100
