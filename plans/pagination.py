from rest_framework.pagination import PageNumberPagination

class MembershipPagination(PageNumberPagination):
    page_size = 6