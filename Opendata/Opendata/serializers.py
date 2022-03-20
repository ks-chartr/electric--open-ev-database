from rest_framework import serializers
from EVUpdates.models import *


class EVLocationsListSerializer(serializers.ListSerializer):
    uid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    vendor_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    charger_type = serializers.CharField()
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    open = serializers.CharField(max_length=100)
    close = serializers.CharField(max_length=100)
    logo_url = serializers.CharField(max_length=1000)
    staff = serializers.CharField(max_length=100)
    total = serializers.CharField(max_length=100)
    available = serializers.CharField(max_length=100)
    cost_per_unit = serializers.CharField(max_length=100)
    payment_modes = serializers.CharField(max_length=100)
    contact_numbers = serializers.CharField(max_length=100)

    def create(self, validated_data):
        evlocations = [EVLocations(**item) for item in validated_data]
        return EVLocations.objects.bulk_create(evlocations)

    def update(self, instance, validated_data):
        book_mapping = {book.uid: book for book in instance}
        data_mapping = {item['uid']: item for item in validated_data}

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
    uid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    vendor_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    charger_type = serializers.CharField()
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    open = serializers.CharField(max_length=100)
    close = serializers.CharField(max_length=100)
    logo_url = serializers.CharField(max_length=1000)
    staff = serializers.CharField(max_length=100)
    total = serializers.CharField(max_length=100)
    available = serializers.CharField(max_length=100)
    cost_per_unit = serializers.CharField(max_length=100)
    payment_modes = serializers.CharField(max_length=100)
    contact_numbers = serializers.CharField(max_length=100)

    class Meta:
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
