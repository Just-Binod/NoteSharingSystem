from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from datetime import date
from datetime import datetime
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
    return render(request,'nav.html')
def home(request):
    return render(request,'home.html')





@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@guest
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('adminpage')
            else:
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def adminpage(request):
    return render(request,'adminpage.html')





@auth
def dashboard_view(request):
    return render(request,'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')

#

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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notes, Subject

from .models import Notes, Subject, Category  # make sure these are imported
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def upload_notes(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            subject_name = request.POST['subject_name']
            description = request.POST['description']
            notes_file = request.FILES['notes_file']
            upload_date_str = request.POST.get('upload_date')

            allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
            if notes_file.content_type not in allowed_types:
                return render(request, 'upload_notes.html', {
                    'error': 'yes',
                    'error_message': 'Only PDF, JPG, and PNG files are allowed'
                })
            try:
                upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
                if upload_date > datetime.now().date():
                    return render(request, 'upload_notes.html', {
                        'error': 'yes',
                        'error_message': 'Date cannot be in the future'
                    })
            except (ValueError, TypeError):
                return render(request, 'upload_notes.html', {
                    'error': 'yes',
                    'error_message': 'Invalid date format'
                })
            

            

            # Create or get default category
            default_category, _ = Category.objects.get_or_create(
                category_name='General',
                defaults={'category_code': 'GEN'}
            )

            # Create or get subject with the required category
            subject, _ = Subject.objects.get_or_create(
                subject_name=subject_name,
                defaults={'category_id': default_category}
            )

            # Create the note
            Notes.objects.create(
                title=title,
                description=description,
                notes_file=notes_file,
                user_id=request.user,
                subject_id=subject,
                upload_date=upload_date  # New field added
            )

            return render(request, 'upload_notes.html', {'success': True})

        except Exception as e:
            return render(request, 'upload_notes.html', {
                'error': 'yes',
                'error_message': str(e)
            })

    return render(request, 'upload_notes.html')

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
    notes = Notes.objects.filter(user_id=request.user).order_by('upload_date')
    return render(request, 'viewmy_notes.html', {'notes': notes})

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