from django.shortcuts import render
from django.db.models import Count, F

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from registrations.models import Registration
from registrations.serializers import RegistrationSerializer

from .models import Event, Track, Session
from .serializers import EventSerializer, TrackSerializer, SessionSerializer

from core.responses import success_response, error_response, paginated_response
from events.permissions import IsAdminOrSuperAdmin, IsOwnerOrReadOnly

class EventPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin, IsOwnerOrReadOnly]
    filterset_fields = ['name', 'venue', 'start_date']
    pagination_class = EventPagination
    
    def get_queryset(self):
        return Event.objects.annotate(
            registered_count=Count('registrations'),
            available_seats=F('capacity') - Count('registrations')
        ).prefetch_related(
            'tracks__sessions'
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="List of events"
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="List of events"
        )

    # RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return success_response(
            data=serializer.data,
            message="Event detail"
        )

    # CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_create(serializer)

        return success_response(
            data=serializer.data,
            message="Event created",
            status_code=status.HTTP_201_CREATED
        )

    # UPDATE
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Event updated"
        )

    # PARTIAL UPDATE
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Event partially updated"
        )

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return success_response(
            data=None,
            message="Event deleted",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'], url_path='my-events')
    def my_events(self, request):
        queryset = self.get_queryset().filter(created_by=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="My events"
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="My events"
        )

    @action(detail=True, methods=['get'], url_path='my-event-detail')
    def my_event_detail(self, request, pk=None):
        try:
            event = self.get_queryset().get(pk=pk, created_by=request.user)
        except Event.DoesNotExist:
            return error_response("Event not found", status_code=404)

        serializer = self.get_serializer(event)

        return success_response(
            data=serializer.data,
            message="My event detail"
        )
        
    @action(detail=True, methods=['get'], url_path='registrations')
    def event_registrations(self, request, pk=None):
        try:
            event = self.get_queryset().get(pk=pk, created_by=request.user)
        except Event.DoesNotExist:
            return error_response("Event not found", status_code=404)

        queryset = Registration.objects.filter(event=event).select_related('user')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RegistrationSerializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="Event registrations"
            )

        serializer = RegistrationSerializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Event registrations"
        )
        
class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAdminOrSuperAdmin, IsAuthenticated]
    pagination_class = EventPagination
    filterset_fields = ['name', 'event']
    
    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

    # 🔹 LIST
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="List of tracks"
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="List of tracks"
        )

    # 🔹 RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return success_response(
            data=serializer.data,
            message="Track detail"
        )

    # 🔹 CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_create(serializer)

        return success_response(
            data=serializer.data,
            message="Track created",
            status_code=status.HTTP_201_CREATED
        )

    # 🔹 UPDATE
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Track updated"
        )

    # 🔹 PARTIAL UPDATE
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Track partially updated"
        )

    # 🔹 DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return success_response(
            data=None,
            message="Track deleted",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAdminOrSuperAdmin, IsAuthenticated]
    pagination_class = EventPagination
    filterset_fields = ['track', 'start_time']

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

    # 🔹 LIST
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="List of sessions"
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="List of sessions"
        )

    # 🔹 RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return success_response(
            data=serializer.data,
            message="Session detail"
        )

    # 🔹 CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_create(serializer)

        return success_response(
            data=serializer.data,
            message="Session created",
            status_code=status.HTTP_201_CREATED
        )

    # 🔹 UPDATE
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Session updated"
        )

    # 🔹 PARTIAL UPDATE
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return error_response(serializer.errors)

        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message="Session partially updated"
        )

    # 🔹 DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return success_response(
            data=None,
            message="Session deleted",
            status_code=status.HTTP_204_NO_CONTENT
        )