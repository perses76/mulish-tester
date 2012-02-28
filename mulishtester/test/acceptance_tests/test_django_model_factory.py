import unittest
from mulishtester import PersistenceModelFactory

class PersistenceModel(object):
    count = 0
    save_calls_history = []
    delete_calls_history = []

    def __init__(self):
        self.id = None

    def save(self):
        PersistenceModel.count += 1
        self.id = PersistenceModel.count

    def delete(self):
        self.id = None

class Department(PersistenceModel):

    def __init__(self):
        super(Department, self).__init__()
        self.title = None

class Person(PersistenceModel):

    def __init__(self):
        super(Person, self).__init__()
        self.name = None
        self.department = None

    def delete(self):
        if self.department.id is None:
            raise Exception("Department should be deleted after person")
        super(Person, self).delete()

    def save(self):
        if self.department.id is None:
            raise Exception("Department must be created before person")
        super(Person, self).save()


class DepartmentFactory(PersistenceModelFactory):
    class Meta:
        model = Department
    title = "IT Department"

class PersonFactory(PersistenceModelFactory):
    class Meta:
        model = Person
    name = "first_name last_name"
    department = DepartmentFactory()

class DjangoModelFactoryTest(unittest.TestCase):
    
    def test_save_delete(self):
        person = PersonFactory.create()
        person = person.save()
        self.assertEqual(person.id, 2)
        self.assertEqual(person.department.id, 1)
        person.delete()
        self.assertEqual(person.id, None)
        self.assertEqual(person.department.id, None)
        

  