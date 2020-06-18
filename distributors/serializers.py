from rest_framework import serializers
from .models import Distributor, State, District


class DistributorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Distributor

    def create(self, validated_data:dict):
        state = State.objects.get(pk=validated_data["state"])
        district = District.objects.get(pk=validated_data["district"])
        validated_data["state"], validated_data["district"] = state, district
        return Distributor(**validated_data)
        