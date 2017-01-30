from django import forms
from django.contrib.auth.models import User
from .models import Profile
#from .models import User, Profile

# for validation
def startsWithNumber(value):
    for i in range(10):
        if value.startswith(str(i)):
            return True
    return False

class feedbackForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(required=True,
                               widget=forms.Textarea)
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                max_length=50)
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        cd = self.cleaned_data
        if len(cd['username']) < 4 or len(cd['username']) > 25:
            raise forms.ValidationError(
                'Username must be between 4 and 25 characters long')
        elif startsWithNumber(cd['username']):
            raise forms.ValidationError(
                'Username must not start with a digit')
        elif not cd['username'].isalnum():
            raise forms.ValidationError(
                'Username must contain only digits and alphabets')

        return cd['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        if len(cd['password']) < 4 or len(cd['password']) > 50:
            raise forms.ValidationError(
                'Password must be between 4 and 50 characters long')

        return cd['password2']
    
class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'surname', 'phone', 'bank', 'account_number')  

    def clean_first_name(self):  
        cd = self.cleaned_data
        if len(cd['first_name']) < 3 or len(cd['first_name']) > 25:
            raise forms.ValidationError(
                'First name must be between 3 and 25 characters long')
        elif not cd['first_name'].isalpha():
            raise forms.ValidationError(
                'First name must contain only alphabets')

        return cd['first_name']

    def clean_surname(self):
        cd = self.cleaned_data
        if len(cd['surname']) < 3 or len(cd['surname']) > 25:
            raise forms.ValidationError(
                'Surname must be between 3 and 25 characters long')
        elif not cd['surname'].isalpha():
            raise forms.ValidationError(
                'Surname must contain only alphabets')

        return cd['surname']
    
    def clean_account_number(self):
        cd = self.cleaned_data
        if len(cd['account_number']) != 10:
            raise forms.ValidationError(
                'Invalid account number')
        elif not cd['account_number'].isdigit():
            raise forms.ValidationError(
                'Account number must contain only digits')
        return cd['account_number']

    def clean_phone(self):
        cd = self.cleaned_data
        if len(cd['phone']) != 11:
            raise forms.ValidationError('Invalid phone number')
        elif not cd['phone'].isdigit():
            raise forms.ValidationError('Phone number must contain only digits')
        return cd['phone']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'surname', 'phone', 'bank', 'account_number')

    
