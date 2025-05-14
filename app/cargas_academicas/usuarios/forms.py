from django import forms
from django.contrib.auth.models import User

from .models import Alumno

class FormAlumno(forms.ModelForm):

    class Meta:
        model = Alumno
        exclude = ['usuario']

class FormUser(forms.ModelForm):
    re_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'email','re_password']

    def clean_password(self, *args, **kwargs):
        if self.data['password'] != self.data['re_password']:
            raise forms.ValidationError('Las contraseñas no coinciden', code='password_no_coniciden')
        return self.data['password']

    def save(self, commit = True):
        user = super(FormUser, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user