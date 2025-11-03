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
from django.contrib.admin.views.decorators import staff_member_required
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
@staff_member_required
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
    from_email = "dc.aloneboe@gmail.com"  # Replace with your email
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

    # 

    # note = get_object_or_404(Notes, pk=note_id)

    # upvotes = notes.upvotes.count()



    # 


    date=datetime.now()
    h=time.strftime("%H")
    if h>='0' and h<'12':
        msg="Good Morning, "
    elif h>='12' and h<'18':
        msg="Good Afternoon, "
    else:
        msg="Good Evening,"
    
    return render(request,'dashboard.html',{'notes':notes,'datetime':date,'greet':msg,})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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
@login_required
@staff_member_required
def profile1(request):
    return render(request,'profile1.html')



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
@staff_member_required
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
from collections import defaultdict
@login_required
def viewall_notes_user(request):
    date = datetime.now()
    h = time.strftime("%H")
    if h >= '0' and h < '12':
        msg = "Good Morning,"
    elif h >= '12' and h < '18':
        msg = "Good Afternoon,"
    else:
        msg = "Good Evening,"

    # Get all notes ordered by upload date
    notes = Notes.objects.select_related("subject_id__category_id").order_by("upload_date")

    # Group notes by category
    categories = defaultdict(list)
    for note in notes:
        category = note.subject_id.category_id if note.subject_id and note.subject_id.category_id else None
        categories[category].append(note)

    # Convert into list of dicts for template
    grouped_categories = []
    for category, notes_in_cat in categories.items():
        grouped_categories.append({
            "category": category,
            "notes": notes_in_cat
        })

    return render(request, "viewall_notes_user.html", {
        "categories": grouped_categories,
        "datetime": date,
        "greet": msg
    })
# def viewall_notes_user(request):
#     date = datetime.now()
#     h = time.strftime("%H")
#     if h >= '0' and h < '12':
#         msg = "Good Morning, "
#     elif h >= '12' and h < '18':
#         msg = "Good Afternoon, "
#     else:
#         msg = "Good Evening,"
    
#     # Get all notes ordered by upload date
#     notes = Notes.objects.all().order_by('upload_date')
#     return render(request, 'viewall_notes_user.html', {'notes': notes, 'datetime': date, 'greet': msg})


# def viewall_notes_user(request):
#     date=datetime.now()
#     h=time.strftime("%H")
#     if h>='0' and h<'12':
#         msg="Good Morning, "
#     elif h>='12' and h<'18':
#         msg="Good Afternoon, "
#     else:
#         msg="Good Evening,"
#     # Get all notes ordered by upload date
#     notes = Notes.objects.all().order_by('upload_date')
#     return render(request, 'viewall_notes_user.html', {'notes': notes,'datetime':date,'greet':msg})

####
# 
# from django.shortcuts import render
# from .models import Notes, Category  # 👈 Import your Category model
# from django.utils import timezone
# import time

# def viewall_notes_user(request):
#     """
#     This view displays all note categories and allows users to view
#     notes for each category in a modal pop-up.
#     """
#     # --- Greeting Logic (your original code is fine) ---
#     now = timezone.now()
#     h = now.strftime("%H")
#     if '00' <= h < '12':
#         msg = "Good Morning, "
#     elif '12' <= h < '18':
#         msg = "Good Afternoon, "
#     else:
#         msg = "Good Evening,"

#     # --- Data Fetching Logic ---
#     # 1. Get all notes and pre-fetch related subject and category data to avoid extra DB queries.
#     all_notes = Notes.objects.select_related('subject_id__category_id').all().order_by('-upload_date')

#     # 2. Get a list of category IDs that actually have notes.
#     #    This prevents displaying empty category cards.
#     category_ids_with_notes = all_notes.values_list('subject_id__category_id', flat=True).distinct()

#     # 3. Fetch the actual category objects.
#     categories = Category.objects.filter(id__in=category_ids_with_notes).order_by('category_name')

#     # --- Context to be passed to the template ---
#     context = {
#         'notes': all_notes,
#         'categories': categories,
#         'datetime': now,
#         'greet': msg,
#     }
    
#     return render(request, 'viewall_notes_user.html', context)
# ###

# in nssapp/views.py

# def viewall_notes_user(request):
#     # ... (the rest of your view code) ...
    
#     category_ids_with_notes = all_notes.values_list('subject_id__category_id', flat=True).distinct()
    
#     #  FIX: Changed filter from 'id__in' to 'category_id__in'
#     categories = Category.objects.filter(category_id__in=category_ids_with_notes).order_by('category_name')

#     context = {
#         'notes': all_notes,
#         'categories': categories,
#         'datetime': now,
#         'greet': msg,
#         # ... (the rest of your context) ...
#     }
    
#     return render(request, 'viewall_notes_user.html', context)
    



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
@staff_member_required
def viewmy_notes_admin(request):
    notes = Notes.objects.filter(user_id=request.user).order_by('upload_date')
    return render(request, 'viewmy_notes_admin.html', {'notes': notes})



#admin
@login_required
@staff_member_required
def delete_mynotes_admin(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    note = get_object_or_404(Notes, note_id=id)
    note.delete()
    return redirect('viewall_notes')


from django.contrib import messages
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')

#         # Basic validation
#         if not username or not email:
#             messages.error(request, 'Please fill in all fields.')
#             return render(request, 'edit_profile.html', {'user': request.user})



#         user = request.user
#         user.username = username
#         user.email = email
#         user.save()

#         messages.success(request, 'Profile updated successfully.')
#         return redirect('profile')  # or wherever your profile view is

#     return render(request, 'edit_profile.html', {'user': request.user})
# =============================================

# //////////////////////////////////////////////////////////////////////////
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')  # Handle file upload

        # Basic validation
        if not username or not email:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'edit_profile.html', {'user': request.user})

        user = request.user
        user.username = username
        user.email = email
        if profile_picture:
            # Validate file type and size
            allowed_types = ['image/jpeg', 'image/png']
            if profile_picture.content_type not in allowed_types:
                messages.error(request, 'Only JPG and PNG images are allowed.')
                return render(request, 'edit_profile.html', {'user': request.user})
            if profile_picture.size > 10* 1024 * 1024:  # 5MB limit
                messages.error(request, 'Image file size must be under 10MB.')
                return render(request, 'edit_profile.html', {'user': request.user})
            user.profile_picture = profile_picture
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': request.user})


# ////////////////////////////////////////////

@login_required
@staff_member_required
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
#view user
@login_required
@staff_member_required
@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    users = User.objects.all()
    return render(request, "view_users.html", {"users": users})

## delete user
@staff_member_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    """
    Delete a user by ID, restricted to superusers.
    Prevents deletion of the requesting user.
    """
    try:
        user_to_delete = User.objects.get(id=user_id)
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete your own account.")
        elif user_to_delete.is_superuser:
            messages.error(request, "Cannot delete superuser accounts.")
        else:
            username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request, f"User {username} deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        messages.error(request, "An error occurred while deleting the user.")
    return redirect('view_users')
##
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

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    comments = note.comments.all().order_by("-created_at")
    upvotes = note.upvotes.count()

    return render(request, "note_detail.html", {
        "note": note,
        "comments": comments,
        "upvotes": upvotes,
    })

@staff_member_required
def note_detail_admin(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    comments = note.comments.all().order_by("-created_at")
    upvotes = note.upvotes.count()

    return render(request, "note_detail_admin.html", {
        "note": note,
        "comments": comments,
        "upvotes": upvotes,
    })

@login_required
def upvote_note(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    user = request.user

    if user.is_authenticated:
        upvote, created = Upvote.objects.get_or_create(note=note, user=user)
        if not created:
            upvote.delete()  # toggle (remove if already liked)
        return redirect("note_detail", note_id=note.note_id)
    return redirect("login")  # redirect if not logged in

@login_required
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
@login_required
@staff_member_required
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


@login_required
@staff_member_required
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


####################################

# views.py - Add this temporary debug view
def debug_callback(request):
    """Debug view to see callback data"""
    return HttpResponse(f"""
    <h1>Callback Debug</h1>
    <p>GET parameters: {dict(request.GET)}</p>
    <p>Current user: {request.user}</p>
    <p>Authenticated: {request.user.is_authenticated}</p>
    <p><a href="/note/auth/google/">Try Google Login Again</a></p>
    <p><a href="/note/login/">Back to Login</a></p>
    """)




 # views.py - Update your Google auth views
import requests  
def google_auth(request):
    """Google OAuth2 initiation - works for both dev and production"""
    if settings.DEBUG:
        redirect_uri = 'http://127.0.0.1:8000/note/auth/google/callback/'
    else:
        redirect_uri = 'https://iwasbinod.pythonanywhere.com/note/auth/google/callback/'
    
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=email%20profile&"
        f"access_type=online"
    )
    return redirect(google_auth_url)

def google_auth_callback(request):
    """Handle Google callback for both environments"""
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        messages.error(request, f"Google login failed: {error}")
        return redirect('login')
    
    if not code:
        messages.error(request, "No authorization code received from Google")
        return redirect('login')
    
    try:
        # Determine redirect URI based on environment
        if settings.DEBUG:
            redirect_uri = 'http://127.0.0.1:8000/note/auth/google/callback/'
        else:
            redirect_uri = 'https://iwasbinod.pythonanywhere.com/note/auth/google/callback/'
        
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        
        response = requests.post(token_url, data=data)
        token_data = response.json()
        
        if 'error' in token_data:
            error_msg = token_data.get('error_description', token_data['error'])
            messages.error(request, f"Token exchange failed: {error_msg}")
            return redirect('login')
        
        # Get user info using access token
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
        
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()
        
        # Extract user data
        email = user_info['email']
        google_id = user_info['id']
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        
        # Get or create user
        user = get_or_create_google_user(email, google_id, first_name, last_name)
        
        # Log the user in
        login(request, user)
        messages.success(request, f"Welcome, {first_name or user.username}!")
        
        # Redirect based on user type
        if user.is_superuser:
            return redirect('adminpage')
        else:
            return redirect('dashboard')
            
    except Exception as e:
        messages.error(request, f"Login failed: {str(e)}")
        return redirect('login')
    

# views.py - Add this function
def get_or_create_google_user(email, google_id, first_name, last_name):
    """Get or create user from Google data"""
    try:
        # Try to find user by Google ID first
        user = User.objects.get(google_id=google_id)
        print(f"Found existing user by Google ID: {user.username}")
        return user
    except User.DoesNotExist:
        try:
            # Try to find by email and link Google account
            user = User.objects.get(email=email)
            print(f"Found existing user by email, linking Google ID: {user.username}")
            user.google_id = google_id
            user.save()
            return user
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
            # Make username unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            print(f"Creating new user: {username}")
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_id=google_id,
                is_active=True
            )
            user.set_unusable_password()  # Google users don't need password
            user.save()
            return user



#####################################



#####################################################################################
######################################################################################
########################################################################################
# exclusive

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden, FileResponse
from django.db.models import Q
from .models import ExclusiveNote, NotePurchase, User
from decimal import Decimal

def is_admin(user):
    return user.is_authenticated and user.role and user.role.is_admin_role

# User Views
@login_required
def exclusive_notes_list(request):
    notes = ExclusiveNote.objects.filter(is_active=True)
    
    # Check which notes the user has purchased
    purchased_notes = NotePurchase.objects.filter(user=request.user).values_list('note_id', flat=True)
    
    # Create a list of purchased note IDs for the template
    purchased_note_ids = list(purchased_notes)
    
    context = {
        'notes': notes,
        'purchased_note_ids': purchased_note_ids
    }
    
    return render(request, 'exclusive_notes_list.html', context)

@login_required
def purchase_note(request, note_id):
    note = get_object_or_404(ExclusiveNote, note_id=note_id, is_active=True)
    
    # Check if user already purchased this note
    if NotePurchase.objects.filter(user=request.user, note=note).exists():
        messages.warning(request, 'You have already purchased this note!')
        return redirect('exclusive_notes_list')
    
    # In a real application, you would integrate with a payment gateway here
    # For now, we'll simulate the purchase
    
    purchase = NotePurchase.objects.create(
        user=request.user,
        note=note,
        amount_paid=note.price
    )
    
    messages.success(request, f'Successfully purchased "{note.title}" for ${note.price}!')
    return redirect('exclusive_notes_list')

@login_required
def download_exclusive_note(request, note_id):
    note = get_object_or_404(ExclusiveNote, note_id=note_id)
    
    # Check if user purchased this note or is admin
    if not NotePurchase.objects.filter(user=request.user, note=note).exists() and not is_admin(request.user):
        messages.error(request, 'You need to purchase this note before downloading!')
        return redirect('exclusive_notes_list')
    
    # Serve the file for download
    response = FileResponse(note.notes_file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{note.notes_file.name}"'
    return response

# Admin Views
@login_required
@staff_member_required
# @user_passes_test(is_admin)
def admin_exclusive_notes(request):
    notes = ExclusiveNote.objects.all().order_by('-upload_date')
    return render(request, 'admin_exclusive_notes.html', {'notes': notes})

@login_required
@staff_member_required
def upload_exclusive_note(request):
    from .forms import ExclusiveNoteForm  # We'll create this form next
    
    if request.method == 'POST':
        form = ExclusiveNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.user
            note.save()
            messages.success(request, 'Exclusive note uploaded successfully!')
            return redirect('admin_exclusive_notes')
    else:
        form = ExclusiveNoteForm()
    
    return render(request, 'upload_exclusive_note.html', {'form': form})




@login_required
@staff_member_required
def view_purchase_details(request):
    purchases = NotePurchase.objects.all().order_by('-purchase_date')
    
    # Calculate total revenue from completed purchases only
    total_revenue = sum(
        purchase.amount_paid for purchase in purchases 
        if purchase.payment_status == 'COMPLETED'
    )
    
    return render(request, 'purchase_details.html', {
        'purchases': purchases,
        'total_revenue': total_revenue
    })



##esewa 


# Add these imports at the top
import uuid
import hmac
import hashlib
import base64
import json
import requests
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# eSewa Configuration
ESEWA_MERCHANT_ID = "EPAYTEST"
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"
ESEWA_BASE_URL = "https://rc-epay.esewa.com.np"  # For testing


@login_required
def purchase_note(request, note_id):
    note = get_object_or_404(ExclusiveNote, note_id=note_id, is_active=True)
    
    # Check if user already has any purchase record for this note (including failed ones)
    existing_purchase = NotePurchase.objects.filter(
        user=request.user, 
        note=note
    ).first()
    
    if existing_purchase:
        if existing_purchase.payment_status == 'COMPLETED':
            messages.warning(request, 'You have already purchased this note!')
            return redirect('exclusive_notes_list')
        else:
            # If there's a pending or failed purchase, update it instead of creating new
            existing_purchase.amount_paid = note.price
            existing_purchase.payment_status = 'PENDING'
            existing_purchase.save()
            
            # Redirect to eSewa payment with existing purchase
            return redirect('esewa_payment', purchase_id=existing_purchase.purchase_id)
    
    # Create a new pending purchase record only if no existing record
    purchase = NotePurchase.objects.create(
        user=request.user,
        note=note,
        amount_paid=note.price,
        payment_status='PENDING'
    )
    
    # Redirect to eSewa payment
    return redirect('esewa_payment', purchase_id=purchase.purchase_id)



# eSewa Payment View
class EsewaView(View):
    def get(self, request, purchase_id, *args, **kwargs):
        purchase = get_object_or_404(NotePurchase, purchase_id=purchase_id, user=request.user)
        
        if purchase.payment_status == 'COMPLETED':
            messages.success(request, 'Payment already completed!')
            return redirect('exclusive_notes_list')
        
        # Generate unique transaction UUID
        transaction_uuid = str(uuid.uuid4())
        purchase.esewa_transaction_uuid = transaction_uuid
        purchase.save()
        
        # Prepare data for signature
        amount = str(float(purchase.amount_paid))
        tax_amount = "0"
        product_service_charge = "0"
        product_delivery_charge = "0"
        total_amount = str(float(amount) + float(tax_amount) + float(product_service_charge) + float(product_delivery_charge))
        
        # Create signature
        data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={ESEWA_MERCHANT_ID}"
        signature = hmac.new(
            ESEWA_SECRET_KEY.encode('utf-8'),
            data_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        data = {
            "amount": amount,
            "tax_amount": tax_amount,
            "product_service_charge": product_service_charge,
            "product_delivery_charge": product_delivery_charge,
            "total_amount": total_amount,
            "transaction_uuid": transaction_uuid,
            "product_code": ESEWA_MERCHANT_ID,
            "success_url": request.build_absolute_uri(f'/note/esewa-verify/{purchase.purchase_id}/'),
            "failure_url": request.build_absolute_uri(f'/note/esewa-verify/{purchase.purchase_id}/'),
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature_base64,
            "purchase_id": purchase.purchase_id,
            "note_title": purchase.note.title,
        }
        
        return render(request, "esewa_payment.html", {"data": data})

# eSewa Verification View
@login_required
def esewa_verify(request, purchase_id):
    if request.method == 'GET':
        try:
            data = request.GET.get('data')
            purchase = get_object_or_404(NotePurchase, purchase_id=purchase_id, user=request.user)
            
            if not data:
                messages.error(request, 'Payment verification failed: No data received')
                return redirect('exclusive_notes_list')
            
            # Decode the response data
            decoded_data = base64.b64decode(data).decode('utf-8')
            map_data = json.loads(decoded_data)
            
            if map_data.get('status') == 'COMPLETE':
                # Verify the transaction with eSewa
                verification_data = {
                    'product_code': ESEWA_MERCHANT_ID,
                    'total_amount': str(float(purchase.amount_paid)),
                    'transaction_uuid': purchase.esewa_transaction_uuid
                }
                
                # In production, you should verify with eSewa's verification API
                # For testing, we'll assume it's successful
                
                purchase.payment_status = 'COMPLETED'
                purchase.esewa_transaction_code = map_data.get('transaction_code', '')
                purchase.save()
                
                messages.success(request, f'Successfully purchased "{purchase.note.title}"! You can now download the note.')
                return redirect('exclusive_notes_list')
            else:
                purchase.payment_status = 'FAILED'
                purchase.save()
                messages.error(request, 'Payment failed! Please try again.')
                return redirect('exclusive_notes_list')
                
        except Exception as e:
            messages.error(request, f'Payment verification error: {str(e)}')
            return redirect('exclusive_notes_list')

# Update the download view to check payment status
@login_required
def download_exclusive_note(request, note_id):
    note = get_object_or_404(ExclusiveNote, note_id=note_id)
    
    # Check if user purchased this note or is admin
    has_purchased = NotePurchase.objects.filter(
        user=request.user, 
        note=note, 
        payment_status='COMPLETED'
    ).exists()
    
    if not has_purchased and not is_admin(request.user):
        messages.error(request, 'You need to purchase this note before downloading!')
        return redirect('exclusive_notes_list')
    
    # Serve the file for download
    response = FileResponse(note.notes_file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{note.notes_file.name}"'
    return response

# Update the exclusive_notes_list view
@login_required
def exclusive_notes_list(request):
    notes = ExclusiveNote.objects.filter(is_active=True)
    
    # Check which notes the user has purchased (only completed payments)
    purchased_notes = NotePurchase.objects.filter(
        user=request.user, 
        payment_status='COMPLETED'
    ).values_list('note_id', flat=True)
    
    # Create a list of purchased note IDs for the template
    purchased_note_ids = list(purchased_notes)
    
    context = {
        'notes': notes,
        'purchased_note_ids': purchased_note_ids
    }
    
    return render(request, 'exclusive_notes_list.html', context)
