import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session

# from . import download_file, get_html_content, logging
from . import logging, get_html_content
from .db import database

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


url = "https://paravi.ruh.ac.lk/fosmis2020/"

log = logging.getLogger(__name__)


def updateDB():
    log.info("fetching data from fosmis ...")
    with Session() as ses:
        ses.post("https://paravi.ruh.ac.lk/fosmis2020/login.php", data=dict(uname=USERNAME, upwd=PASSWORD))
        res = ses.get(url + "forms/form_53_a.php")
        soup = BeautifulSoup(res.content, "lxml")
        gdp_table = soup.findAll("tr", attrs={"class": "trbgc"})
        news = []
        # count = 0
        for row in gdp_table:
            row_data = []
            for row.td in row:
                if row.td.a:
                    if re.search(r".pdf", row.td.a['href']) or re.search(r".docx", row.td.a['href']) :
                        filename = re.findall(r'-[\w,\s]*', row.td.a['href'])[0]
                        filename = filename.split('-')
                        filename = ' '.join(filename)
                        url2 = re.findall(r'/.*', row.td.a['href'])[0]
                        # row_data.append(download_file(ses, url + "/" + url2, filename))
                        link = url + row.td.a['href'].split('/', 1)[1]
                        row_data.append({"path": link})
                    elif re.search(r".html", row.td.a['href']):
                        row_data.append(
                            {"description": get_html_content(ses, url + 'forms/' + row.td.a['href'])})
                row_data.append(row.td.text)
            news.append(row_data)
            # count += 1
            # if count == 3:
            #     break

        log.info("updating db ...")
        key = 0

        # get current database newsdata
        data = database.child('Newsdata').get().val()

        # log.info(data)
        # append the updates to the Database
        # finaldata = {}
        for row in news:
            if len(row) > 3:
                key += 1
                newsdata = None
                edit = re.findall('\w*', row[1])
                while "" in edit:
                    edit.remove("")
                date = datetime(year=int(edit[0]), month=int(edit[1]), day=int(edit[2]), hour=int(edit[3]),
                                minute=int(edit[4]))
                today = datetime.today()
                time_gone = (today - date).days

                if time_gone > 5:
                    recent = False
                else:
                    recent = True
                for x in row[3]:
                    if "path" == x:
                        newsdata = {"id": key, "date": str(date), "title": row[2], "description": "",
                                    "source": ["view_link",row[3]['path']],
                                    "recent": recent}
                    else:
                        newsdata = {"id": key, "date": str(date), "title": row[2], "description": row[3]["description"],
                                    "source": ["", ""],
                                    "recent": recent}
                log.info(f"{newsdata['title']} inserting to db")
                flag = -1
                if data:
                    for news in data:
                        if news is not None:
                            if newsdata['title'] == news['title']:
                                if newsdata['date'] == news['date']:
                                    if newsdata['recent'] == news['recent']:
                                        flag = -2
                                        break
                                    flag = news['id']
                                    break
                if flag == -1:
                    if data:
                        newsdata['id'] = len(data)
                        database.child("Newsdata").child(newsdata['id']).set(newsdata)
                        log.info(f"{newsdata['title']} inserted")
                        data.append(newsdata)
                    else:
                        database.child("Newsdata").child(newsdata['id']).set(newsdata)
                        log.info(f"{newsdata['title']} inserted")
                elif flag == -2:
                    log.info(f"{newsdata['title']} exist abort insert")
                else:
                    database.child('Newsdata').child(flag).update({"recent": False})
                    log.info(f"{newsdata['title']} Updated")

        log.info("fetched all data !")
