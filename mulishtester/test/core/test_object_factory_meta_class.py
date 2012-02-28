import unittest

from mulishtester.core import ObjectFactoryMetaClass, factorymethod, FactoryAttributesCollection, ConstField, CallableField

def my_func(obj):
    pass

class CustomFactory(object):
    factory_attributes = FactoryAttributesCollection()
    __metaclass__ = ObjectFactoryMetaClass

    class Meta:
        pass

    class MetaDefault:
        pass

    arg1 = "arg1_value"
    arg2 = ConstField("value")

    arg3 = my_func

    @factorymethod
    def my_factory_method(self):
        pass

class ObjectFactoryMetaClassTest(unittest.TestCase):
    
    def test_read_factory_feilds(self):
        custom_factory = CustomFactory
        factory_attributes = custom_factory.factory_attributes
        expected_attributes = FactoryAttributesCollection([
            ("arg1", ConstField("arg1_value")),
            ("arg2", ConstField("value")),
            ("arg3", CallableField(my_func))
        ])
        self.assertEqual(expected_attributes, factory_attributes)
        # self.assertEqual(factorymethod, type(custom_factory.my_factory_method))
        self.assertFalse(hasattr(custom_factory, "arg1"))
        self.assertFalse(hasattr(custom_factory, "arg2"))