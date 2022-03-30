from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import mixins, viewsets
from profiles.permissions import PostPermission, check_owner_page

from profiles.serializers import ShowPostSerializer, CreatePostSerializer, EditPostSerializer, \
    ReplyToPostSerializer, CommentPostSerializer
from profiles.models import Post, Page, User


class PostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ShowPostSerializer
    queryset = Post.objects
    permission_classes = (PostPermission,)

    def get_queryset(self):
        if self.action == "list":
            if not (self.request.user.is_superuser or self.request.user.role == User.Roles.MODERATOR):
                return self.queryset.filter(owner=self.request.user)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return EditPostSerializer
        if self.action == 'create':
            return CreatePostSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        page_id = serializer.validated_data.get('page_id')
        page = get_object_or_404(Page, pk=page_id)
        check_owner_page(page, self.request.user)
        serializer.save()

    @action(detail=True, methods=['post'], url_path='like')
    def post_like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        page_id = request.data.get('page_id')

        if page_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='page_id is required')

        page = get_object_or_404(Page, pk=page_id)
        check_owner_page(page, request.user)
        post.likes.add(page)
        count_likes = post.total_likes
        return Response(status=status.HTTP_200_OK, data=count_likes)

    @action(detail=True, methods=['post'], url_path='dislike')
    def post_dislike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        page_id = request.data.get('page_id')

        if page_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='page_id is required')

        page = get_object_or_404(Page, pk=page_id)
        check_owner_page(page, request.user)
        post.likes.remove(page)
        count_likes = post.total_likes
        return Response(status=status.HTTP_200_OK, data=count_likes)

    @action(detail=True, methods=['get'], url_path='liked-post')
    def show_liked_post(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        check_owner_page(page, request.user)
        liked_post = Post.objects.filter(likes=page)
        serializer = ShowPostSerializer(liked_post, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=['post'], url_path='reply')
    def reply_to_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment = ReplyToPostSerializer(data=request.data)
        comment.is_valid(raise_exception=True)
        page_id = request.data.get('page_id')

        page = get_object_or_404(Page, pk=page_id)
        check_owner_page(page, request.user)
        new_comment = comment.save(page=page, reply_to=post)
        return Response(status=status.HTTP_201_CREATED, data=CommentPostSerializer(new_comment).data)

