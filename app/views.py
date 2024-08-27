from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils import timezone
from .forms import PatientForm, PsychologistForm, LoginForm
from app.models import Entry, Patient, Psychologist


# Vista para la página de inicio
# Esta página sirve como punto de entrada al sitio web y
# contiene el nombre de la página, además de enlaces a register o login
# del paciente o el psicólogo.
def landing(request):
    # If user is authenticated and tries to sneak into the landing page...
    # ...it will redirect the user to its corresponding diary immediately.
    # The only case in which you can view the landing page while being logged in is when
    # you are authenticated as a user that is not a patient or psychologist,
    # which will never happen unless you manually create users from the admin.
    if request.user.is_authenticated:
        if hasattr(request.user, 'patient'):
            return redirect('user-diary')
        elif hasattr(request.user, 'psychologist'):
            return redirect('psych-diary')
    return render(request, "landing.html")


# Vista para la página de inicio de sesión
# Permite a los usuarios registrados (pacientes y psicólogos) iniciar sesión en sus cuentas.
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return HttpResponse("Usuario o contraseña incorrectos")
            if user and password == user.password:
                is_patient = Patient.objects.filter(user=user).exists()
                is_psychologist = Psychologist.objects.filter(user=user).exists()
                if is_patient:
                    login(request, user)
                    return redirect('user-diary')
                elif is_psychologist:
                    login(request, user)
                    return redirect('psych-diary')
                else:
                    return HttpResponse("Usuario no es paciente ni psicólogo")
            else:
                return HttpResponse("Usuario o contraseña incorrectos")

    return render(request, "login.html", {'form': LoginForm(request.POST)})


@login_required
def log_out(request):
    logout(request)
    return redirect("landing")


# Vista para la página de registro de pacientes
# Permite a los nuevos pacientes crear una cuenta en el sistema.
def patient_register(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                birthdate = form.cleaned_data['birthdate']
                photo = form.cleaned_data['photo']

                user = User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()

                patient = Patient.objects.create(
                    user=user,
                    name=name,
                    birthdate=birthdate,
                    photo=photo
                )
                patient.save()

                login(request, user)

                return redirect('user-diary')

            except Exception as e:
                return HttpResponse(f"ERROR EN EL REGISTRO PACIENTE ({e})")

    return render(request, "patient-register.html", {
        'form': PatientForm(request.POST)
    })


# Vista para la página de registro de psicólogos
# Permite a los nuevos psicólogos crear una cuenta en el sistema.
def psych_register(request):
    if request.method == 'POST':
        form = PsychologistForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                birthdate = form.cleaned_data['birthdate']
                specialty = form.cleaned_data['specialty']
                photo = form.cleaned_data['photo']
                title = form.cleaned_data['title']

                user = User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()

                psych = Psychologist.objects.create(
                    user=user,
                    name=name,
                    specialty=specialty,
                    birthdate=birthdate,
                    photo=photo,
                    title=title
                )
                psych.save()

                login(request, user)

                return redirect('psych-diary')

            except Exception as e:
                return HttpResponse(f"ERROR EN EL REGISTRO PSICÓLOGO ({e})")

    return render(request, "psych-register.html", {
        'form': PsychologistForm(request.POST)
    })


# Vista para la página del diario del usuario
# Permite a los pacientes registrados registrar entradas en su diario personal,
# además de ver las entradas anteriores, también pueden ver la lista de sus psicólogos
# y algunas configuraciones de la página.
@login_required
def user_diary(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                patient = request.user.patient
            except Patient.DoesNotExist:
                return redirect('psych-diary')
        else:
            return redirect('login')

        # Get the list of diary entries for the patient
        diaries_list = Entry.objects.filter(patient=patient).order_by('-date')

        # Get the list of psychologists associated with the patient
        psych_list = patient.psychologists.all()

        all_psych_list = Psychologist.objects.all()

        return render(request, "user-diary.html", {
            'patient': patient,
            'diaries_list': diaries_list,
            'psych_list': psych_list,
            'all_psych_list': all_psych_list
        })


# Vista para la página del psicólogo.
# Permite a los psicólogos ver la lista de entradas del diario de cada paciente que lo ha seleccionado.
# Además, los psicológos podrán realizar una búsqueda sobre cada diario y pedir auxilio en caso de que un paciente
# requiera de alguna atención urgente.
@login_required
def psych_diary(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                psych = request.user.psychologist
            except Psychologist.DoesNotExist:
                return redirect('user-diary')
        else:
            return redirect('login')

        patient_list = psych.patients.all()

        diaries_list = Entry.objects.none()

        if patient_list.exists():
            patient = patient_list.first()
            diaries_list = []

        return render(request, "psych-diary.html", {
            'psych': psych,
            'diaries_list': diaries_list,
            'patient_list': patient_list
        })

# Vista que le permite a un paciente vincular a un psicólogo a su lista de psicólogos
# de los psicólogos registrados en la página.
# Permitiendo que el psicólogo pueda ver el diario del paciente.
# Actualiza la lista de psicólogos y devuelve la nueva lista actualizada.
@login_required
def link_psychologist(request, psych_id):
    patient = get_object_or_404(Patient, user=request.user)
    psychologist = get_object_or_404(Psychologist, id=psych_id)
    patient.psychologists.add(psychologist)

    updated_psych_list_html = render_to_string('partials/psych_list.html', {'psych_list': patient.psychologists.all()})
    updated_all_psych_list_html = render_to_string('partials/all_psych_list.html', {
        'all_psych_list': Psychologist.objects.all(),
        'psych_list': patient.psychologists.all(),
    })

    return JsonResponse({'status': 'linked', 'updated_psych_list_html': updated_psych_list_html,
                         'updated_all_psych_list_html': updated_all_psych_list_html})

# Vista que le permite a un paciente desvincular a un psicólogo de su lista de psicólogos
# denegándole el acceso a sus diarios.
# Actualiza la lista de psicólogos y devuelve la nueva lista actualizada.
@login_required
def unlink_psychologist(request, psych_id):
    patient = get_object_or_404(Patient, user=request.user)
    psychologist = get_object_or_404(Psychologist, id=psych_id)
    patient.psychologists.remove(psychologist)

    updated_psych_list_html = render_to_string('partials/psych_list.html', {'psych_list': patient.psychologists.all()})
    updated_all_psych_list_html = render_to_string('partials/all_psych_list.html', {
        'all_psych_list': Psychologist.objects.all(),
        'psych_list': patient.psychologists.all(),
    })

    return JsonResponse({'status': 'unlinked', 'updated_psych_list_html': updated_psych_list_html,
                         'updated_all_psych_list_html': updated_all_psych_list_html})

# Vista que permite a un paciente eliminar todos los psicólogos de su lista de psicólogos,
# dejando su diario oculto para todos los psicólogos.
# Actualiza la lista de psicólogos y devuelve la nueva lista actualizada
@login_required
def remove_all_psychologists(request):
    patient = get_object_or_404(Patient, user=request.user)
    patient.psychologists.clear()

    updated_psych_list_html = render_to_string('partials/psych_list.html', {'psych_list': patient.psychologists.all()})
    updated_all_psych_list_html = render_to_string('partials/all_psych_list.html', {
        'all_psych_list': Psychologist.objects.all(),
        'psych_list': patient.psychologists.all(),
    })

    return JsonResponse({'status': 'all_removed', 'updated_psych_list_html': updated_psych_list_html,
                         'updated_all_psych_list_html': updated_all_psych_list_html})

# Esta vista permite a un paciente crear una nueva entrada en su diario
# con un título, texto y emoji de emoción.
# Realiza validaciones de entrada y actualiza la lista de entradas del diario.
@login_required
def create_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        emotion = request.POST.get('emotion')

        # Validate emoji
        if not emotion or len(emotion) < 1 or len(emotion) > 3:
            return JsonResponse({'status': 'error', 'message': 'Invalid emoji. Must be a single character.'},
                                status=400)

        # Validate title
        if not title or len(title) > 25:
            return JsonResponse(
                {'status': 'error', 'message': 'Title must not be empty and should be at most 25 characters long.'},
                status=400)

        # Validate text
        if not text or len(text) < 1 or len(text) > 500:
            return JsonResponse({'status': 'error',
                                 'message': 'Text must not be empty and should be between 1 and 500 characters long.'},
                                status=400)

        patient = request.user.patient
        print(timezone.now())
        entry = Entry.objects.create(
            patient=patient,
            date=timezone.now(),
            emotion=emotion,
            title=title,
            text=text
        )

        # Render the updated entry list
        updated_entry_list_html = render_to_string('partials/entry_list.html', {
            'diaries_list': Entry.objects.filter(patient=patient).order_by('-date')})

        return JsonResponse(
            {'status': 'success', 'entry_id': entry.id, 'updated_entry_list_html': updated_entry_list_html})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

# Vista que le permite a un paciente ordenar su diario por fecha, 
# ya sea en orden ascendente o descendente. 
# Actualiza la lista de entradas del diario.
@login_required
def sort_entries(request, order):
    patient = request.user.patient
    if order == 'recent':
        diaries_list = Entry.objects.filter(patient=patient).order_by('-date')
    else:
        diaries_list = Entry.objects.filter(patient=patient).order_by('date')

    updated_entry_list_html = render_to_string('partials/entry_list.html', {'diaries_list': diaries_list})
    return JsonResponse({'status': 'success', 'updated_entry_list_html': updated_entry_list_html})

# Vista que permite al paciente buscar sus entradas del diario por título o texto,
# mostrándolos del más nuevo al más antiguo.
# Actualiza la lista de entradas del diario con lo diarios que coincidan con el texto.
@login_required
def search_entries(request):
    query = request.GET.get('query', '')
    if query:
        entries = Entry.objects.filter(patient=request.user.patient)
        entries = entries.filter(Q(title__icontains=query) | Q(text__icontains=query)).order_by('-date')
    else:
        entries = Entry.objects.filter(patient=request.user.patient).order_by('-date')

    context = {
        'diaries_list': entries
    }

    html = render_to_string('partials/entry_list.html', context)

    return JsonResponse({
        'status': 'success',
        'updated_entry_list_html': html
    })

# Esta vista le permite a un paciente eliminar todas las entradas de su diario.
# Actualiza la lista de entradas del diario.
@login_required
def delete_all_diaries(request):
    if request.method == 'POST':
        try:
            patient = request.user.patient  # Assuming the user is a Patient
            Entry.objects.filter(patient=patient).delete()
            updated_entry_list_html = render_to_string('partials/entry_list.html', {
                'diaries_list': Entry.objects.filter(patient=patient).order_by('-date')})
            return JsonResponse({'status': 'success', 'updated_entry_list_html': updated_entry_list_html})
        except Patient.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Patient not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Esta vista permite a un paciente obtener todas las entradas de sus diarios.
# Actualiza la lista de entradas del diario.
@login_required
def get_patient_diaries(request):
    patient_id = request.GET.get('patient_id')
    try:
        patient = Patient.objects.get(id=patient_id)
        diaries = Entry.objects.filter(patient=patient).order_by('-date')
        context = {'diaries_list': diaries}
        html = render_to_string('partials/entry_list.html', context)
        return JsonResponse({'status': 'success', 'updated_entry_list_html': html})
    except Patient.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Patient not found'})

# Vista permite a un psicólogo ordenar las entradas de los diarios de un paciente específico por fecha.
# del más reciente al más antiguo o viceversa.
# Actualiza la lista de entradas
@login_required
def sort_patient_entries(request, order):
    psychologist = request.user.psychologist
    patient_id = request.GET.get('patient_id')

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Patient not found.'})

    if patient not in psychologist.patients.all():
        return JsonResponse(
            {'status': 'error', 'message': 'You do not have permission to view this patient\'s entries.'})

    if order == 'recent':
        diaries_list = Entry.objects.filter(patient=patient).order_by('-date')
    else:
        diaries_list = Entry.objects.filter(patient=patient).order_by('date')

    updated_entry_list_html = render_to_string('partials/entry_list.html', {'diaries_list': diaries_list})
    return JsonResponse({'status': 'success', 'updated_entry_list_html': updated_entry_list_html})

# Vista que permite buscar entradas en el diario de un paciente por título o texto,
# permitiendo ver los diarios solo a los psicólogos vinculados al paciente.
# Entrega la lista de diarios actualizada.
@login_required
def search_patient_entries(request):
    query = request.GET.get('query', '')
    patient_id = request.GET.get('patient_id')

    if not patient_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Patient ID is required.'
        })

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Patient not found.'
        })

    if hasattr(request.user, 'psychologist'):
        psychologist = request.user.psychologist
        if patient not in psychologist.patients.all():
            return JsonResponse({
                'status': 'error',
                'message': 'You do not have permission to view this patient\'s entries.'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not authorized to perform this action.'
        })

    entries = Entry.objects.filter(patient=patient)
    if query:
        entries = entries.filter(Q(title__icontains=query) | Q(text__icontains=query)).order_by('-date')
    else:
        entries = entries.order_by('-date')

    context = {
        'diaries_list': entries
    }

    html = render_to_string('partials/entry_list.html', context)

    return JsonResponse({
        'status': 'success',
        'updated_entry_list_html': html
    })

# Vista que le permite a un psicólogo obtener las entradas del diario de un paciente específico.
# Entrega la lista de diarios.
@login_required
def get_entries_from_psych(request):
    try:
        patient_id = request.GET.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        diaries = Entry.objects.filter(patient=patient).order_by('-date')
        context = {'diaries_list': diaries}
        html = render_to_string('partials/entry_list.html', context)
        return JsonResponse({'status': 'success', 'updated_entry_list_html': html})
    except Patient.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Patient not found'})
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User is not a patient'})
