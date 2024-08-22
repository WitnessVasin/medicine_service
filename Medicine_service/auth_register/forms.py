from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from string import ascii_letters

from source.settings import INVITE_CODE
from .models import Account
from doctor.models import Doctor
from user.models import User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'phone_number', 'password', 'invite_code']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 999 99 99'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'invite_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Инвайт код (если вы врач)'}),
        }

    name = forms.CharField(max_length=60, required=True, label='Ваше имя',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    second_name = forms.CharField(max_length=60, required=True, label='Ваша фамилия',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    middle_name = forms.CharField(max_length=60, required=False, label='Ваше отчество',
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}))
    birthday = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        spec_symbols = ['_', '/', '.', ',', '-', '=', '']
        if len(password) > 6 and set(spec_symbols).intersection(set(password)):
            return password
        raise ValidationError(
            f'Пароль должен иметь больше 6 символов и содержать спец-символы: {" ".join(spec_symbols)}')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ascii_symbols = ascii_letters
        if all(map(lambda x: x in ascii_symbols, username)):
            return username
        raise ValidationError('Имя должно состоять из латинских букв')

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code:
            if invite_code == INVITE_CODE:
                return invite_code
            else:
                raise ValidationError('Вы ввели неверный инвайт-код')

    def save(self, commit=True):
        account = super().save(commit=False)
        invite_code = self.cleaned_data.get('invite_code')
        key_list = ['name', 'second_name', 'middle_name', 'birthday', 'photo']
        account_data = {i: self.cleaned_data.get(i) for i in key_list}
        if invite_code == INVITE_CODE:
            doctor_group, flag = Group.objects.get_or_create(name='Doctor')
            account.is_doctor = True
            doctor_data = Doctor.objects.create(**account_data)
            account.doctor_data = doctor_data
            account.groups.add(doctor_group)
        else:
            user_data = User.objects.create(**account_data)
            account.user_data = user_data
        if commit:
            account.set_password(self.cleaned_data['password'])
            account.slug = slugify(account.username)
            account.save()
        return account


