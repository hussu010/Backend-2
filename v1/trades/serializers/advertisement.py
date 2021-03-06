from django.db import transaction

from rest_framework import serializers

from v1.constants.models import TnbcrowConstant
from v1.users.models.wallets import Wallet
from v1.core.models.asset import Asset

from ..models.advertisement import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ('uuid', 'role', 'currency', 'payment_method', 'fee',
                  'rate', 'amount', 'terms_of_trade', 'min_reputation',
                  'broadcast_trade', 'payment_windows', 'is_active', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'fee'

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']

        asset = Asset.objects.get(symbol="TNBC")

        wallet, created = Wallet.objects.get_or_create(user=context.user, asset=asset)

        amount = int(validated_data.pop('amount'))

        tnbcrow_constants = TnbcrowConstant.objects.get(title="main")

        if amount < tnbcrow_constants.minimum_escrow_amount or amount > tnbcrow_constants.maximum_escrow_amount:
            error = {'error': f'You can not escrow less than {tnbcrow_constants.minimum_escrow_amount} and more than {tnbcrow_constants.maximum_escrow_amount} TNBC.'}
            raise serializers.ValidationError(error)

        else:
            if context.data['role'] == Advertisement.SELLER:
                if wallet.get_available_balance() >= amount:
                    validated_data['amount'] = amount
                    wallet.locked += amount
                    wallet.save()

                else:
                    error = {'error': f'You only have {wallet.get_available_balance()} TNBC in your account.'}
                    raise serializers.ValidationError(error)
            else:
                validated_data['amount'] = amount

        fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee

        validated_data['fee'] = amount * fee_percentage / 100

        instance = super(AdvertisementSerializer, self).create(validated_data)
        return instance
