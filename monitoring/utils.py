def get_records_data_for_chart(records):
    values_str = '['
    for record in records:
        timestamp = record.datetime_device.strftime("%Y, %m, %d, %H, %M, %S")
        values_str += f"[new Date({timestamp}), {record.value}],"
    values_str = values_str.rstrip(',') + ']'
    return values_str
