import unittest

from mulishtester.core import FactoryAttributesCollection, ConstField, FactoryAttribute

class FieldCollectionTest(unittest.TestCase):

    def test_constuctor(self):
        field1 = self.create_attr("arg1", "value1")
        field2 = self.create_attr("arg2", "value2")
        expected = FactoryAttributesCollection([field1, field2])
        fields = FactoryAttributesCollection([field1, field2])
        self.assertEqual(expected, fields)

    def test_append_new(self):
        field1 = self.create_attr("arg1", "value1")
        fields = FactoryAttributesCollection([field1])
        field2 = self.create_attr("arg2", "value2")
        fields.append(field2)
        expected_fields = [field1, field2]
        self.assertEqual(expected_fields, fields)

    def test_append_replace_existed(self):
        field1 = self.create_attr("arg1", "value1")
        fields = FactoryAttributesCollection([field1])
        field2 = self.create_attr("arg1", "value1_new")
        fields.append(field2)
        expected = FactoryAttributesCollection([field2])
        self.assertEqual(expected, fields)

    def test_extend(self):
        fields1 = FactoryAttributesCollection([self.create_attr("arg1", "value1")])
        fields2 = FactoryAttributesCollection([self.create_attr("arg1", "value1_new"),
                                               self.create_attr("new_arg", "new_arg_val")])
        new_fields = fields1.extend(fields2)
        new_fields_expected = FactoryAttributesCollection([self.create_attr("arg1", "value1_new"),
                                                           self.create_attr("new_arg", "new_arg_val")])
        expected_fields1 = FactoryAttributesCollection([self.create_attr("arg1", "value1")])
        self.assertEqual(new_fields_expected, new_fields)
        self.assertEqual(expected_fields1, fields1)

    def test_create_from_iterable(self):
        expected = FactoryAttributesCollection([self.create_attr("arg1", "value1"),
                                                self.create_attr("arg2", "value2")])
        fields = FactoryAttributesCollection((("arg1", "value1"), ("arg2", "value2"),))
        self.assertEqual(expected, fields)

    def create_attr(self, attr_name, value):
        return FactoryAttribute(attr_name, ConstField(value))



        
  