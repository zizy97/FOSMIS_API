import pathlib
import os

from .gdrive import uploadPDF
from . import logging

log = logging.getLogger(__name__)

dirName = 'pdf'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory ", dirName, " Created ")
except FileExistsError:
    print("Directory ", dirName, " already exists")


def download_file(ses, url, filename):
    path = str(pathlib.Path().absolute()) + f'/pdf/{filename}.pdf'
    if not os.path.exists(path):
        log.info("downloading %s ...", filename)
        response = ses.get(url)
        file = open(path, 'wb')
        file.write(response.content)
        file.close()
    log.info("uploading %s ...", filename)
    link = uploadPDF(path, filename)
    return {"path": link}
