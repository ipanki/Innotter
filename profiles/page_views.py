from rest_framework import mixins, viewsets
from profiles.permissions import PagePermission

from profiles.serializers import CreatePageSerializer, ShowPageSerializer, EditPageSerializer
from profiles.models import Page, User


class PageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = ShowPageSerializer
    queryset = Page.objects
    permission_classes = (PagePermission,)

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


    # def list(self, request):
    #     """List all pages"""
    #     pages = Page.objects.all() if request.user.is_superuser or request.user.role == User.Roles.MODERATOR \
    #         else Page.objects.filter(owner=request.user)
    #     serializer = ShowPageSerializer(pages, many=True)
    #     return Response({'data': serializer.data})

    # def create(self, request):
    #     """Create a new page"""
    #     page = CreatePageSerializer(data=request.data)
    #     page.is_valid(raise_exception=True)
    #     profile = page.save(owner=request.user)
    #     return Response(status=status.HTTP_201_CREATED, data=CreatePageSerializer(profile).data)

    # def update(self, request, pk):
    #     page = get_object_or_404(Page, pk=pk)
    #     self.check_object_permissions(request, page)
    #     form = EditPageSerializer(data=request.data, instance=page, partial=True)
    #     form.is_valid(raise_exception=True)
    #     profile = form.save()
    #     return Response(status=status.HTTP_201_CREATED, data=EditPageSerializer(profile).data)

    # def retrieve(self, request, pk):
    #     page = get_object_or_404(Page, pk=pk)
    #     self.check_object_permissions(request, page)
    #     serializer = ShowPageSerializer(page)
    #     return Response({'data': serializer.data})
