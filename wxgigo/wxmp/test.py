class Field(object):
    def __init__(self, *args, **kwargs):
        self.required = True

    def to_dict(self):
        return self.__dict__


class CharField(Field):
    def __init__(self, label, default=None, help_text=None, secret= False, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.type = "text"

        self.label = label
        self.default = None
        self.help_text = help_text
        # if input box shows as password style or not
        self.secret = secret

class ChoiceField(Field):
    def __init__(self, label, choices, default, help_text=None, *args, **kwargs):
        super(ChoiceField, self).__init__(*args, **kwargs)
        self.type = "choice"

        self.label = label
        self.choices = choices
        self.default = None
        self.help_text = help_text


class BasePluginConfig(object):
    def loads(self, settings):
      for k,v in self.__class__.__dict__.items():
        if not k.startswith('__') and not callable(v):
          self.__dict__[k] = settings[k] 

    def dumps(self):
      layout = self.get_layout()
      if not layout:
        print 'yes'

      d = {}
      for k,v in self.__class__.__dict__.items():
        if not k.startswith('__') and not callable(v):
            d[k] = v.to_dict()
      return d

    def get_layout(self):
      print "in parent layout"
      return None
   
class PluginConfig(BasePluginConfig):
    name = CharField(label='Name', help_text='Please input username') 
    a, b = ('A', 'B')

    def get_layout(self):
      print 'in child layout'
      return []


class Plugin(object):
  def __init__(self, config=None):
    self.config = config



#config = PluginConfig()

#settings = {'name':123}
#config.loads(settings)

#p = Plugin(config=config)

#print p.config.__dict__


#new_settings = {'name':456}
#p.config.loads(new_settings)
#print p.config.__dict__


p = PluginConfig()
print p.a
print p.b

