from exceptions import AttributeNotExistInModel

# reversed name of attributes in factories that will not be converted to FactoryAttribute
RESERVED_NAMES_FOR_FACTORIES = ["factory_attributes",  "Meta", "MetaDefault", "factory", "factory_object_id"]

class DummyObject(object):
    """Object generated by Factory if model is not defined"""
    pass


class FactoryAttribute(object):
    """Factory attribute for object generation"""
    def __init__(self, attr_name, field):
        self.attr_name = attr_name
        self.field = field

    def assign_attr(self, parent_obj):
        """Assign attribute to object
        :param parent_obj: object where value will be assign"""
        setattr(self._get_target(parent_obj), self._get_attr_name(), self.field.get_value(parent_obj))

    def is_complex_attr_name(self):
        """
        return True if name of attribute is complex: containes referenced objects and method separeated by __
        :return:
        """
        return  "__" in self.attr_name

    def _get_target(self, parent_obj):
        """
        Return target object for attribute. if attribute has compex name then we need to find actual target object where
        value generated by attribute will be assign
        :param parent_obj: object that will be generated by factory
        :return: target object where value will be assign
        """
        ar = self.attr_name.split("__")
        target = parent_obj
        for step in ar[:-1]:
            target = getattr(target, step)
        return target

    def _get_attr_name(self):
        """
        Return attribute name. if attribute is complex return last part (after __) of attr_name
        :return: string
        """
        ar = self.attr_name.split("__")
        return ar[-1]

    def __hash__(self):
        """
        Hash value of Factory Attribute
        :return: integer
        """
        return hash(repr(self))

    def __eq__(self, other):
        """
        Override == operator
        :param other: other object to compare with
        :return: boolean
        """
        return hash(self) == hash(other)

    def __repr__(self):
        """
        Return string presentation using in tests
        :return: string
        """
        return "%s:%s" % (self.attr_name , repr(self.field))

def create_factory_field(value):
    """
    Constructor for FactoryField. if value is FactoryField, return value,
    if value is callable returns CallableFactory, otherwise return ConstFactory
    :param value: value for FactoryField
    :return: FactoryField Object depending from value.
    """
    if isinstance(value, FactoryField):
        return value

    if hasattr(value, "__call__"):
        return CallableField(value)

    return ConstField(value)

class FactoryField(object):
    """Base class for all factory field"""

    def get_value(self, parent_obj=None):
        """
        Return value genenerated by Factory Field
        :param parent_obj:
        :return: object
        """
        raise NotImplemented("Must be redefine in child class")

    def __eq__(self, other):
        return hash(self) == hash(other)

class ConstField(FactoryField):
    """
    Factory field for constant values like: stirng, integer, datetime....
    """

    def __init__(self, value):
        FactoryField.__init__(self)
        self.value = value

    def get_value(self, parent_obj=None):
        return self.value

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return str(self.value)


class CallableField(FactoryField):
    """
    Factory field for callable values: functions. classes
    """
    def __init__(self, func):
        FactoryField.__init__(self)
        self.func = func

    def get_value(self, parent_obj=None):
        return self.func(parent_obj)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return str(self.func)


class FactoryAttributesCollection(object):
    """
    Collections of FactoryAttributes object
    """
    def __init__(self, attributes=None):
        """
        FactoryAttributesCollection Constructor
        :param attributes: can be None, dictionary, iterable or FactoryAttributesCollection
        :return:
        """
        self.attributes = self._initialize_data(attributes)

    def _initialize_data(self, attributes):
        """Convert constructor argument to internal data structure"""
        if attributes is None:
            return []
        if isinstance(attributes, dict):
           return [FactoryAttribute(key, create_factory_field(value))
                   for key, value in attributes.items()]

        if hasattr(attributes, "__iter__"):
            try:
                return [FactoryAttribute(key, create_factory_field(value))
                        for key, value in attributes]
            except TypeError:
                pass
        
        return attributes

    def __iter__(self):
        return self.attributes.__iter__()

    def __getitem__(self, attr_name):
        result = [attr for attr in self.attributes if attr.attr_name == attr_name]
        if result:
            return result[0]
        else:
            raise AttributeError("Can not find field '%s'" % attr_name)

    def append(self, attr):
        """append new attribute to collection
        if attribute with same attr_name already exists, it will be replaced with new one
        """
        try:
            existed_attrd= self[attr.attr_name]
            index = self.attributes.index(existed_attrd)
            self.attributes[index] = attr
        except AttributeError:
            self.attributes.append(attr)

    def extend(self, attrs):
        """Create new FactoryAttributesCollection from existed attributes and attributes in attr """
        new_attrs = self._copy()
        if attrs:
            for attr in attrs:
                new_attrs.append(attr)
        return new_attrs

    def _copy(self):
        """Create copy of FactoryAttributesCollection"""
        copy_data = self.attributes[:]
        return FactoryAttributesCollection(copy_data)

    def __repr__(self):
        return "{"+"}{".join([str(attr) for attr in self.attributes])+"}"

    def __eq__(self, other):
        self_hash = dict([(hash(attr), attr) for attr in self])
        other_hash = dict([(hash(attr), attr) for attr in other])
        for key in self_hash.keys():
            if not other_hash.has_key(key):
                return False
        for key in other_hash.keys():
            if not self_hash.has_key(key):
                return False
        return True

class factorymethod(object):
    """
    decorator for factory methods.
    Factory methods are not copied to created object
    """
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, klass=None):
        if obj is None:
          obj = klass
        def newfunc(*args, **kwargs):
           return self.f(obj, *args, **kwargs)
        return newfunc


def is_attribute_field(key, value):
    """check if attribute in factory class defenition is factory field"""
    return not isinstance(value, factorymethod) \
           and not key.startswith("__") and not key in RESERVED_NAMES_FOR_FACTORIES

def extend_Meta(meta, meta_default):
    """Extend Meta class defiented in Factory wth Default Meta class"""
    for key in dir(meta_default):
        if not key.startswith("__") and not hasattr(meta, key):
            setattr(meta, key, getattr(meta_default, key))


class ObjectFactoryMetaClass(type):
    """Meta class for Object Factory Class"""
    def __new__(mcs, classname, bases, class_dict):
        """create FactoryAttributes from class memberes and store them in factory_attributes attribute of class
        Extend Meta class data with Default Meta class data
        """
        factory_attributes = FactoryAttributesCollection([(key, value) for key, value in class_dict.items()
                                            if is_attribute_field(key, value)])
        class_dict = dict([(key, value) for key, value in class_dict.items()
                                            if not is_attribute_field(key, value)])

        new_class =  type.__new__(mcs, classname, bases, class_dict)
        new_class.factory_attributes = factory_attributes
        extend_Meta(new_class.Meta, new_class.MetaDefault)
        return new_class


class MetaDataBase:
    """Base meta data definition for meta classes in Factory"""
    model = DummyObject
    chain_call_func = []
    reverse_chain_call_func = []
    check_method_attributes = False


class ChainCallWrapper(object):
    """Wrapper for methods have to be called in chain"""
    def __init__(self, obj, func_name, reverse_call=False):
        self.obj = obj
        self.func_name = func_name
        self.reverse_call = reverse_call
        self.func = getattr(self.obj, self.func_name)
        self.sub_factories = [attr for attr in self.obj.factory.factory_attributes
                              if isinstance(attr.field, ObjectFactory)]
        
    def __call__(self, *args, **kwargs):
        if self.reverse_call:
            self.func(*args, **kwargs)
            self.call_func_in_subfactories(*args, **kwargs)
        else:
            self.call_func_in_subfactories(*args, **kwargs)
            self.func(*args, **kwargs)
        return self.obj

    def call_func_in_subfactories(self, *args, **kwargs):
        """call func for all referenced objects in object"""
        for factory in self.sub_factories:
            sub_obj = getattr(self.obj, factory.attr_name)
            func = getattr(sub_obj, self.func_name)
            func(*args, **kwargs)
    

class ObjectFactory(FactoryField):
    """Base class for Object Factory"""
    __metaclass__ = ObjectFactoryMetaClass
    factory_attributes = FactoryAttributesCollection()
    factory_object_id = 0

    class Meta(MetaDataBase):
        """Meta data"""
        pass

    class MetaDefault(MetaDataBase):
        """Default meta data"""
        pass

    def __init__(self, **kwargs):
        self.factory_attributes = self.factory_attributes.extend(FactoryAttributesCollection(kwargs))
        self.factory_object_id = 0
        FactoryField.__init__(self)

    @factorymethod
    def create_factory(self, **kwargs):
        """Create new factory for kwargs arguments"""
        if not kwargs:
            return self
        if isinstance(self, FactoryField):
            new_factory = self.__class__()
        else:
            new_factory = getattr(self, "__call__")()
        new_factory.factory_attributes = self.factory_attributes.extend(FactoryAttributesCollection(kwargs))
        new_factory.get_factory_id = self.get_factory_id
        return new_factory

    @factorymethod
    def create(self, **kwargs):
        """generate object from factory"""
        new_factory = self.create_factory(**kwargs)
        obj = new_factory.get_value()
        return obj

    @factorymethod
    def get_value(self, parent_obj=None):
        """Return object generated by factory"""
        obj = self.create_object()
        obj.factory_object_id = self.get_factory_id()
        obj.factory = self
        if self.Meta.model != DummyObject:
            self.check_model_signature(obj)
        for field in self.factory_attributes:
            field.assign_attr(obj)
        self.wrap_chain_call_methods(obj)
        return obj

    @factorymethod
    def check_model_signature(self, obj):
        """Check if model has attributes defined in factory"""
        for field in self.factory_attributes:
            if not field.is_complex_attr_name() and  not hasattr(obj, field.attr_name):
                raise AttributeNotExistInModel(obj, field.attr_name)

    @factorymethod
    def create_object(self):
        """Create new object"""
        return self.Meta.model()

    @factorymethod
    def get_factory_id(self):
        """Return new auto-incremented number, that can be used as object id"""
        self.factory_object_id += 1
        return self.factory_object_id

    @factorymethod
    def wrap_chain_call_methods(self, obj):
        """Wrap object methods for chain call and reverse chain call"""
        [setattr(obj, func_name, ChainCallWrapper(obj, func_name))
         for func_name in self.Meta.chain_call_func]
        [setattr(obj, func_name, ChainCallWrapper(obj, func_name, reverse_call=True))
         for func_name in self.Meta.reverse_chain_call_func]


class PersistenceModelFactory(ObjectFactory):
    """Object factory with predefined chain_call_func and reverse_chain_call_func"""
    class MetaDefault(MetaDataBase):
        model = None
        chain_call_func = ["save"]
        reverse_chain_call_func = ["delete"]





        
        






        
    