from django import forms
from django.contrib.auth.models import User
from .models import Patient


class PatientForm(forms.Form):
    name = forms.CharField(max_length=80, label='Nombre completo', widget=forms.TextInput(
        attrs={'placeholder': "Introduzca su nombre y apellido", 'type': 'text'}))
    username = forms.CharField(max_length=80, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'placeholder': "Ejemplo: johndoe123", 'type': 'text'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.TextInput(
        attrs={'placeholder': "Introduzca la dirección de su correo electrónico", 'type': 'email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Elija una contraseña para ingresar a su cuenta'}),
        label='Contraseña')
    birthdate = forms.DateField(label='Fecha de nacimiento',
                                widget=forms.TextInput(attrs={'placeholder': "Haga clic para seleccionar fecha",
                                                              'type': "text",
                                                              'onfocus': "(this.type='date')",
                                                              'onblur': "(this.type='text')",
                                                              'id': "birthdate"}))
    photo = forms.FileField(label='Foto de perfil', widget=forms.FileInput(attrs={'placeholder': "Foto de perfil",
                                                                                  'type': 'file',
                                                                                  'id': 'img',
                                                                                  'accept': "image/png, image/jpg, image/jpeg, image/gif"}))


class PsychologistForm(forms.Form):
    name = forms.CharField(max_length=80, label='Nombre completo', widget=forms.TextInput(
        attrs={'placeholder': "Introduzca su nombre y apellido", 'type': 'text'}))
    username = forms.CharField(max_length=80, label='Nombre de usuario',
                               widget=forms.TextInput(attrs={'placeholder': "Ejemplo: johndoe123", 'type': 'text'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.TextInput(
        attrs={'placeholder': "Introduzca la dirección de su correo electrónico", 'type': 'email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Elija una contraseña para ingresar a su cuenta'}),
        label='Contraseña')
    birthdate = forms.DateField(label='Fecha de nacimiento',
                                widget=forms.TextInput(attrs={'placeholder': "Haga clic para seleccionar fecha",
                                                              'type': "text",
                                                              'onfocus': "(this.type='date')",
                                                              'onblur': "(this.type='text')",
                                                              'id': "birthdate"}))
    specialty = forms.ChoiceField(label="Especialidad", choices=[
        ('default', 'Seleccionar especialidad...'),
        ('Psicología Clínica', 'Psicología Clínica'),
        ('Psicología Educativa', 'Psicología Educativa'),
        ('Psicología Infantil', 'Psicología Infantil'),
        ('Psicología de la Salud', 'Psicología de la Salud'),
        ('Neuropsicología', 'Neuropsicología'),
        ('Psicología Ocupacional', 'Psicología Ocupacional'),
        ('Psicología Social', 'Psicología Social'),
        ('Psicología del Deporte', 'Psicología del Deporte'),
        ('Psicoterapia', 'Psicoterapia'),
        ('Psiquiatría', 'Psiquiatría'),
        ('Psiquiatría Geriátrica', 'Psiquiatría Geriátrica'),
        ('Psiquiatría Infantil y de Adolescentes', 'Psiquiatría Infantil y de Adolescentes'),
        ('Psiquiatría de Adicciones', 'Psiquiatría de Adicciones'),
    ], widget=forms.Select(attrs={"id": "specialty"}))

    photo = forms.FileField(label='Foto de perfil', widget=forms.FileInput(attrs={'placeholder': "Foto de perfil",
                                                                                  'type': 'file',
                                                                                  'id': 'img',
                                                                                  'accept': "image/png, image/jpg, image/jpeg, image/gif"}))

    title = forms.FileField(label='Foto de su título', widget=forms.FileInput(attrs={'placeholder': "Foto de perfil",
                                                                                     'type': 'file',
                                                                                     'id': 'titles',
                                                                                     'accept': "image/png, image/jpg, image/jpeg, image/gif, image/pdf"}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80, label='Nombre de usuario o email', widget=forms.TextInput(
        attrs={'placeholder': "Nombre de usuario o email", 'type': 'text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), label='Contraseña')
