from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from profiles.serializers import CreatePageSerializer, ShowPostSerializer, CreatePostSerializer, EditPostSerializer
from profiles.models import Post, Page


class PostViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """List all post"""
        pages = Post.objects.all() if request.user.is_superuser else Post.objects.filter(page__owner=request.user)
        serializer = ShowPostSerializer(pages, many=True)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'], url_path='create-post')
    def create_post(self, request, pk):
        """Create a new post"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post = CreatePostSerializer(data=request.data)
        post.is_valid(raise_exception=True)
        new_post = post.save(page=page)
        return Response(status=status.HTTP_201_CREATED, data=ShowPostSerializer(new_post).data)

    def update(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        form = EditPostSerializer(data=request.data, instance=post, partial=True)
        form.is_valid(raise_exception=True)
        profile = form.save()
        return Response(status=status.HTTP_201_CREATED, data=EditPostSerializer(profile).data)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='like')
    def post_like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        page_id = request.data.get('page_id')

        if page_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='page_id is required')

        page = get_object_or_404(Page, pk=page_id)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

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

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.likes.remove(page)
        count_likes = post.total_likes
        return Response(status=status.HTTP_200_OK, data=count_likes)

    @action(detail=True, methods=['get'], url_path='liked-post')
    def show_liked_post(self, request, pk):
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        liked_post = Post.objects.filter(likes=page)
        serializer = ShowPostSerializer(liked_post, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
