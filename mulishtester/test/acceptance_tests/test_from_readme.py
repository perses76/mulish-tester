import unittest

class TestsFromReadMe(unittest.TestCase):

    def test_base_use(self):
        from mulishtester import ObjectFactory, DummyObject

        class CustomFactory(ObjectFactory):
            arg1 = "arg1"
            arg2 = "arg2"
            arg3 = "arg3"


        #use class method to generate object
        obj = CustomFactory.create()
        assert type(obj) == DummyObject
        assert obj.arg1 == "arg1"
        assert obj.arg2 == "arg2"
        assert obj.arg3 == "arg3"

        #You can override default value in factory constructor or in create method
        factory = CustomFactory(arg2="instance_arg2")
        obj = factory.create(arg3="method_arg3")
        assert obj.arg1 == "arg1"
        assert obj.arg2 == "instance_arg2"
        assert obj.arg3 == "method_arg3"

    def test_referenced_and_callable_fields(self):
        from mulishtester import ObjectFactory

        class BaseFactory(ObjectFactory):
            base_arg = "base_arg"

        class ChildFactory(ObjectFactory):
            base = BaseFactory()
            child_arg = "child_arg"

            def child_arg_plus_something(self):
                return self.child_arg + "+something"


        obj = ChildFactory.create()
        assert obj.child_arg == "child_arg"
        assert obj.base.base_arg == "base_arg"
        assert obj.child_arg_plus_something == "child_arg"+ "+something"

    def test_factory_object_id(self):
        from mulishtester import ObjectFactory, DummyObject

        class CustomFactory(ObjectFactory):
            arg1 = "arg1"

        factory = CustomFactory()
        obj1 = factory.create()
        obj2 = factory.create()
        assert type(obj1.factory) == CustomFactory
        assert obj1.factory_object_id == 1
        assert obj2.factory_object_id == 2

    def test_complex_attr_name(self):
        from mulishtester import ObjectFactory

        class BaseFactory(ObjectFactory):
            base_arg1 = "base_arg1"
            base_arg2 = "base_arg2"
            base_arg3 = "base_arg3"

        class ChildFactory(ObjectFactory):
            base = BaseFactory()
            child_arg = "child_arg"

        factory = ChildFactory(base__base_arg2 = "child2")
        obj = factory.create(base__base_arg3 = "child3")
        assert obj.base.base_arg1 == "base_arg1"
        assert obj.base.base_arg2 == "child2"
        assert obj.base.base_arg3 == "child3"
        assert obj.child_arg == "child_arg"


    def test_model_fabric(self):
        from mulishtester import ObjectFactory

        class Custom(object):
            def __init__(self):
                self.arg1 = None

        class CustomFactory(ObjectFactory):
            class Meta:
                model = Custom
            arg1 = "arg1"

        obj = CustomFactory.create()
        assert type(obj) == Custom
        assert obj.arg1 == "arg1"

    def test_check_model_signature(self):
        from mulishtester import ObjectFactory, AttributeNotExistInModel

        class Custom(object):
            def __init__(self):
                self.arg1 = None

        class CustomFactory(ObjectFactory):
            class Meta:
                model = Custom
            arg_not_exist = "arg1"

        try:
            CustomFactory.create() # here AttributeNotExistInModel thrown
            assert False
        except AttributeNotExistInModel:
            pass

    def test_call_in_chain(self):
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
                super(Department, self).__init__()
                self.title = None

        class Person(PersistenceModel):

            def __init__(self):
                super(Person, self).__init__()
                self.name = None
                self.department = None



        from mulishtester import ObjectFactory

        class DepartmentFactory(ObjectFactory):
            class Meta:
                model = Department
            title = "IT Department"


        class PersonFactory(ObjectFactory):
            class Meta:
                model = Person
                chain_call_func = ["save"]
                reverse_chain_call_func = ["delete"]
            name = "first_name last_name"
            department = DepartmentFactory()

        person = PersonFactory.create().save()
        assert person.id == 2
        assert person.department.id == 1
        person.delete()
        assert person.id == None
        assert person.department.id == None

    # and Djnago Model Factory Test

        from mulishtester import PersistenceModelFactory
        PersistenceModel.count = 0
        class DepartmentFactory(PersistenceModelFactory):
            class Meta:
                model = Department
            title = "IT Department"

        class PersonFactory(PersistenceModelFactory):
            class Meta:
                model = Person
            name = "first_name last_name"
            department = DepartmentFactory()

        person = PersonFactory.create().save()

        assert person.id == 2
        assert person.department.id == 1
        person.delete()
        assert person.id == None
        assert person.department.id == None










  