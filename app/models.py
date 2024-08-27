from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    """
    Model representing a basic kind of user on the platform who can register, login, and post diary entries.
    
    Fields:
        email (str): Unique email address for login.
        name (str): Full name of the patient, displayed on their diary page.
        password (str): Password used to login.
        birth_date (date): Birth date of the patient.
        photo (Image): Photo for the user.
        psychologists (ManyToMany): Psychologists who can see the patient's diary.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    photo = models.ImageField()
    name = models.CharField(max_length=80)

    psychologists = models.ManyToManyField('Psychologist', related_name='patients')

    def __str__(self):
        return f"patient: {self.name} ({self.user.email})"


class Psychologist(models.Model):
    """
    Model representing the kind of user qualified to evaluate and comment on patients' entries of their diaries.
    
    Fields:
        email (str): Unique email address for login.
        name (str): Full name of the psychologist, displayed on user diary pages.
        password (str): Password used to login.
        specialty (str): Area of specialty, displayed to patients on user diary pages.
        birth_date (Date): Birth date of the psychologist.
        photo (Image): Photo for the user.
        title (Image): Tittle of the specialty of the psychologist.
        entries (ManyToMany): Entries that the Psychlogist is able to see.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    specialty = models.CharField(max_length=80)
    birthdate = models.DateField()
    photo = models.ImageField()
    title = models.ImageField()

    def __str__(self):
        return f"psychologyst: {self.name} ({self.user.email})"


class Entry(models.Model):
    """
    Model representing an entry in a patient's diary that can be posted by the patient
    
    Fields:
        patient (ForeignKey): Reference to the Patient that owns the entry.
        date (date): Date of post of the diary entry.
        emotion (str): The primary emotion expressed in the entry (up to 10 characters).
        title (str): Title of the diary entry (up to 80 characters).
        text (str): Main text content of the diary entry (up to 280 characters).
        activities (list): List of activities associated with the diary entry.
        feelings (list): List of feelings associated with the diary entry.
    """

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

    date = models.DateTimeField()
    emotion = models.CharField(max_length=2)
    title = models.CharField(max_length=25)
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"entry: {str(self.patient).replace('patient: ', '')} - {self.title} - {self.date}"
