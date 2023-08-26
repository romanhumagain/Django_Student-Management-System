# to create a dumy data to the model

from faker import Faker
from . models import DumyStudent , DumyDepartment
import random
fake = Faker()

departments = DumyDepartment.objects.all()
def generate_student_data(num):
  for _ in range(num):
    DumyStudent.objects.create(
      department = fake.random_element(elements = departments ),
      name = fake.name(),
      address = fake.address(),
      email = fake.email(),
      age = fake.random_int(min=18 , max= 30)
    )