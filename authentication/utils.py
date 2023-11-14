import os


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'users/{id}/profile{ext}'.format(id=instance.id, ext=ext)