from crispy_forms.layout import Field


class CustomCheckbox(Field):
    template = 'custom/checkbox-field.html'


class CustomRadio(Field):
    template = 'custom/radio-field.html'


class CustomSwitch(Field):
    template = 'custom/switch-field.html'
