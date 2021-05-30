#import logging
import re
import os
from bs4 import BeautifulSoup
from requests import Session

#from .downloadfile import download_file
from .getcontent import get_html_content
from .config import NewsData, db

#format = "%(asctime)s: %(message)s"
#logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

url = "https://paravi.ruh.ac.lk/fosmis2020/"


def updateDB():
    with Session() as ses:
        ses.post("https://paravi.ruh.ac.lk/fosmis2020/login.php", data=dict(uname=USERNAME, upwd=PASSWORD))
        res = ses.get(url + "forms/form_53_a.php")
        soup = BeautifulSoup(res.content, "lxml")
        gdp_table = soup.findAll("tr", attrs={"class": "trbgc"})
        news = []
        for row in gdp_table:
            row_data = []
            for row.td in row:
                if row.td.a:
                    if re.search(r".pdf", row.td.a['href']):
                        #logging.info("File Stated Downloading")
                        filename = re.findall(r'-[\w,\s]*', row.td.a['href'])
                        url2 = re.findall(r'/.*', row.td.a['href'])
                        #row_data.append({"path": download_file(ses, url + url2[0], filename[0])})
                        row_data.append({"path": "file-path-url"})

                        break
                    elif re.search(r".html", row.td.a['href']):
                        row_data.append(
                            {"descritption": get_html_content(ses, url + 'forms/' + row.td.a['href'])})
                    continue
                row_data.append(row.td.text)
            news.append(row_data)
        finaldata = {}
        key = 0
        for row in news:
            if len(row) > 3:
                key += 1
                newsdata = None
                for x in row[3]:
                    if "path" in row[3]:
                        newsdata = NewsData(row[0], row[1], row[2], "", row[3]["path"])
                        finaldata.update({key: newsdata})
                    else:
                        newsdata = NewsData(row[0], row[1], row[2], row[3]["descritption"], "")
                        finaldata.update({key: newsdata})
                    db.session.add(newsdata)
                    db.session.commit()
        return finaldata

