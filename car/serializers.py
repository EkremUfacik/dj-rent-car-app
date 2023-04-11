from rest_framework import serializers
from .models import Car, Reservation


class CarSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField()
    class Meta:
        model = Car
        fields = (
            'id',
            'plate_number',
            'brand',
            'model',
            'year',
            'gear',
            "image",
            'rent_per_day',
            'availability',
            'is_available'
        )
    # Bu method u override etmek yerine staff ve normal userlar için ayrı ayrı serializerlar oluşturulup
    # View de get_serializer_class methode u override edilerek user a göre serializerlar seçilebilir.

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        if request.user and not request.user.is_staff:
            fields.pop('availability')
            fields.pop('plate_number')
        return fields


# class CarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car
#         fields = (
#             'id',
#             'brand',
#             'model',
#             'year',
#             'gear',
#             'rent_per_day',
#         )


class ReservationSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    customer_id = serializers.IntegerField(required=False)
    customer = serializers.StringRelatedField()
    car = serializers.StringRelatedField()
    car_id = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = (
            'id',
            "customer_id",
            'customer',
            'car',
            'car_id',
            'start_date',
            'end_date',
            'total_price'
        )
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Reservation.objects.all(),
        #         fields=('customer_id', 'start_date', 'end_date'),
        #         message=('You alreday have a reservation between these dates...')
        #     )
        # ]

    def get_total_price(self, obj):
        return obj.car.rent_per_day * (obj.end_date - obj.start_date).days
    
    def create(self, validated_data):
        validated_data["customer_id"] = self.context["request"].user.id
        instance = Reservation.objects.create(**validated_data)
        return instance