from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    max_page_size = 1000
    page_query_param = 'page_size'
    page_size = 100


