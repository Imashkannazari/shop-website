from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SingUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارد کنید'}))
    last_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد کنید'}))
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید'}))
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'}))
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 رقم خود را وارد کنید'
            }
        ))
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'type': 'password',
                'placeholder': 'دوباره رمز خود را وارد کنید'
            }
        ))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = 'نام کاربری باید یکتا باشد.'
        self.fields['password1'].help_text = (
            'رمز عبور باید حداقل 8 کاراکتر باشد، خیلی ساده یا کاملا عددی نباشد '
            'و شبیه اطلاعات شخصی شما انتخاب نشود.'
        )
        self.fields['password2'].help_text = 'برای تایید، رمز عبور را دقیقا تکرار کنید.'

        self.fields['username'].error_messages.update({
            'required': 'وارد کردن نام کاربری الزامی است.',
            'unique': 'این نام کاربری قبلا ثبت شده است.',
        })
        self.fields['password1'].error_messages.update({
            'required': 'وارد کردن رمز عبور الزامی است.',
        })
        self.fields['password2'].error_messages.update({
            'required': 'تکرار رمز عبور الزامی است.',
        })

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('این نام کاربری قبلا ثبت شده است.')
        return username
