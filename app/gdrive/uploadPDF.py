from googleapiclient.http import MediaFileUpload
from . import create_service

drive_service = create_service()


def uploadPDF(filepath, filename):
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
    response = drive_service.permissions().create(
        fileId=file_id,
        body=user_permissions
    ).execute()
    response = drive_service.files().get(fileId=file_id, fields='webContentLink,webViewLink').execute()
    return {"webViewLink": response.get('webViewLink'), "webContentLink": response.get('webContentLink')}
