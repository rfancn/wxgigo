from inspect import isfunction
from abc import ABCMeta, abstractmethod

class MetaPluginClass(type):
    BASIC_CONSTANTS = set(['NAME', 'VERSION', "DESCRIPTION", "AUTHOR"])
    BASIC_METHODS = set(['is_matched', 'process'])

    @classmethod
    def __check_basic_constants(cls, future_class_attr):
        # if future class doesn't contain enough basic constants, fail to initialize class
        if not cls.BASIC_CONSTANTS.issubset([ x.upper() for x in future_class_attr.keys()]):
            raise Exception("No enough basic constants: {0}".format(cls.BASIC_CONSTANTS))

    @classmethod
    def __check_basic_methods(cls, future_class_attr):
        """
        Deprecated as it use ABCMeta to do the same
        """
        future_class_method_names = [ k for k,v in future_class_attr.items()  if isfunction(v) ]
        # if future class doesn't contain enough basic methods, fail to initialize class
        if not cls.BASIC_METHODS.issubset(future_class_method_names):
            raise Exception("It need implements method: {0}".format(cls.BASIC_METHODS))

    @classmethod
    def __get_magic_constants(cls, future_class_attr):
        """
        1. Convert constants to lowercase
        2. Add 'meta_keys' for future reference
        """
        # for convernience purpose, convert to lowercase one for future reference
        for (name, value) in future_class_attr.items():
            if name.upper() in  cls.BASIC_CONSTANTS:
                future_class_attr.update({name.lower(): value})
                # remove the uppercase one
                del future_class_attr[name]

        #attrs = ((name, value) for name, value in future_class_attr.items() if name.upper() in cls.BASIC_CONSTANTS)
        #lowercase_attr = dict((name.lower(), value) for name, value in attrs)

        # store meta keys for future reference
        future_class_attr['meta_keys'] = set([ i.lower() for i in cls.BASIC_CONSTANTS])
        return future_class_attr

    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        cls.__check_basic_constants(future_class_attr)

        # this is basic OOP, nothing magic in there
        return type.__new__(cls, future_class_name, future_class_parents, cls.__get_magic_constants(future_class_attr))

class MixedMetaClass(ABCMeta, MetaPluginClass):
    """
    Mixed metaclass to inherit abstract function
    """
    pass

class BasePlugin(object):
    __metaclass__ =  MixedMetaClass
    NAME = None
    VERSION = None
    DESCRIPTION = None
    AUTHOR = None

    def __init__(self, config=None):
        self.config = config

    def update_config(self, config):
        self.config = config

    @abstractmethod
    def is_matched(self, recv):
        """
        Check if plugin will process Weixin Recv object
        """
        raise NotImplementedError

    @abstractmethod
    def process(self, recv):
        raise NotImplementedError

    @abstractmethod
    def get_processing_mode(self):
        return





