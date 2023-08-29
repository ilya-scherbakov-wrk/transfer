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

    @staticmethod
    def get_user(user_id):
        return User.objects.filter(id=user_id).first()

    @action(methods=['get'], detail=True, url_path='total')
    def get_total(self, request, *args, **kwargs):
        user = self.get_user(kwargs['pk'])
        if not user:
            return Response({'error': f'Пользователя не существует.'}, status=status.HTTP_400_BAD_REQUEST)

        total = UserTransaction.get_total(user)
        return Response(data={'total': total}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='story')
    def get_story(self, request, *args, **kwargs):
        user = self.get_user(kwargs['pk'])
        if not user:
            return Response({'error': f'Пользователя не существует.'}, status=status.HTTP_400_BAD_REQUEST)

        user_transaction_story_qs = UserTransaction.objects.filter(user_id=user.id)
        serializer = UserTransactionSerializer(user_transaction_story_qs, many=True)
        return Response(serializer.data)


class UserTransactionViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserTransaction.objects.all()
    serializer_class = UserTransactionSerializer
    pagination_class = None
