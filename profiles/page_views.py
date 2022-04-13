from rest_framework import mixins, viewsets
from profiles.permissions import PagePermission
from rest_framework import filters

from profiles.serializers import CreatePageSerializer, ShowPageSerializer, EditPageSerializer
from profiles.models import Page, User


class PageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = ShowPageSerializer
    queryset = Page.objects
    permission_classes = (PagePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '=uuid', '=tags__name', 'owner__username']

    def get_queryset(self):
        if self.action == "list":
            if not (self.request.user.is_superuser or self.request.user.role == User.Roles.MODERATOR):
                return self.queryset.filter(owner=self.request.user)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePageSerializer
        if self.action == 'update':
            return EditPageSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
