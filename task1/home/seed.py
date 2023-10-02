from faker import Faker
from random import choice
from .models import Student
import random
fake = Faker()

def generate_fake_data(num_records):
    gender_choices=['Male', 'Female', 'Other']
    for _ in range(num_records):
        name = fake.name()
        age = fake.random_int(min=18, max=25)
        idx=random.randint(0,len(gender_choices)-1)
        Student.objects.create(name=name, age=age, gender=gender_choices[idx])


