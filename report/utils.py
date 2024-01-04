import os


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'reports/{id}{ext}'.format(id=instance.id, ext=ext)
