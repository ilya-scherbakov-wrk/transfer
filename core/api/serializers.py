from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.models import User, UserTransaction


class ReadOnlySerializerMixin(ModelSerializer):
    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self.Meta, 'read_only_fields', [*self.fields])


class UserReadOnlySerializer(ReadOnlySerializerMixin):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )


class UserTransactionReadOnlySerializer(ReadOnlySerializerMixin):
    transaction_type = SerializerMethodField(source='get_transaction_type', read_only=True)

    class Meta:
        model = UserTransaction
        fields = (
            'amount',
            'created_at',
            'transaction_type',
        )

    def get_transaction_type(self, user_transaction):
        user = self.context['request'].user
        return user_transaction.get_transaction_type(user)


class UserTransactionSerializer(ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = (
            'recipient',
            'amount',
            'created_at',
        )
        read_only_fields = [
            'id',
        ]

    def validate(self, attrs):
        recipient = attrs.get('recipient')
        amount = attrs.get('amount')
        owner = self.context['request'].user
        errors = []

        if owner == recipient:
            errors.append('Нельзя отправить самому себе.')
        if amount > UserTransaction.get_total(owner):
            errors.append('Не достаточно средств.')

        if errors:
            raise ValidationError({'errors': errors})

        return attrs
