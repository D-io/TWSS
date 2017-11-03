# -*- coding: utf-8 -*-

import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

from django.http import HttpResponse, StreamingHttpResponse

from project.views import database_management


def database(request):
    request.encoding = 'utf-8'

    from project.utilities.indentity import check_identity
    check_return = check_identity(request)
    if check_return == False:
        return False  # 返回错误信息
    else:
        user = check_return

    requestfor = request.POST['requestfor']
    if requestfor == 'database_backup':
        return database_backup(request)
    if requestfor == 'backup_download':
        return buckup_download(request)
    if requestfor == 'buckup_delete':
        return buckup_delete(request, user)


def database_backup(request):
    if request.POST['filename']:
        filename = request.POST['filename']
    else:
        filename = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())

    full_filename = BASE_DIR + '/project/database_backups/' + filename + '.json'

    os.system('cd ' + BASE_DIR)
    os.system('python3 manage.py dumpdata > ' + full_filename)
    os.system('mysqldump -uroot -pzql twss > ' + full_filename)

    os.system('chmod 444 ' + full_filename)

    file = open(full_filename)
    # response = StreamingHttpResponse(file.read())
    response = HttpResponse(file.read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}.json"'.format(filename)
    return response


def buckup_download(request):
    filename = request.POST['buckup_id']
    file = open(BASE_DIR + '/project/database_backups/' + filename)

    response = HttpResponse(file.read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}.json"'.format(filename)
    return response


def buckup_delete(request, user):
    filename = request.POST['request_data']
    full_filename = BASE_DIR + '/project/database_backups/' + filename

    os.remove(full_filename)

    return database_management(request, user)