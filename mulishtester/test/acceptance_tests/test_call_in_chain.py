import unittest
from mulishtester import ObjectFactory


class PersistenceModel(object):
    count = 0


    def __init__(self):
        self.id = None

    def save(self):
        PersistenceModel.count += 1
        self.id = PersistenceModel.count

    def delete(self):
        self.id = None

class Department(PersistenceModel):

    def __init__(self):
        self.title = None


class Person(PersistenceModel):

    def __init__(self):
        self.first_name = None
        self.department = None

    def delete(self):
        if self.department.id is None:
            raise Exception("Department should be deleted after person")
        super(Person, self).delete()

    def save(self):
        if self.department.id is None:
            raise Exception("Department must be created before person")
        super(Person, self).save()
        

class DepartmentFactory(ObjectFactory):
    class Meta:
        model = Department
    title = "Department title"

class PersonFactory(ObjectFactory):
    class Meta:
        model = Person
        chain_call_func = ["save"]
        reverse_chain_call_func = ["delete"]
    first_name = "First Name"
    department = DepartmentFactory()


class CallInChainTest(unittest.TestCase):
    
    def test_save_success(self):
        person = PersonFactory.create().save()
        self.assertEqual(1, person.department.id)
        self.assertEqual(2, person.id)

    def test_delete_success(self):
        person = PersonFactory.create()
        person.id = 1
        person.department.id = 1
        person = person.delete()
        self.assertEqual(None, person.id)
        self.assertEqual(None, person.department.id)

  