# forms.py
from django import forms
from django.forms.fields import TypedChoiceField, DateField, MultipleChoiceField, ChoiceField, DateTimeField, \
    BooleanField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField, ModelForm


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')


class FormFieldRenderMixin(object):

    def __init__(self, *args, **kwargs):
        super(FormFieldRenderMixin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            self.field_rendering(visible)

    def field_rendering(self, visible):
        if isinstance(visible.field, (ModelChoiceField, TypedChoiceField, ChoiceField,)):
            visible.field.widget.attrs.update({'class': 'form-select'})
        elif isinstance(visible.field, (ModelMultipleChoiceField, MultipleChoiceField,)):
            visible.field.widget.attrs.update({'class': 'form-select miSelect'})
        elif isinstance(visible.field, (DateField,)):
            visible.field.widget.attrs = {'type': 'date', 'class': 'date-picker form-control', 'autocomplete': 'off'}
        elif isinstance(visible.field, (DateTimeField,)):
            visible.field.widget.attrs = {'type': 'date', 'class': 'date-picker form-control', 'autocomplete': 'off'}
        elif isinstance(visible.field, (BooleanField,)):
            visible.field.widget.attrs = {'class': 'form-check-input'}
        else:
            visible.field.widget.attrs = {'class': 'form-control'}


class BaseModelForm(FormFieldRenderMixin, ModelForm):
    pass