import unittest
from mulishtester import ObjectFactory

DEPARTMENT_TITLE = "Department Title"
PERSON_NAME = "Person name"

class DepartmentFactory(ObjectFactory):
    title = "Default department title"

class PersonFactory(ObjectFactory):
    name = PERSON_NAME
    department = DepartmentFactory(title=DEPARTMENT_TITLE)


class ReferenecedFactoryTest(unittest.TestCase):
    
    def test_success(self):
        person = PersonFactory.create()
        self.assertEqual(PERSON_NAME, person.name)
        self.assertEqual(DEPARTMENT_TITLE, person.department.title)
  