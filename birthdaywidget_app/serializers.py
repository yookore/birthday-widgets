from rest_framework import serializers

class BirthdaySerializer(serializers.Serializer):

    firstname                       = serializers.CharField(read_only=True)
    lastname                        = serializers.CharField(read_only=True)
    username                        = serializers.CharField(read_only=True)
    birthdate                       = serializers.DateTimeField(read_only=True)
    userid                          = serializers.UUIDField(read_only=True)
    avatarurl                       = serializers.CharField(read_only=True)