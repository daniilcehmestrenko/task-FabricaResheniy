from rest_framework import serializers

from .models import MailingList, Client

class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MailingListStatSerializer(serializers.ModelSerializer):
    count_message = serializers.IntegerField()
    status_message = serializers.BooleanField()
    
    class Meta:
        model = MailingList
        fields = '__all__'


class MailingListStatDetailSerializer(serializers.ModelSerializer):
    count_message = serializers.IntegerField()
    count_not_sent_messages = serializers.IntegerField()
    count_sent_messages = serializers.IntegerField()

    class Meta:
        model = MailingList
        fields = '__all__'