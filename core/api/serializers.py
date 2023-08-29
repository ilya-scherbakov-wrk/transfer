from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from core.models import User, UserTransaction


class UserReadOnlySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self.Meta, 'read_only_fields', [*self.fields])


class UserTransactionSerializer(ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = ('amount', 'mark', 'created_at', )
        read_only_fields = ['id', ]

    def validate(self, attrs):
        amount = attrs.get('amount')
        mark = attrs.get('mark')

        if mark == UserTransaction.WITHDRAW:
            if amount > UserTransaction.get_total(self.context['request'].user):
                raise ValidationError({'error': 'Не достаточно средств.'})

        return attrs
