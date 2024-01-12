import xlsxwriter
from django.core.files import File
from django.db.models import Value
from django.db.models.functions import Concat
from rest_framework import serializers
from zappa.asynchronous import task

from monitoring.models import Record
from report.models import RecordReport

FIELDS = ('datetime_device', 'datetime_server', 'patient_identification', 'patient_name', 'variable_name', 'value',
          'alarm_name', 'alarm_operator', 'alarm_ref_value')


class RecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField()

    class Meta:
        model = Record
        fields = FIELDS


@task
def generate_excel_report(record_report_instance_id):
    report = RecordReport.objects.get(id=record_report_instance_id)
    excel_file_path = f'report_{report.patient_id}.xlsx'
    workbook = xlsxwriter.Workbook(excel_file_path)

    # Iterate over variables and create sheets
    try:
        for variable in report.variables.all():
            variable_records = Record.objects.filter(variable=variable, patient=report.patient,
                                                     datetime_device__gte=report.start_datetime,
                                                     datetime_server__lte=report.end_datetime). \
                annotate(patient_name=Concat('patient__first_name', Value(' '), 'patient__last_name'))

            worksheet = workbook.add_worksheet(variable.name)

            for col_num, header in enumerate(FIELDS):
                worksheet.write(0, col_num, header)

            for row_num, record in enumerate(variable_records, start=1):
                serialized_data = RecordSerializer(record).data
                for col_num, field in enumerate(FIELDS):
                    value = serialized_data[field]
                    worksheet.write(row_num, col_num, value)

        # Cierra el libro de trabajo
        workbook.close()

        # Upload file to S3
        with open(excel_file_path, 'rb') as excel_file:
            report.file.save(excel_file_path, File(excel_file))
    except Exception as error:
        report.error = str(error)
        report.status = RecordReport.Status.FAILED
    else:
        report.status = RecordReport.Status.SUCCESSFUL
    finally:
        report.save()
