from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from profiles.permissions import PostPermission, check_owner_page

from profiles.serializers import ShowPostSerializer, CreatePostSerializer, EditPostSerializer, \
    ReplyToPostSerializer, CommentPostSerializer
from profiles.models import Post, Page, User


class PostViewSet(ViewSet):
    permission_classes = (PostPermission,)

    def list(self, request):
        """List all post"""
        posts = Post.objects.all() if request.user.is_superuser or request.user.role == User.Roles.MODERATOR \
            else Post.objects.filter(page__owner=request.user)
        serializer = ShowPostSerializer(posts, many=True)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'], url_path='create-post')
    def create_post(self, request, pk):
        """Create a new post"""
        page = get_object_or_404(Page, pk=pk)
        check_owner_page(page, request.user)
        post = CreatePostSerializer(data=request.data)
        post.is_valid(raise_exception=True)
        new_post = post.save(page=page)
        return Response(status=status.HTTP_201_CREATED, data=ShowPostSerializer(new_post).data)

    def update(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        form = EditPostSerializer(data=request.data, instance=post, partial=True)
        form.is_valid(raise_exception=True)
        profile = form.save()
        return Response(status=status.HTTP_201_CREATED, data=EditPostSerializer(profile).data)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

