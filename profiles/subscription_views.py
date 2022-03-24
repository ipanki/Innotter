from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from profiles.serializers import ShowFollowerSerializer
from profiles.models import Page


class SubscriptionViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk):
        page = get_object_or_404(Page, pk=pk)

        try:
            if page.is_private:
                page.follow_requests.add(request.user)
                return Response(status=status.HTTP_201_CREATED, data="Subscription request sent")
            else:
                page.followers.add(request.user)
                return Response(status=status.HTTP_201_CREATED, data="Subscribed")

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    @action(detail=True, methods=['get'], url_path='requests')
    def show_following_requests(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = ShowFollowerSerializer(page)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'], url_path='accept-request')
    def accept_following_request(self, request, pk):
        """Single subscription approval"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')

        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='user_id is required')

        for user in page.follow_requests.all():
            if user.id == user_id:
                page.followers.add(user)
                page.follow_requests.remove(user)
                return Response(status=status.HTTP_200_OK, data='Request accepted')

        return Response(status=status.HTTP_404_NOT_FOUND, data='Request not found')

    @action(detail=True, methods=['post'], url_path='accept-requests')
    def accept_following_requests(self, request, pk):
        """Accept all subscriptions"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if page.follow_requests.all() is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Requests not found')

        for user in page.follow_requests.all():
            page.followers.add(user)
            page.follow_requests.remove(user)

        return Response(status=status.HTTP_200_OK, data='Requests accepted')

    @action(detail=True, methods=['post'], url_path='deny-request')
    def deny_following_request(self, request, pk):
        """Deny 1 subscription request"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')

        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='user_id is required')

        for user in page.follow_requests.all():
            if user.id == user_id:
                page.follow_requests.remove(user)
                return Response(status=status.HTTP_200_OK, data='Request denied')

    @action(detail=True, methods=['post'], url_path='deny-requests')
    def deny_following_requests(self, request, pk):
        """Deny all subscription requests"""
        page = get_object_or_404(Page, pk=pk)

        if page.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        for user in page.follow_requests.all():
            page.follow_requests.remove(user)

        return Response(status=status.HTTP_200_OK, data='Requests denied')
