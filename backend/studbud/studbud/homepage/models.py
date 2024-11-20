from django.db import models

# Create your models here.

class User(models.Model):
    classes = [
        ("CS135", "CS135"),
        ("MATH135", "MATH135"),
        ("MATH137", "MATH137"),
        ("COMMST223", "COMMST223"),
        ("ECON101", "ECON101"),
    ]
    genders = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    study_times = [
        ("Morning", "Morning"),
        ("Afternoon", "Afternoon"),
        ("Night", "Night"),
    ]
    personalities = [
        ("Introvert", "Introvert"),
        ("Extrovert", "Extrovert"),
    ]
    learning_styles = [
        ("Audio", "Audio"),
        ("Visual", "Visual"),
        ("Kinaesthetic", "Kinaesthetic"),
    ]
    
    name = models.CharField(max_length=100)
    courseCode = models.CharField(max_length=200, choices=classes)
    gender = models.CharField(max_length=20, choices=genders)
    preftime = models.CharField(max_length=20, choices=study_times)
    personality = models.CharField(max_length=20, choices=personalities)
    learning_style = models.CharField(max_length=20, choices=learning_styles)

    def __str__(self):
        return self.name
