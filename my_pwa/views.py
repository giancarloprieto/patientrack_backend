import boto3
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponse

from patientrack import settings


from django.http import HttpResponse
from django.conf import settings

def service_worker(request):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_key = 'static/serviceWorker.js'

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        return HttpResponse(content, content_type='application/javascript')
    except NoCredentialsError:
        return HttpResponse("Error: No se proporcionaron credenciales de AWS.", status=500)
    except Exception as e:
        return HttpResponse(f"Error al obtener el archivo: {str(e)}", status=500)