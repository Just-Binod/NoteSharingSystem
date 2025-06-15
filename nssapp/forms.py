# # from django import forms
# # from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# # from django.contrib.auth import get_user_model

# # User = get_user_model()

# # class CustomUserCreationForm(UserCreationForm):
# #     class Meta:
# #         model = User
# #         fields = ('username', 'email', 'password1', 'password2')

# # class CustomAuthenticationForm(AuthenticationForm):
# #     class Meta:
# #         model = User
# #         fields = ('username', 'password')


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model, authenticate

# User = get_user_model()

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


# class CustomAuthenticationForm(forms.Form):
#     email = forms.EmailField(label='Email', max_length=255)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     def __init__(self, request=None, *args, **kwargs):
#         self.request = request
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         email = self.cleaned_data.get('email')
#         password = self.cleaned_data.get('password')

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise forms.ValidationError("Invalid email or password")

#         self.user = authenticate(request=self.request, username=user.username, password=password)
#         if self.user is None:
#             raise forms.ValidationError("Invalid email or password")

#         return self.cleaned_data

#     def get_user(self):
#         return self.user





# #

# # forms.py
# from django import forms
# from .models import Notes
# from django.contrib.auth.models import User
# from .models import Subject

# class NotesForm(forms.ModelForm):
#     class Meta:
#         model = Notes
#         fields = ['title', 'description', 'notes_file', 'subject_id']
        
#         # You can customize widgets if needed
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#         }
    
#     # If you want to filter the subject choices based on some condition
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(NotesForm, self).__init__(*args, **kwargs)
#         if user:
#             self.fields['subject_id'].queryset = Subject.objects.filter(some_condition_based_on_user=user)





#
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Notes, Subject

User = get_user_model()

## User Authentication Forms ##

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user = authenticate(
                    request=self.request,
                    username=user.username,
                    password=password
                )
                if self.user is None:
                    raise forms.ValidationError("Invalid email or password")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")

        return self.cleaned_data

    def get_user(self):
        return self.user

## Notes Form with Proper Subject Filtering ##

# class NotesForm(forms.ModelForm):
#     class Meta:
#         model = Notes
#         fields = ['title', 'description', 'notes_file', 'subject_id']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={
#                 'rows': 4,
#                 'class': 'form-control',
#                 'placeholder': 'Enter detailed description'
#             }),
#             'notes_file': forms.FileInput(attrs={'class': 'form-control'}),
#             'subject_id': forms.Select(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'subject_id': 'Subject'
#         }
    
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(NotesForm, self).__init__(*args, **kwargs)
        
#         if user:
#             # Filter subjects based on actual fields in your Subject model
#             # Example: filter by user's department or other relationship
#             # Replace with your actual filtering logic
#             self.fields['subject_id'].queryset = Subject.objects.filter(
#                 department=user.profile.department  # Adjust this to your actual relationship
#             ).order_by('subject_name')
            
#             # If no specific filtering needed, just show all subjects:
#             # self.fields['subject_id'].queryset = Subject.objects.all().order_by('subject_name')