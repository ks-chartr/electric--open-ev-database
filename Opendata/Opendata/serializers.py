import json
from rest_framework import serializers
from EVUpdates.models import *


def charger_type_validator(charger_type):
    for charger_ in charger_type:
        for field in ["available", "capacity", "cost_per_unit", "diagram", "total", "type"]:
            if field not in charger_.keys():
                raise serializers.ValidationError(f"{field} not given in charger type")


def coordinates_validator(coordinates):
    for field in ['latitude', 'longitude']:
        if field not in coordinates.keys():
            raise serializers.ValidationError(f"{field} not given in charger type")


class EVLocationsListSerializer(serializers.ListSerializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    vendor = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    coordinates = serializers.JSONField(validators=[coordinates_validator])
    charger_type = serializers.JSONField(validators=[charger_type_validator])
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    open = serializers.CharField(max_length=100)
    close = serializers.CharField(max_length=100)
    logo = serializers.CharField(max_length=1000, allow_blank=True)
    staff = serializers.CharField(max_length=100)
    total = serializers.CharField(max_length=100)
    available = serializers.CharField(max_length=100)
    payment_modes = serializers.CharField(max_length=100)
    contact_numbers = serializers.JSONField()
    postal_code = serializers.CharField(max_length=100)

    def create(self, validated_data):
        evlocations = [EVLocations(**item) for item in validated_data]
        return EVLocations.objects.bulk_create(evlocations)

    def update(self, instance, validated_data):
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))
        return ret


class EVLocationsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    vendor = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    coordinates = serializers.JSONField(validators=[coordinates_validator])
    charger_type = serializers.JSONField(validators=[charger_type_validator])
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    open = serializers.CharField(max_length=100)
    close = serializers.CharField(max_length=100)
    logo = serializers.CharField(max_length=1000, allow_blank=True)
    staff = serializers.CharField(max_length=100)
    total = serializers.CharField(max_length=100)
    available = serializers.CharField(max_length=100)
    payment_modes = serializers.CharField(max_length=100)
    contact_numbers = serializers.JSONField()
    postal_code = serializers.CharField(max_length=100)

    class Meta:
        model = EVLocations
        list_serializer_class = EVLocationsListSerializer

    def create(self, validated_data):
        added_data = EVLocations(**validated_data)
        added_data.save()
        return added_data

    def update(self, instance, validated_data):
        instance.charger_type = validated_data.get('charger_type', instance.charger_type)
        instance.available = validated_data.get('content', instance.available)
        instance.save()
        return instance
