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


async def download_file(index, arr):
    if not os.path.exists('pdf/' + arr[2] + '.pdf'):
        response = arr[0].get(arr[1])
        file = open('pdf/' + arr[2] + ".pdf", 'wb')
        file.write(response.content)
        file.close()
    path = str(pathlib.Path().absolute()) + f'\\img\\{arr[2]}.pdf'
    file_path = '/'.join(path.split("\\"))
    link = uploadPDF(file_path, arr[2])
    return [index, link]
