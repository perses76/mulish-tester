import unittest
from mulishtester import ObjectFactory

DEPARTMENT_TITLE = "Department Title"
PERSON_NAME = "Person name"

class Department(object):
    def __init__(self):
        self.title = None

class Person(object):
    def __init__(self):
        self.name = None
        self.department = None

class DepartmentFactory(ObjectFactory):
    class Meta:
        model = Department
    title = "Default department title"

class PersonFactory(ObjectFactory):
    class Meta:
        model = Person
    name = PERSON_NAME
    department = DepartmentFactory()


class ComplexAttrNameTest(unittest.TestCase):
    """Tests for complex attribute"""

    def test_define_for_instance(self):
        person_factory = PersonFactory(department__title=DEPARTMENT_TITLE)
        person = person_factory.create()
        self.assertEqual(DEPARTMENT_TITLE, person.department.title)

    def test_define_for_method(self):
        person_factory = PersonFactory()
        person = person_factory.create(department__title=DEPARTMENT_TITLE)
        self.assertEqual(DEPARTMENT_TITLE, person.department.title)

        
  