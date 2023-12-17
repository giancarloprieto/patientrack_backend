import django
import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patientrack.settings')
django.setup()

from patient.models import Patient
from device.models import Device, Variable
from monitoring.models import Record

patient = Patient.objects.get(id=1)
device = Device.objects.get(patient=patient)

data = {
    'temperatura': [35, 37, 34.5, 35.8, 39.7, 34.6, 38.2, 36.5, 28.4, 33.6, 37.5],
    'ritmo cardiaco': [120, 130, 140, 150, 95, 94, 93, 88, 106, 100, 131, 117, 128],
}

dt = datetime(2023, 12, 16, 13, 0, 0)

for var_name, values in data.items():
    variable = Variable.objects.get(name__icontains=var_name)
    for value in values:
        dt += timedelta(minutes=15)
        record = Record(
            datetime_server=dt,
            datetime_device=dt,
            patient=patient,
            patient_identification=patient.identification,
            device=device,
            device_identifier=device.identifier,
            variable=variable,
            variable_name=variable.name,
            value=value,
            payload='1jajrwuw'

        )
        record.save()
