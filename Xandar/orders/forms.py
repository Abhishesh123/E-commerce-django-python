from django.forms import ModelForm
from core.models import DeliveryAddresses


class UpdateAddress(ModelForm):
    class Meta:
        model = DeliveryAddresses
        fields = ['receiver_name', 'phone_number', 'street_address', 'city', 'pincode', 'state']