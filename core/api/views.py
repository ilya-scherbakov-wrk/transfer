from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.api.serializers import UserReadOnlySerializer, UserTransactionSerializer, UserTransactionReadOnlySerializer
from core.models import User, UserTransaction


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserReadOnlySerializer
    pagination_class = None

    @action(methods=['get'], detail=False, url_path='total')
    def get_total(self, request, *args, **kwargs):
        total = UserTransaction.get_total(self.request.user)
        return Response(data={'total': total}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='me')
    def get_me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)


class UserTransactionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = UserTransaction.objects.all()
    serializer_class = UserTransactionSerializer
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(Q(owner=self.request.user) | Q(recipient=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserTransactionReadOnlySerializer
        return super().get_serializer_class()
