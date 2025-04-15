from cProfile import label

from django import forms
from .models import Costumer, User, Account , Image , Ticket
from django.contrib.auth.forms import AuthenticationForm

class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone

class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Costumer
        fields = ['title', 'description','category']
        widgets={
            'title': forms.TextInput(attrs={
                'class':'form-control',
                'id' : "con-name",

            }),
            'description': forms.Textarea(attrs={
            	'class': 'form-control',
				 'rows': '5',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),


        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }
        
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='پسورد')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='تکرار پسورد')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' , 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
            }),
            'job': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }