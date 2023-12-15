from django import template

register = template.Library()


@register.filter(name='get_variable_record')
def get_variable_record(patient_obj, variable_id):
    record_list = getattr(patient_obj, f'latest_{variable_id}_record')
    if record_list:
        return record_list[0]
