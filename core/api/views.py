from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.api.serializers import UserReadOnlySerializer, UserTransactionSerializer
from core.models import User, UserTransaction


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserReadOnlySerializer
    pagination_class = None

    @action(methods=['get'], detail=False, url_path='total')
    def get_total(self, request, *args, **kwargs):
        user = self.request.user
        total = UserTransaction.get_total(user)
        return Response(data={'total': total}, status=status.HTTP_200_OK)


class UserTransactionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = UserTransaction.objects.all()
    serializer_class = UserTransactionSerializer
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
