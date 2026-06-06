from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import AuthorPage, BookPage, EventPage
from home.models.contact_message import ContactMessage
from home.serializers.author import AuthorPageSerializer
from home.serializers.book import BookPageDetailSerializer, BookPageListSerializer
from home.serializers.contact import ContactMessageInputSerializer
from home.serializers.event import EventPageDetailSerializer, EventPageListSerializer


class AuthorPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AuthorPage model with read-only access."""

    queryset = AuthorPage.objects.none()
    serializer_class = AuthorPageSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return AuthorPage.objects.live().public().order_by("title")


class BookPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BookPage model with read-only access."""

    queryset = BookPage.objects.none()

    def get_queryset(self):
        return BookPage.objects.live()

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "retrieve":
            return BookPageDetailSerializer
        return BookPageListSerializer


class EventPageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for EventPage model with read-only access."""

    queryset = EventPage.objects.none()

    def get_queryset(self):
        return EventPage.objects.live().order_by("event_date", "event_time")

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "retrieve":
            return EventPageDetailSerializer
        return EventPageListSerializer


class ContactMessageAPIView(APIView):
    """Receive contact messages via POST."""

    def post(self, request):
        serializer = ContactMessageInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid contact message payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ContactMessage.objects.create(**serializer.validated_data)

        return Response(
            {"message": "Contact message received successfully."},
            status=status.HTTP_201_CREATED,
        )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenAPIView(APIView):
    """Set a CSRF cookie for SPA clients before unsafe requests."""

    def get(self, request):
        return Response({"detail": "CSRF cookie set."}, status=status.HTTP_200_OK)
