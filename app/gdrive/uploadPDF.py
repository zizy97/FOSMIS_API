from googleapiclient.http import MediaFileUpload
from . import create_service
from ..logging import logging

log = logging.getLogger(__name__)

drive_service = create_service()


def uploadPDF(filepath, filename):
    log.info(f"{filename} Started to Upload")
    results = drive_service.files().list(fields="files(id,name)").execute()
    items = results.get('files', [])
    dic = {}
    for item in items:
        dic.update({item.get('name'): item.get('id')})

    if filename not in dic:
        log.info(f"{filename} Uploading......")
        file_metadata = {'name': filename, "parents": ['18X9FVtm0L0LrEvfiFXe0KqcJKSz30G_3']
                         }
        media = MediaFileUpload(filepath, mimetype='application/pdf', resumable=True)
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            ).execute()

        file_id = file.get('id')
        user_permissions = {
            'type': 'anyone',
            'role': 'reader'
        }
        drive_service.permissions().create(
            fileId=file_id,
            body=user_permissions
        ).execute()
    else:
        log.info(f"{filename} exist on drive no need to upload!")
        file_id = dic[filename]
    response = drive_service.files().get(fileId=file_id, fields='webContentLink,webViewLink').execute()
    return {"download": response.get('webContentLink'), "view": response.get('webViewLink')}
