import unittest
from mulishtester import ObjectFactory

class CustomFactory(ObjectFactory):
    arg1 = "arg1"

class FactoryObjectIdTest(unittest.TestCase):
    
    def test_for_class(self):
        obj = CustomFactory.create()
        self.assertEqual("arg1", obj.arg1)
        self.assertEqual(1, obj.factory_object_id)
        obj = CustomFactory.create()
        self.assertEqual(2, obj.factory_object_id)

    def test_for_instance(self):
        factory = CustomFactory()
        obj = factory.create()
        self.assertEqual("arg1", obj.arg1)
        self.assertEqual(1, obj.factory_object_id)
        obj = factory.create()
        self.assertEqual(2, obj.factory_object_id)

  