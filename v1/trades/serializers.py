from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from .models import TradePost, TradeRequest, ActiveTrade, CompletedTrade


class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePost
        fields = ('uuid', 'owner_role', 'currency',
                  'payment_method', 'exchange', 'margin',
                  'rate', 'amount', 'terms_of_trade', 'min_reputation',
                  'broadcast_trade', 'is_active', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'rate',

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']
        user = context.user
        amount = int(context.data['amount'])
        if context.data['owner_role'] == '1':
            if user.get_user_balance() >= amount:
                user.locked += amount
                user.save()
            else:
                error = {'error': 'Please load enough coins into your account'}
                raise serializers.ValidationError(error)
        instance = super(TradePostSerializer, self).create(validated_data)
        return instance


class TradeRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'amount', 'rate', 'message', 'status', 'created_at', 'updated_at', 'expires_at')
        read_only_fields = 'created_at', 'updated_at', 'status', 'rate', 'expires_at'

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']
        amount = int(context.data['amount'])

        if self.validated_data['post'].amount <= amount:
            error = {'error': 'Amount has exceeded the trade amount'}
            raise serializers.ValidationError(error)

        user = context.user
        post = self.validated_data['post']
        if post.owner_role == 0:
            if user.get_user_balance() >= amount:
                user.locked += amount
                user.save()
            else:
                error = {'error': 'Please load enough coins into your account'}
                raise serializers.ValidationError(error)
            post.amount -= amount
            post.save()

        instance = super(TradeRequestCreateSerializer, self).create(validated_data)

        return instance


class TradeRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'status', 'rate', 'amount', 'message', 'created_at', 'updated_at', 'expires_at')
        read_only_fields = 'uuid', 'created_at', 'updated_at', 'post', 'amount', 'message', 'rate', 'expires_at'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        if self.instance.expires_at < timezone.now():
            error = {'error': 'OOps!! Trade request is expired'}
            raise serializers.ValidationError(error)
        elif self.instance.status == 1:
            error = {'error': 'Trade request already accepted'}
            raise serializers.ValidationError(error)
        elif self.instance.status == 2:
            error = {'error': 'You cannot undo a rejected trade request'}
            raise serializers.ValidationError(error)
        elif self.instance.status == 3:
            error = {'error': 'You cannot undo a cancelled trade request'}
            raise serializers.ValidationError(error)

        instance = super(TradeRequestUpdateSerializer, self).update(instance, validated_data)
        if 'status' in context.data:
            if context.data['status'] == '1':
                instance.post.amount -= int(context.data['amount'])
                instance.post.save()
                obj, created = ActiveTrade.objects.get_or_create(post=instance.post,
                                                                 initiator=instance.initiator,
                                                                 amount=instance.amount,
                                                                 rate=instance.rate,
                                                                 payment_windows=instance.payment_windows,
                                                                 terms_of_trade=instance.terms_of_trade,
                                                                 payment_method=instance.payment_method)
            elif context.data['status'] == '2' or context.data['status'] == '3':
                if self.instance.post.owner_role == 0:
                    user = context.user
                    user.locked -= self.instance.amount
                    user.save()
        return instance


class ActiveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveTrade
        fields = ('uuid', 'post', 'amount', 'initiator_confirmed', 'owner_confirmed', 'created_at', 'updated_at', 'status')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        payment_windows_expires_at = instance.created_at + timedelta(minutes=instance.payment_windows)

        if self.instance.status == 1 or self.instance.status == 2 or self.instance.status == 3 or self.instance.status == 4 or self.instance.status == 5:
            error = {'error': 'You cannot undo the action'}
            raise serializers.ValidationError(error)

        if 'status' in context.data:
            if context.data['status'] == '1' or context.data['status'] == '2' or context.data['status'] == '5':
                error = {'error': 'You cannot set this status'}
                raise serializers.ValidationError(error)
            elif payment_windows_expires_at > timezone.now():
                if (instance.post.owner_role == 0 and context.data['status'] == '4') or (instance.post.owner_role == 1 and context.data['status'] == '3'):
                    error = {'error': 'Payment window must expire before cancelling the ActiveTrade'}
                    raise serializers.ValidationError(error)

        instance = super(ActiveTradeSerializer, self).update(instance, validated_data)
        if instance.initiator_confirmed and instance.owner_confirmed:
            if instance.post.owner_role == 0:
                buyer = instance.post.owner
                seller = instance.initiator
            else:
                seller = instance.post.owner
                buyer = instance.initiator
            user = self.context['request'].user
            user.loaded += instance.amount
            user.locked -= instance.amount
            user.save()
            CompletedTrade.objects.create(buyer=buyer, seller=seller, amount=instance.amount)
        return instance


class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradePost
        fields = ('amount', )
