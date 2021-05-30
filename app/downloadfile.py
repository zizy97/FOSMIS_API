import pathlib
import os

dirName = 'pdf'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory ", dirName, " Created ")
except FileExistsError:
    print("Directory ", dirName, " already exists")


def download_file(ses, download_url, filename):
    if not os.path.exists('pdf/' + filename + '.pdf'):
        response = ses.get(download_url)
        file = open('pdf/' + filename + ".pdf", 'wb')
        file.write(response.content)
        file.close()
    path = str(pathlib.Path().absolute()) + f'\\img\\{filename}.pdf'
    return '/'.join(path.split("\\"))
