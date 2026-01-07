from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Student(models.Model):
    name= models.CharField(max_length=100,  validators=[
        RegexValidator(
            regex='^[A-Za-z ]+$',
            message='Only alphabets allowed in name field'
        )
    ]
)
    email=models.EmailField()
    course=models.CharField(max_length=100,  validators=[
        RegexValidator(
            regex='^[A-Za-z ]+$',
            message='Only alphabets allowed in  course field'
        )
    ])
    age=models.IntegerField()
    ph_no = models.CharField(max_length=15, validators=[RegexValidator(
    regex=r'^\d+$',
    message='Phone number should contain only digits'
) ])
    date = models.DateField(auto_now=True)

    
    def __str__(self):
        return self.name