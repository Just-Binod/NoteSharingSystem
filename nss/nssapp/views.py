from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from datetime import date
from datetime import datetime
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notes, Subject
from mimetypes import guess_type

from .models import Notes, Subject, Category  # make sure these are imported
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
#mdiddleware kolagi

from .middlewares import auth,guest
# views.py

from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.
def nav(request):
    datetime=datetime.datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    return render(request,'nav.html',{'datetime':datetime,'greet':msg})



def usernav(request):
    datetime=datetime.datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    return render(request,'usernav.html',{'datetime':datetime,'greet':msg})


def home(request):
    notes = Notes.objects.all().order_by('upload_date')
    return render(request,'home.html',{'notes': notes})





# @guest
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})


#
#
#updated register view for email auth
###
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.auth.tokens import default_token_generator
# from .forms import CustomUserCreationForm

# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Deactivate until email is verified
#             user.save()

#             # Generate activation link
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')

#             # Render activation email template
#             subject = "Activate Your Account"
#             message = render_to_string('activation_email.html', {
#                 'user': user,
#                 'activation_link': activation_link,
#             })

#             # Send email
#             send_mail(subject, message, 'your_email@gmail.com', [user.email])

#             messages.success(request, "Account created! Check your email to activate your account.")
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})





#$#
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until activation
            user.save()
            send_activation_email(user, request)
            messages.success(request, "Registration successful! Check your email to activate.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

#$#

###
###
#ew view--activation view
###
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(f"Found user: {user.username}, is_active: {user.is_active}")  # Debug
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(f"Error decoding UID or finding user: {e}")  # Debug
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()  # Ensure save is called
        print(f"User activated: {user.username}, new is_active: {user.is_active}")  # Debug
        messages.success(request, "Your account has been activated! You can now log in.")
    else:
        print(f"Token validation failed for user: {user}, token: {token}")  # Debug
        messages.error(request, "Activation link is invalid or expired.")

    return redirect("login")
###


# @guest
# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             if user.is_superuser:
#                 return redirect('adminpage')
#             else:
#                 return redirect('dashboard')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'login.html', {'form': form})

###
#updated login view, block the in active
###
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"Authenticated user: {user}, is_active: {user.is_active if user else None}")  # Debug
            if user and not user.is_active:
                messages.error(request, "Please activate your account first.")
                return redirect("login")
            login(request, user)
            if user.is_superuser:
                return redirect("adminpage")
            else:
                return redirect("dashboard")
        else:
            print(f"Form errors: {form.errors}")  # Debug
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

###

def adminpage(request):
    return render(request,'adminpage.html')

####
#email sending code activation mail
###
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_activation_email(user, request):
    subject = "Activate Your Account"
    from_email = "yourmail@gmail.com"  # Replace with your email
    recipient_list = [user.email]

    # Generate activation link (relative or local for dev)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"/note/activate/{uid}/{token}/"  # Relative URL

    # For local testing, you can use:
    # activation_link = f"http://127.0.0.1:8000{note/activate/{uid}/{token}/"  # Uncomment for local dev

    html_content = render_to_string("activation_email.html", {
        'user': user,
        'activation_link': request.build_absolute_uri(activation_link),  # Builds full URL
    })

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
###



@auth 
@login_required
def dashboard_view(request):
    notes = Notes.objects.all()
    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    
    return render(request,'dashboard.html',{'notes':notes,'datetime':date,'greet':msg})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    return render(request,'profile.html',{'datetime':date,'greet':msg})

#
def profile1(request):
    return render(request,'profile1.html')

# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import NotesForm
# from .models import Notes
# from django.contrib.auth.decorators import login_required
# #
# @login_required
# def create_note(request):
#     if request.method == 'POST':
#         form = NotesForm(request.POST, request.FILES, user=request.user)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user_id = request.user  # Set the user
#             note.save()
#             return redirect('note_detail', note_id=note.note_id)
#     else:
#         form = NotesForm(user=request.user)
    
#     return render(request, 'create_note.html', {'form': form})

# @login_required
# def note_detail(request, note_id):
#     note = get_object_or_404(Notes, note_id=note_id)
#     return render(request, 'note_detail.html', {'note': note})

# @login_required
# def note_list(request):
#     notes = Notes.objects.filter(user_id=request.user)
#     return render(request, 'note_list.html', {'notes': notes})

# #
# from django.shortcuts import render, redirect
# from .models import Notes, Subject
# from django.contrib.auth.decorators import login_required

# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.all()  # Get all subjects for the dropdown
    
#     if request.method == 'POST':
#         try:
#             # Get form data
#             title = request.POST['title']
#             subject_id = request.POST['subject_id']
#             description = request.POST['description']
#             notes_file = request.FILES.get('notes_file')
            
#             # Create new note
#             note = Notes(
#                 title=title,
#                 description=description,
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 subject_id_id=subject_id
#             )
#             note.save()
            
#             return render(request, 'upload_notes.html', {
#                 'subjects': subjects,
#                 'error': 'no'
#             })
            
#         except Exception as e:
#             print(e)
#             return render(request, 'upload_notes.html', {
#                 'subjects': subjects,
#                 'error': 'yes'
#             })
    
#     return render(request, 'upload_notes.html', {
#         'subjects': subjects
#     })

from django.shortcuts import render, redirect
from .models import Notes, Subject
from django.contrib.auth.decorators import login_required

# @login_required    
# def upload_notes(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     error=" "
#     if request.method=="POST":
#         b=request.POST['branch']
#         s=request.POST['subject']
#         n=request.FILES['notesfile']
#         f=request.POST['filetype']
#         d=request.POST['description']
#         u=User.objects.filter(username=request.user.username).first()
#         try:
#             user=Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,filetype=f,description=d,status='pending')
#             error="no"
#         except:
#             error="yes"
#     d={'error':error}
#     return render(request,'upload_notes.html',d)

# views.py





#
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import Category, Subject, Notes

# @login_required
# def upload_notes(request):
#     if request.method == 'POST':
#         try:
#             title = request.POST['title']
#             category = request.POST.get('category')
#             subject_name = request.POST['subject_name']
#             description = request.POST['description']
#             notes_file = request.FILES['notes_file']
#             upload_date_str = request.POST.get('upload_date')

#             # Validate file type
#             allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
#             if notes_file.content_type not in allowed_types:
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Only PDF, JPG, and PNG files are allowed',
#                     'form_data': request.POST,  # Preserve form data
#                 })

#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#                 if upload_date > datetime.now().date():
#                     return render(request, 'upload_notes.html', {
#                         'error': 'yes',
#                         'error_message': 'Date cannot be in the future',
#                         'form_data': request.POST,  # Preserve form data
#                     })
#             except (ValueError, TypeError):
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Invalid date format',
#                     'form_data': request.POST,  # Preserve form data
#                 })

#             # Create or get default category
#             default_category, _ = Category.objects.get_or_create(
#                 category_name='General',
#                 defaults={'category_code': 'GEN'}
#             )

#             # Create or get subject with the required category
#             subject, _ = Subject.objects.get_or_create(
#                 subject_name=subject_name,
#                 defaults={'category_id': default_category}
#             )

#             # Create the note
#             note = Notes(
#                 title=title,
#                 category=category,
#                 description=description,
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 subject_id=subject,
#                 upload_date=upload_date
#             )
#             note.save()

#             return render(request, 'upload_notes.html', {'success': True})

#         except Exception as e:
#             return render(request, 'upload_notes.html', {
#                 'error': 'yes',
#                 'error_message': str(e),
#                 'form_data': request.POST,  # Preserve form data
#             })

#     # For GET requests, set default form data with today's date
#     form_data = {
#         'title': '',
#         'category': '',
#         'subject_name': '',
#         'description': '',
#         'upload_date': date.today().isoformat(),  # Sets to 2025-06-16
#     }
#     return render(request, 'upload_notes.html', {'form_data': form_data})
# #

#
# Add this to the top if not already present




#upload note for user

# ##
# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.select_related('category_id').all()
    
#     if request.method == 'POST':
#         form_data = {
#             'title': request.POST.get('title'),
#             'subject': request.POST.get('subject'),  # Should be subject ID
#             'description': request.POST.get('description'),
#             'upload_date': request.POST.get('upload_date'),
#         }
        
#         try:
#             # Validate required fields
#             if not all([form_data['title'], form_data['subject'], form_data['description']]):
#                 raise ValueError("All required fields must be filled")
            
#             # Get subject instance
#             try:
#                 subject = Subject.objects.get(pk=form_data['subject'])
#             except Subject.DoesNotExist:
#                 raise ValueError("Selected subject does not exist")
            
#             # Handle file upload
#             if 'notes_file' not in request.FILES:
#                 raise ValueError("No file was uploaded")
            
#             notes_file = request.FILES['notes_file']
            
#             # Validate file type
#             allowed_types = [
#                 'application/pdf',
#                 'image/jpeg',
#                 'image/png',
#                 'application/msword',
#                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#             ]
            
#             if notes_file.content_type not in allowed_types:
#                 raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")
            
#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
#                 if upload_date > timezone.now().date():
#                     raise ValueError("Date cannot be in the future")
#             except (ValueError, TypeError):
#                 raise ValueError("Invalid date format")
            
#             # Create and save note
#             note = Notes(
#                 title=form_data['title'],
#                 subject_id=subject,
#                 description=form_data['description'],
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 upload_date=upload_date
#             )
#             note.save()
            
#             messages.success(request, "Notes uploaded successfully!")
#             return redirect('view_notes')  # Redirect to notes listing
            
#         except Exception as e:
#             messages.error(request, str(e))
#             return render(request, 'upload_notes.html', {
#                 'form_data': form_data,
#                 'subjects': subjects,
#                 'field_errors': {
#                     'title': not form_data.get('title'),
#                     'subject': not form_data.get('subject'),
#                     'description': not form_data.get('description'),
#                 }
#             })
    
#     # GET request - show empty form
#     return render(request, 'upload_notes.html', {
#         'form_data': {
#             'title': '',
#             'subject': '',
#             'description': '',
#             'upload_date': timezone.now().date().isoformat(),
#         },
#         'subjects': subjects
#     })
# ##







#
# 
# 
# 
# 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Subject, Notes
from datetime import datetime

@login_required
def upload_notes(request):
    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    
   
    subjects = Subject.objects.select_related('category_id').all()
    field_errors = {}

    if request.method == 'POST':
        form_data = {
            'title': request.POST.get('title', '').strip(),
            'subject': request.POST.get('subject', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'upload_date': request.POST.get('upload_date', '').strip(),
        }

        try:
            if not form_data['title']:
                field_errors['title'] = True
                raise ValueError("Title is required")
            if not form_data['subject']:
                field_errors['subject'] = True
                raise ValueError("Subject is required")
            if not form_data['description']:
                field_errors['description'] = True
                raise ValueError("Description is required")

            try:
                upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
                if upload_date > timezone.now().date():
                    field_errors['upload_date'] = True
                    raise ValueError("Date cannot be in the future")
            except (ValueError, TypeError):
                field_errors['upload_date'] = True
                raise ValueError("Invalid date format")

            try:
                subject_id = int(form_data['subject'])
                subject = Subject.objects.get(pk=subject_id)
            except (Subject.DoesNotExist, ValueError, TypeError):
                field_errors['subject'] = True
                raise ValueError("Invalid subject selected")

            if 'notes_file' not in request.FILES:
                field_errors['notes_file'] = True
                raise ValueError("No file uploaded")

            notes_file = request.FILES['notes_file']
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/png',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            if notes_file.content_type not in allowed_types:
                field_errors['notes_file'] = True
                raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")

            if notes_file.size > 10 * 1024 * 1024:
                field_errors['notes_file'] = True
                raise ValueError("File size exceeds 10MB limit")

            note = Notes(
                title=form_data['title'],
                subject_id=subject,
                description=form_data['description'],
                notes_file=notes_file,
                user_id=request.user,
                upload_date=upload_date
            )
            note.save()

            messages.success(request, "Notes uploaded successfully!")
            return redirect('upload_notes')

        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'upload_notes.html', {
                'form_data': form_data,
                'subjects': subjects,
                'field_errors': field_errors
            })

    return render(request, 'upload_notes.html', {
        'datetime': date,
        'greet': msg,
        'form_data': {
            'title': '',
            'subject': '',
            'description': '',
            'upload_date': timezone.now().date().isoformat()
        },
        'subjects': subjects,
        'field_errors': {}
    })


#  


@login_required
def upload_notes_admin(request):
    subjects = Subject.objects.select_related('category_id').all()
    field_errors = {}

    if request.method == 'POST':
        form_data = {
            'title': request.POST.get('title', '').strip(),
            'subject': request.POST.get('subject', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'upload_date': request.POST.get('upload_date', '').strip(),
        }

        try:
            if not form_data['title']:
                field_errors['title'] = True
                raise ValueError("Title is required")
            if not form_data['subject']:
                field_errors['subject'] = True
                raise ValueError("Subject is required")
            if not form_data['description']:
                field_errors['description'] = True
                raise ValueError("Description is required")

            try:
                upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
                if upload_date > timezone.now().date():
                    field_errors['upload_date'] = True
                    raise ValueError("Date cannot be in the future")
            except (ValueError, TypeError):
                field_errors['upload_date'] = True
                raise ValueError("Invalid date format")

            try:
                subject_id = int(form_data['subject'])
                subject = Subject.objects.get(pk=subject_id)
            except (Subject.DoesNotExist, ValueError, TypeError):
                field_errors['subject'] = True
                raise ValueError("Invalid subject selected")

            if 'notes_file' not in request.FILES:
                field_errors['notes_file'] = True
                raise ValueError("No file uploaded")

            notes_file = request.FILES['notes_file']
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/png',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            if notes_file.content_type not in allowed_types:
                field_errors['notes_file'] = True
                raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")

            if notes_file.size > 10 * 1024 * 1024:
                field_errors['notes_file'] = True
                raise ValueError("File size exceeds 10MB limit")

            note = Notes(
                title=form_data['title'],
                subject_id=subject,
                description=form_data['description'],
                notes_file=notes_file,
                user_id=request.user,
                upload_date=upload_date
            )
            note.save()

            messages.success(request, "Notes uploaded successfully!")
            return redirect('upload_notes_admin')

        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'upload_notes_admin.html', {
                'form_data': form_data,
                'subjects': subjects,
                'field_errors': field_errors
            })

    return render(request, 'upload_notes_admin.html', {
        'form_data': {
            'title': '',
            'subject': '',
            'description': '',
            'upload_date': timezone.now().date().isoformat()
        },
        'subjects': subjects,
        'field_errors': {}
    })

# 









# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# from .models import Subject, Notes  # adjust import as needed
# from datetime import datetime

# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.select_related('category_id').all()
#     field_errors = {}

#     if request.method == 'POST':
#         form_data = {
#             'title': request.POST.get('title', '').strip(),
#             'subject': request.POST.get('subject', '').strip(),
#             'description': request.POST.get('description', '').strip(),
#             'upload_date': request.POST.get('upload_date', '').strip(),
#         }

#         try:
#             # Validate required fields
#             if not form_data['title']:
#                 field_errors['title'] = True
#                 raise ValueError("Title is required")
#             if not form_data['subject']:
#                 field_errors['subject'] = True
#                 raise ValueError("Subject is required")
#             if not form_data['description']:
#                 field_errors['description'] = True
#                 raise ValueError("Description is required")

#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
#                 if upload_date > timezone.now().date():
#                     field_errors['upload_date'] = True
#                     raise ValueError("Date cannot be in the future")
#             except (ValueError, TypeError):
#                 field_errors['upload_date'] = True
#                 raise ValueError("Invalid date format")

#             # Validate and get Subject
#             try:
#                 subject_id = int(form_data['subject'])
#                 subject = Subject.objects.get(pk=subject_id)
#             except (Subject.DoesNotExist, ValueError, TypeError):
#                 field_errors['subject'] = True
#                 raise ValueError("Invalid subject selected")

            

#             # Validate file
#             if 'notes_file' not in request.FILES:
#                 field_errors['notes_file'] = True
#                 raise ValueError("No file uploaded")

#             notes_file = request.FILES['notes_file']
#             allowed_types = [
#                 'application/pdf',
#                 'image/jpeg',
#                 'image/png',
#                 'application/msword',
#                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#             ]
#             if notes_file.content_type not in allowed_types:
#                 field_errors['notes_file'] = True
#                 raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")

#             if notes_file.size > 10 * 1024 * 1024:
#                 field_errors['notes_file'] = True
#                 raise ValueError("File size exceeds 10MB limit")

#             # Save the note
#             note = Notes(
#                 title=form_data['title'],
#                 subject_id=subject,
#                 description=form_data['description'],
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 upload_date=upload_date
#             )
#             note.save()

#             messages.success(request, "Notes uploaded successfully!")
#             return redirect('view_notes')

#         except Exception as e:
#             messages.error(request, str(e))
#             return render(request, 'upload_notes.html', {
#                 'form_data': form_data,
#                 'subjects': subjects,
#                 'field_errors': field_errors
#             })

#     else:
#         # GET request
#         return render(request, 'upload_notes.html', {
#             'form_data': {
#                 'title': '',
#                 'subject': '',
#                 'description': '',
#                 'upload_date': timezone.now().date().isoformat()
#             },
#             'subjects': subjects,
#             'field_errors': {}  # Ensure field_errors is always available
#         })















# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.select_related('category_id').all()
    
#     if request.method == 'POST':
#         form_data = {
#             'title': request.POST.get('title', '').strip(),
#             'subject': request.POST.get('subject', '').strip(),
#             'description': request.POST.get('description', '').strip(),
#             'upload_date': request.POST.get('upload_date', '').strip(),
#         }
        
#         try:
#             # Validate required fields
#             if not form_data['title']:
#                 raise ValueError("Title is required")
#             if not form_data['subject']:
#                 raise ValueError("Subject is required")
#             if not form_data['description']:
#                 raise ValueError("Description is required")
            
#             # Get the specific subject instance
#             try:
#                 subject = Subject.objects.get(pk=form_data['subject'])
#             except (Subject.DoesNotExist, ValueError):
#                 raise ValueError("Invalid subject selected")
            
#             # Handle file upload
#             if 'notes_file' not in request.FILES:
#                 raise ValueError("No file was uploaded")
            
#             notes_file = request.FILES['notes_file']
            
#             # Validate file type
#             allowed_types = [
#                 'application/pdf',
#                 'image/jpeg',
#                 'image/png',
#                 'application/msword',
#                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#             ]
            
#             if notes_file.content_type not in allowed_types:
#                 raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")
            
#             # Validate file size (10MB limit)
#             if notes_file.size > 10 * 1024 * 1024:  # 10MB
#                 raise ValueError("File size exceeds 10MB limit")
            
#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
#                 if upload_date > timezone.now().date():
#                     raise ValueError("Date cannot be in the future")
#             except (ValueError, TypeError):
#                 raise ValueError("Invalid date format")
            
#             # Create and save note
#             note = Notes(
#                 title=form_data['title'],
#                 subject_id=subject,
#                 description=form_data['description'],
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 upload_date=upload_date
#             )
#             note.save()
            
#             messages.success(request, "Notes uploaded successfully!")
#             return redirect('view_notes')
            
#         except Exception as e:
#             messages.error(request, str(e))
#             return render(request, 'upload_notes.html', {
#                 'form_data': form_data,
#                 'subjects': subjects,
#                 'field_errors': {
#                     'title': not form_data.get('title'),
#                     'subject': not form_data.get('subject'),
#                     'description': not form_data.get('description'),
#                     'upload_date': not form_data.get('upload_date'),
#                 }
#             })
    
#     # GET request - show empty form
#     today = timezone.now().date()
#     return render(request, 'upload_notes.html', {
#         'form_data': {
#             'title': '',
#             'subject': '',
#             'description': '',
#             'upload_date': today.isoformat(),
#         },
#         'subjects': subjects
#     })



# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.select_related('category_id').all()
    
#     if request.method == 'POST':
#         form_data = {
#             'title': request.POST.get('title'),
#             'subject': request.POST.get('subject'),  # This should be subject ID
#             'description': request.POST.get('description'),
#             'upload_date': request.POST.get('upload_date'),
#         }
        
#         try:
#             # Validate required fields
#             if not all([form_data['title'], form_data['subject'], form_data['description']]):
#                 raise ValueError("All required fields must be filled")
            
#             # Get the specific subject instance
#             try:
#                 subject = Subject.objects.get(pk=form_data['subject'])
#             except Subject.DoesNotExist:
#                 raise ValueError("Selected subject does not exist")
            
#             # Handle file upload
#             if 'notes_file' not in request.FILES:
#                 raise ValueError("No file was uploaded")
            
#             notes_file = request.FILES['notes_file']
            
#             # Validate file type
#             allowed_types = [
#                 'application/pdf',
#                 'image/jpeg',
#                 'image/png',
#                 'application/msword',
#                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#             ]
            
#             if notes_file.content_type not in allowed_types:
#                 raise ValueError("Only PDF, JPG, PNG, DOC, and DOCX files are allowed")
            
#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(form_data['upload_date'], '%Y-%m-%d').date()
#                 if upload_date > timezone.now().date():
#                     raise ValueError("Date cannot be in the future")
#             except (ValueError, TypeError):
#                 raise ValueError("Invalid date format")
            
#             # Create and save note with the specific subject instance
#             note = Notes(
#                 title=form_data['title'],
#                 subject_id=subject,  # Pass the subject instance here
#                 description=form_data['description'],
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 upload_date=upload_date
#             )
#             note.save()
            
#             messages.success(request, "Notes uploaded successfully!")
#             return redirect('view_notes')
            
#         except Exception as e:
#             messages.error(request, str(e))
#             return render(request, 'upload_notes.html', {
#                 'form_data': form_data,
#                 'subjects': subjects,
#                 'field_errors': {
#                     'title': not form_data.get('title'),
#                     'subject': not form_data.get('subject'),
#                     'description': not form_data.get('description'),
#                 }
#             })
    
#     # GET request - show empty form
#     return render(request, 'upload_notes.html', {
#         'form_data': {
#             'title': '',
#             'subject': '',
#             'description': '',
#             'upload_date': timezone.now().date().isoformat(),
#         },
#         'subjects': subjects
#     })
# ##







# @login_required
# def upload_notes(request):
#     subjects = Subject.objects.all()
#     if request.method == 'POST':
#         try:
#             title = request.POST['title']
#             category = request.POST.get('category')
#             subject_name = request.POST['subject_name']
#             description = request.POST['description']
#             notes_file = request.FILES['notes_file']
#             upload_date_str = request.POST.get('upload_date')

#             # Validate file type
#             allowed_types = [
#                 'application/pdf',
#                 'image/jpeg',
#                 'image/png',
#                 'application/msword',               # .doc
#                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # .docx
#             ]

#             if notes_file.content_type not in allowed_types:
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Only PDF, JPG, PNG, DOC, and DOCX files are allowed',
#                     'form_data': request.POST,
#                 })

#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#                 if upload_date > datetime.now().date():
#                     return render(request, 'upload_notes.html', {
#                         'error': 'yes',
#                         'error_message': 'Date cannot be in the future',
#                         'form_data': request.POST,
#                     })
#             except (ValueError, TypeError):
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Invalid date format',
#                     'form_data': request.POST,
#                 })

#             # # Get or create default category
#             # default_category, _ = Category.objects.get_or_create(
#             #     category_name='General',
#             #     defaults={'category_code': 'GEN'}
#             # )

#             # # Get or create subject with the category
#             # subject, _ = Subject.objects.get_or_create(
#             #     subject_name=subject_name,
#             #     defaults={'category_id': default_category}
#             # )

#             # Save the note
#             note = Notes(
#                 title=title,
#                 category=category,
#                 description=description,
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 subject_id=subjects,
#                 upload_date=upload_date
#             )
#             note.save()

#             return render(request, 'upload_notes.html', {'success': True,'subjects':subjects})

#         except Exception as e:
#             return render(request, 'upload_notes.html', {
#                 'error': 'yes',
#                 'error_message': str(e),
#                 'form_data': request.POST,
#             })

#     form_data = {
#         'title': '',
#         'category': '',
#         'subject_name': '',
#         'description': '',
#         'upload_date': date.today().isoformat(),
#     }
#     return render(request, 'upload_notes.html', {'form_data': form_data,'subjects':subjects})

# #

#
# add? view
#
# from django.contrib import messages
# from .models import Subject, Category

# def add_subject(request):
#     categories = Category.objects.all()
#     if request.method == 'POST':
#         subject_name = request.POST.get('subject_name')
#         category_id = request.POST.get('category_id')

#         if Subject.objects.filter(subject_name=subject_name).exists():
#             messages.error(request, "Subject already exists.")
#         else:
#             category = Category.objects.get(category_id=category_id)
#             Subject.objects.create(subject_name=subject_name, category_id=category)
#             messages.success(request, "Subject added successfully.")
#             return redirect('upload_notes')

#     return render(request, 'add_subject.html', {'categories': categories})


# def add_category(request):
#     categories = Category.objects.all()
#     if request.method == 'POST':
#         category_name = request.POST.get('category_name')
  
      

#         if Category.objects.filter(category_name=category_name).exists():
#             messages.error(request, "category  already exists.")
#         else:
#             Category.objects.create(category_name=category_name)
           
#             messages.success(request, "category added successfully.")
#             return redirect('upload_notes')

#     return render(request, 'add_category.html', {'categories': categories})





##

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subject, Category

def add_subject(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        category_id = request.POST.get('category_id')

        if not subject_name or not category_id:
            messages.error(request, "Please fill all required fields.")
        elif Subject.objects.filter(subject_name=subject_name).exists():
            messages.error(request, "Subject already exists.")
        else:
            try:
                category = Category.objects.get(category_id=category_id)
                Subject.objects.create(subject_name=subject_name, category_id=category)
                messages.success(request, "Subject added successfully.")
                return redirect('upload_notes')
            except Category.DoesNotExist:
                messages.error(request, "Selected category does not exist.")

    return render(request, 'add_subject.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if not category_name:
            messages.error(request, "Category name is required.")
        elif Category.objects.filter(category_name=category_name).exists():
            messages.error(request, "Category already exists.")
        else:
            Category.objects.create(category_name=category_name)
            messages.success(request, "Category added successfully.")
            return redirect('add_subject')  # Redirect back to add subject page

    return render(request, 'add_category.html')
##

#




# @login_required
# def upload_notes(request):
#     if request.method == 'POST':
#         try:
#             title = request.POST['title']
#             category = request.POST.get('category')
#             subject_name = request.POST['subject_name']
#             description = request.POST['description']
#             notes_file = request.FILES['notes_file']
#             upload_date_str = request.POST.get('upload_date')

#             allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
#             if notes_file.content_type not in allowed_types:
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Only PDF, JPG, and PNG files are allowed'
#                 })
#             try:
#                 upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#                 if upload_date > datetime.now().date():
#                     return render(request, 'upload_notes.html', {
#                         'error': 'yes',
#                         'error_message': 'Date cannot be in the future'
#                     })
#             except (ValueError, TypeError):
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Invalid date format'
#                 })
            

            

#             # Create or get default category
#             default_category, _ = Category.objects.get_or_create(
#                 category_name='General',
#                 defaults={'category_code': 'GEN'}
#             )

#             # Create or get subject with the required category
#             subject, _ = Subject.objects.get_or_create(
#                 subject_name=subject_name,
#                 defaults={'category_id': default_category}
#             )

#             # Create the note
#             note = Notes(
#                 title=title,
#                 category=category,
#                 description=description,
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 subject_id=subject,
#                 upload_date=upload_date  # New field added
#             )
#             note.save()

#             return render(request, 'upload_notes.html', {'success': True})

#         except Exception as e:
#             return render(request, 'upload_notes.html', {
#                 'error': 'yes',
#                 'error_message': str(e)
#             })

#     return render(request, 'upload_notes.html')

# #
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from datetime import datetime
# from .models import Notes  # Import your Notes model
# @login_required
# def upload_notes(request):
#     field_errors = {}
#     form_data = {}
    
#     if request.method == 'POST':
#         # Get form data
#         title = request.POST.get('title')
#         subject_name = request.POST.get('subject_name')
#         description = request.POST.get('description')
#         notes_file = request.FILES.get('notes_file')
#         upload_date_str = request.POST.get('upload_date')
        
#         # Validate required fields
#         if not title:
#             field_errors['title'] = "Title is required"
#         if not subject_name:
#             field_errors['subject_name'] = "Subject is required"
#         if not description:
#             field_errors['description'] = "Description is required"
#         if not notes_file:
#             field_errors['notes_file'] = "File is required"
        
#         # Process and validate date
#         try:
#             upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#             if upload_date > datetime.now().date():
#                 field_errors['upload_date'] = "Date cannot be in the future"
#         except (ValueError, TypeError):
#             field_errors['upload_date'] = "Invalid date format"
        
#         # Save if no errors
#         if not field_errors:
#             try:
#                 # Create and save new note
#                 note = Notes(
#                     title=title,
#                     subject_name=subject_name,
#                     description=description,
#                     notes_file=notes_file,
#                     upload_date=upload_date,
#                     user_id=request.user  # Assuming you're using authentication
#                 )
#                 note.save()
                
#                 messages.success(request, "Notes uploaded successfully!")
#                 return redirect('viewmy_notes')
#             except Exception as e:
#                 return render(request, 'upload_notes.html', {
#                     'error': "yes",
#                     'error_message': str(e),
#                     'form_data': request.POST
#                 })
        
#         # If errors, preserve form data
#         form_data = request.POST
    
#     # For GET request or failed POST
#     context = {
#         'field_errors': field_errors,
#         'form_data': form_data,
#         # Set default to today's date
#         'default_date': datetime.now().strftime('%Y-%m-%d')
#     }
#     return render(request, 'upload_notes.html', context)



from django.contrib.auth.decorators import login_required
from .models import Notes


@login_required
def viewmy_notes(request):
    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    notes = Notes.objects.filter(user_id=request.user).order_by('upload_date')
    return render(request, 'viewmy_notes.html', {'notes': notes,'datetime':date,'greet':msg})

@login_required
def delete_mynotes(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    note = get_object_or_404(Notes, note_id=id)
    note.delete()
    return redirect('viewmy_notes')


# @login_required
# def delete_mynotes(request,id):
#     dele=Notes.objects.get(id=id)
#     dele.delete()
#     return redirect('viewmy_notes')

#view all
@login_required
def viewall_notes(request):
    # Get all notes ordered by upload date
    notes = Notes.objects.all().order_by('upload_date')
    return render(request, 'viewall_notes.html', {'notes': notes})
#user
@login_required
def viewall_notes_user(request):
    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    # Get all notes ordered by upload date
    notes = Notes.objects.all().order_by('upload_date')
    return render(request, 'viewall_notes_user.html', {'notes': notes,'datetime':date,'greet':msg})

    



from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Notes
from django.db.models import Q

def notes_list(request):
    # Get search parameters
 
    title = request.GET.get('title', '').strip()
    category = request.GET.get('category', '')

    # Base queryset
    notes = Notes.objects.all()

    # Apply filters
    if title:
        notes = notes.filter(Q(title__icontains=title))

    if category:
        notes = notes.filter(category=category)

    # Order notes (optional, e.g., by upload date)
    notes = notes.order_by('-upload_date')

    # Pagination
    paginator = Paginator(notes, 9)  # Show 9 notes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'notes': page_obj,
        'title': title,

        'category': category,
    })










#
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notes

# @login_required
# def download_note(request, note_id):
#     print(f"Processing download for note_id: {note_id}")
#     note = get_object_or_404(Notes, id=note_id)
#     print(f"Note found: {note.title}, download_count: {note.download_count}")
#     if not note.notes_file:
#         print("No file associated with this note")
#         return render(request, 'error.html', {
#             'error_message': 'File not found for this note.'
#         })
#     note.download_count += 1
#     print(f"New download_count: {note.download_count}")
#     note.save(update_fields=['download_count'])
#     print(f"Redirecting to: {note.notes_file.url}")
#     return redirect(note.notes_file.url)


#
# views.py (correct implementation)
# views.py
from django.shortcuts import get_object_or_404
from django.http import FileResponse
@login_required
def download_note(request, pk):  # Changed parameter name to be generic
    # Use note_id instead of id in the query
    note = get_object_or_404(Notes, note_id=pk)
    
    # Increment download count
    note.download_count += 1
    note.save()
    
    # Return the file as attachment
    return FileResponse(note.notes_file.open(), as_attachment=True)




# def upload_notes_admin(request):


# @login_required
# def upload_notes_admin(request):
#     if request.method == 'POST':
#         try:
#             title = request.POST['title']
#             category = request.POST.get('category')
#             subject_name = request.POST['subject_name']
#             description = request.POST['description']
#             notes_file = request.FILES['notes_file']
#             upload_date_str = request.POST.get('upload_date')

#             # Validate file type
#             allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
#             if notes_file.content_type not in allowed_types:
#                 return render(request, 'upload_notes_admin.html', {
#                     'error': 'yes',
#                     'error_message': 'Only PDF, JPG, and PNG files are allowed',
#                     'form_data': request.POST,  # Preserve form data
#                 })

#             # Validate upload date
#             try:
#                 upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
#                 if upload_date > datetime.now().date():
#                     return render(request, 'upload_notes.html', {
#                         'error': 'yes',
#                         'error_message': 'Date cannot be in the future',
#                         'form_data': request.POST,  # Preserve form data
#                     })
#             except (ValueError, TypeError):
#                 return render(request, 'upload_notes.html', {
#                     'error': 'yes',
#                     'error_message': 'Invalid date format',
#                     'form_data': request.POST,  # Preserve form data
#                 })

#             # Create or get default category
#             default_category, _ = Category.objects.get_or_create(
#                 category_name='General',
#                 defaults={'category_code': 'GEN'}
#             )

#             # Create or get subject with the required category
#             subject, _ = Subject.objects.get_or_create(
#                 subject_name=subject_name,
#                 defaults={'category_id': default_category}
#             )

#             # Create the note
#             note = Notes(
#                 title=title,
#                 category=category,
#                 description=description,
#                 notes_file=notes_file,
#                 user_id=request.user,
#                 subject_id=subject,
#                 upload_date=upload_date
#             )
#             note.save()

#             return render(request, 'upload_notes_admin.html', {'success': True})

#         except Exception as e:
#             return render(request, 'upload_notes_admin.html', {
#                 'error': 'yes',
#                 'error_message': str(e),
#                 'form_data': request.POST,  # Preserve form data
#             })

#     # For GET requests, set default form data with today's date
#     form_data = {
#         'title': '',
#         'category': '',
#         'subject_name': '',
#         'description': '',
#         'upload_date': date.today().isoformat(),  # Sets to 2025-06-16
#     }
#     return render(request, 'upload_notes_admin.html', {'form_data': form_data})
# #



# viewmy_notes_admin
@login_required
def viewmy_notes_admin(request):
    notes = Notes.objects.filter(user_id=request.user).order_by('upload_date')
    return render(request, 'viewmy_notes_admin.html', {'notes': notes})



#admin
@login_required
def delete_mynotes_admin(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    note = get_object_or_404(Notes, note_id=id)
    note.delete()
    return redirect('viewall_notes')


from django.contrib import messages
@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Basic validation
        if not username or not email:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'edit_profile.html', {'user': request.user})



        user = request.user
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # or wherever your profile view is

    return render(request, 'edit_profile.html', {'user': request.user})


@login_required
def edit_profile1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        user = request.user
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile1')  # or wherever your profile view is

    return render(request, 'edit_profile1.html', {'user': request.user})






#
#view users

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model  # Add this import

# Use get_user_model() to get the correct User model
User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    users = User.objects.all()
    return render(request, "view_users.html", {"users": users})



    #custom mail for reseet password
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    success_url = "/note/password_reset/done/"
    email_template_name = "emails/password_reset_email.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        users = User.objects.filter(email__iexact=email, is_active=True)

        for user in users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = self.token_generator.make_token(user)

            context = {
                "user": user,
                "domain": settings.MY_SITE_DOMAIN,       # e.g. 127.0.0.1:8000
                "protocol": settings.MY_SITE_PROTOCOL,   # e.g. http
                "uid": uid,
                "token": token,
                "site_name": "MyApp",
            }

            html_content = render_to_string(self.email_template_name, context)

            msg = EmailMultiAlternatives(
                subject="Reset Your Password",
                body="Please view this email in an HTML-compatible client.",  # fallback text
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return super().form_valid(form)


#views for upvote as well as comment, also notedetail pageee
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Notes, Upvote, Comment


def note_detail(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    comments = note.comments.all().order_by("-created_at")
    upvotes = note.upvotes.count()

    return render(request, "note_detail.html", {
        "note": note,
        "comments": comments,
        "upvotes": upvotes,
    })


def note_detail_admin(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    comments = note.comments.all().order_by("-created_at")
    upvotes = note.upvotes.count()

    return render(request, "note_detail_admin.html", {
        "note": note,
        "comments": comments,
        "upvotes": upvotes,
    })


def upvote_note(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    user = request.user

    if user.is_authenticated:
        upvote, created = Upvote.objects.get_or_create(note=note, user=user)
        if not created:
            upvote.delete()  # toggle (remove if already liked)
        return redirect("note_detail", note_id=note.note_id)
    return redirect("login")  # redirect if not logged in


def add_comment(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if request.user.is_authenticated:
            Comment.objects.create(note=note, user=request.user, content=content)
        else:
            guest_name = request.POST.get("guest_name", "Guest")
            Comment.objects.create(note=note, guest_name=guest_name, content=content)
    return redirect("note_detail", note_id=note.note_id)

#for admin
def add_comment_admin(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if request.user.is_authenticated:
            Comment.objects.create(note=note, user=request.user, content=content)
        else:
            guest_name = request.POST.get("guest_name", "Guest")
            Comment.objects.create(note=note, guest_name=guest_name, content=content)
    return redirect("note_detail_admin", note_id=note.note_id)



def upvote_note_admin(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    user = request.user

    if user.is_authenticated:
        upvote, created = Upvote.objects.get_or_create(note=note, user=user)
        if not created:
            upvote.delete()  # toggle (remove if already liked)
        return redirect("note_detail_admin", note_id=note.note_id)
    return redirect("login")  # redirect if not logged in


    #page not found

def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)

