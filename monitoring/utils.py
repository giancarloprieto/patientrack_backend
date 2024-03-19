from main.constants import Roles


def get_records_data_for_chart(records):
    values_str = '['
    for record in records:
        timestamp = record.datetime_device.strftime("%Y, %m-1, %d, %H, %M, %S")
        values_str += f"[new Date({timestamp}), {record.value}],"
    values_str = values_str.rstrip(',') + ']'
    return values_str


def get_patient_qs_filter(user, patient_prefix=False):
    groups = list(user.groups.values_list('name', flat=True))
    prefix = 'patient__' if patient_prefix else ''
    if user.is_patient:
        return {f'{prefix}user_id': user.id}
    elif user.is_staff and Roles.MEDICAL_STAFF in groups:
        return {f'{prefix}attending_staff__user_id': user.id}
