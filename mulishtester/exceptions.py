class MockFactoryException(Exception):
    """Base exception for ModelFactory Project"""
    pass

ATTRIBUTE_NOT_EXISTS_IN_MODEL_TEMPLATE = "Attribute '%s' does not exist in model '%s'"

class AttributeNotExistInModel(MockFactoryException):
    """raise when create_object function try to assign attribute that not exist in mocked model"""
    def __init__(self, model, attr_name):
        self.model = model
        self.attr_name = attr_name

    def __str__(self):
        return ATTRIBUTE_NOT_EXISTS_IN_MODEL_TEMPLATE % (self.attr_name, self.model)