# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email or password")

        self.user = authenticate(request=self.request, username=user.username, password=password)
        if self.user is None:
            raise forms.ValidationError("Invalid email or password")

        return self.cleaned_data

    def get_user(self):
        return self.user
