import xlsxwriter
from django.core.files import File
from rest_framework import serializers

from monitoring.models import Record
from report.models import RecordReport


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('datetime_device', 'datetime_server', 'patient_identification', 'variable_name', 'value')


def generate_excel_report(record_report_instance_id):
    report = RecordReport.objects.get(id=record_report_instance_id)
    excel_file_path = f'report_{report.patient_id}.xlsx'
    workbook = xlsxwriter.Workbook(excel_file_path)

    # Iterate over variables and create sheets
    for variable in report.variables.all():
        variable_records = Record.objects.filter(variable=variable, patient=report.patient)

        worksheet = workbook.add_worksheet(variable.name)

        headers = ('datetime_device', 'datetime_server', 'patient_identification', 'variable_name', 'value')
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        for row_num, record in enumerate(variable_records, start=1):
            serialized_data = RecordSerializer(record).data
            for col_num, field in enumerate(headers):
                value = serialized_data[field]
                worksheet.write(row_num, col_num, value)


    # Cierra el libro de trabajo
    workbook.close()

    # Upload file to S3
    with open(excel_file_path, 'rb') as excel_file:
        report.file.save(excel_file_path, File(excel_file))
