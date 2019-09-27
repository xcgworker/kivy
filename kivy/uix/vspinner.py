from kivy.compat import string_types
from kivy.uix.spinner import Spinner,SpinnerOption
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty, AliasProperty,ObjectProperty
from kivy.factory import Factory


       
class VSpinnerOption(SpinnerOption):
    value=StringProperty()

'''
和Spinner不同的是，区别text和value,
text 是Spinner显示的值
value 是VSpinner on_select 发送信号所带的数据

数据由values指定，它是ListProperty,每一个是一个Dict,包含两个字段,text,和value
''' 
class VSpinner(Spinner):
    values=ListProperty()
    option_cls = ObjectProperty(VSpinnerOption)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_select')
        self.fbind('values', self._update_dropdown)
        
    def _update_dropdown(self, *largs):
        dp = self._dropdown
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        dp.clear_widgets()
        for data in values:
            item = cls(text=data['text'],value=data['value'])
            item.height = self.height if self.sync_height else item.height
            item.bind(on_release=lambda option: dp.select(option))
            dp.add_widget(item)

        if text_autoupdate:
            if values:
                if not self.text or self.text not in values:
                    self.text = data[0].text
            else:
                self.text = ''  
                  
    def _on_dropdown_select(self, instance, data, *largs):
        super()._on_dropdown_select(instance, data.text, *largs)
        self.dispatch('on_select',data.value)
        
    def on_select(self,data):
        pass
        