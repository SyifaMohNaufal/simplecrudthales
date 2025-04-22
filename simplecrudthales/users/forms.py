from django import forms
from .models import User
from django.core.exceptions import ValidationError

def exact_length(length):
    def validator(value):
        if len(value) != length:
            raise ValidationError(f'This field must be exactly {length} characters long.')
    return validator


class UserForm(forms.ModelForm):
    ktp = forms.CharField(
        label="KTP",
        validators=[exact_length(16)],  # require exactly 6 characters
        widget=forms.TextInput(attrs={
            'maxlength': '16',  # for frontend help
            'minlength': '16'   # optional for frontend
        })
    )

    phone = forms.CharField(
        min_length=9,
        max_length=13,
        widget=forms.TextInput(attrs={
            'minlength': '9',
            'maxlength': '13'
        })
    )

    class Meta:
        model = User
        fields = ['full_name',
                  'email',
                  'phone',
                  'gender',
                  'ktp',
                  'address',
                  'province',
                  'city',
                  'birth_day',
                  'birth_place',
                  'nationality' 
                ]
