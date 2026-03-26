from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Page

from home.models import AuthorPage, BlogPost, BookPage
from home.serializers.search import GenericPageSearchSerializer


class GenericPageSearchPagination(PageNumberPagination):
    """Enable dynamic page size via query params."""

    page_size_query_param = "page_size"
    max_page_size = 100


class GenericPageSearchAPIView(APIView):
    """Search across generic pages (blog, author, and book)."""

    pagination_class = GenericPageSearchPagination

    def get(self, request):
        search_query = request.query_params.get("query") or request.query_params.get(
            "q"
        )

        if not search_query:
            return Response(
                {
                    "count": 0,
                    "next": None,
                    "previous": None,
                    "results": [],
                }
            )

        results = (
            Page.objects.live()
            .public()
            .type(
                BlogPost,
                AuthorPage,
                BookPage,
            )
            .filter(
                Q(title__icontains=search_query)
                | Q(search_description__icontains=search_query)
            )
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(results, request, view=self)
        serializer = GenericPageSearchSerializer(
            page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)
