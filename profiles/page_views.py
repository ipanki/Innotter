from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from profiles.serializers import CreatePageSerializer, ShowPageSerializer, EditPageSerializer
from profiles.models import Page


class PageViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """List all pages"""
        pages = Page.objects.all() if request.user.is_superuser else Page.objects.filter(owner=request.user)
        serializer = ShowPageSerializer(pages, many=True)
        return Response({'data': serializer.data})

    def create(self, request):
        """Create a new page"""
        page = CreatePageSerializer(data=request.data)
        page.is_valid(raise_exception=True)
        profile = page.save(owner=request.user)
        return Response(status=status.HTTP_201_CREATED, data=CreatePageSerializer(profile).data)

    def update(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        form = EditPageSerializer(data=request.data, instance=page, partial=True)
        form.is_valid(raise_exception=True)
        profile = form.save()
        return Response(status=status.HTTP_201_CREATED, data=EditPageSerializer(profile).data)

    def retrieve(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = ShowPageSerializer(page)
        return Response({'data': serializer.data})
