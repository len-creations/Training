from django import forms
from .models import User,Profile
from django.core.validators import FileExtensionValidator

class profileupdateform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'team', 'facility', 'staffnumber', 'designation', 'email', 'age']

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)  # Pop user_instance from kwargs
        super().__init__(*args, **kwargs)

        readonly_fields = [ 'email']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True

        if user_instance:
            # Prefill the 'email' field with user's email address
            self.fields['email'].initial = user_instance.email

class UserProfileForm(forms.ModelForm):
    MAX_FILE_SIZE_MB = 6

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic and profile_pic.size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"File size must be less than {self.MAX_FILE_SIZE_MB} MB")
        return profile_pic

    class Meta:
        model = Profile
        fields = ['profile_pic',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].validators.append(
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        )






    