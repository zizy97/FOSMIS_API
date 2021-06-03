import pathlib
import os
from gdrive.uploadPDF import uploadPDF

dirName = 'pdf'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory ", dirName, " Created ")
except FileExistsError:
    print("Directory ", dirName, " already exists")


def download_file(ses,url,filename):
    if not os.path.exists('pdf/' + filename + '.pdf'):
        response = ses.get(url)
        file = open('pdf/' + filename + ".pdf", 'wb')
        file.write(response.content)
        file.close()
    path = str(pathlib.Path().absolute()) + f'\\img\\{filename}.pdf'
    file_path = '/'.join(path.split("\\"))
    link = uploadPDF(file_path, filename)
    return {"path":link}
