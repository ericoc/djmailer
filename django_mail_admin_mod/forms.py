from django import forms

from .models import OutgoingEmail


class OutgoingEmailAdminForm(forms.ModelForm):

    class Meta:
        model = OutgoingEmail
        fields = '__all__'
