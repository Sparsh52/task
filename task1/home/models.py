from django.db import models
# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    def __str__(self) -> str:
        return str(self.name)+" "+str(self.gender)
    class Meta:
        ordering=['name']
