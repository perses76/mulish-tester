mulishtester
===============

mulishtester is object factory that can be used for testing as fixture replaces or data generator.


Credits
--------

Some ideas about class interfaces were taking from  `factory_boy <http://github.com/rbarrois/factory_boy>`_

Installation
------------

TODO

Create simple factory and generate Dummy Object
-----------------------------------------------
Here it is::

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

Referenced ObjectFactory and Callable as member of ObjectFactory
---------------------------------------------------------------------
You can use another ObjectFactory (referenced ObjectFactory)
or callable value (function or class) as attribute for ObjectFactory.
The argument for callable member becomes new object itself. so you can use attribute values defined earler.
Example::

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


Access to auto-generated number and factory object
-------------------------------------------------

For each generated object we add 2 additinal attributes:
 1. factory_object_id - autoincrement number that initalize for each factory
 2. factory - reference to factory object

You can use them inside callable members of Factory class::

    from mulishtester import ObjectFactory, DummyObject

    class CustomFactory(ObjectFactory):
        arg1 = "arg1"

    factory = CustomFactory()
    obj1 = factory.create()
    obj2 = factory.create()
    assert type(obj1.factory) == CustomFactory
    assert obj1.factory_object_id == 1
    assert obj2.factory_object_id == 2


Override default value in referenced factory
---------------------------------------------
You can override default value for referenced factory using special syntax: factory_name__attribute_name
Example::

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


Override model type for generation
----------------------------------
You can define class of the model for generation::

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

Check model attributes
-----------------------
If model is defined in Meta class. Factory checks attributes existense in gerenerated object.
If attribute does not exist in model, but Factory has this attribute, AttributeNotExistInModel thrown::

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


Chain call of model method
---------------------------
You can define what methods to be called in referenced ObjectFactory, when you call this method in generated object
There are 2 attributes that you can define in Meta class:
1. chain_call_func - functions that will be call in direct order. First  in referenced object and after in object.
2. reverse_chain_call_func - functions that will be call in reverse order. First in object and after in referenced object

Example::

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

And we want to call Deparment.save() method when we call Person.save() method before Person.save() processed
and to call Deparment.delete() method when we call Person.delete() method after Person.save() processed
We can do it defined chain_call_func and reverse_chain_call_func attributes in Meta Class
Example::

    from mulishtester import ModelFactory, MetaModel

    class DepartmentFactory(ModelFactory):
        class Meta(MetaModel):
            model = Department
        title = "IT Department"

    class PersonFactory(ModelFactory):
        class Meta(MetaModel):
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


Use PersistenceModelFactory for objects with save and delete methods
----------------------------------------------------------------------------------------
PersistenceModelFactory class has predefined meta data:
 chain_call_func = ["save"] and reverse_chain_call_func = ["delete"]
And you can use it for models with save and delete methods. For example models in Django
For models in prev. example, you can define factories like this::

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







