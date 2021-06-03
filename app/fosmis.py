import re

from bs4 import BeautifulSoup
from requests import Session

from . import download_file, get_html_content, NewsData, db, logging

# USERNAME = os.environ.get("USERNAME")
# PASSWORD = os.environ.get("PASSWORD")
USERNAME = 'sc10676'
PASSWORD = 'Level1@2019'

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
        for row in gdp_table:
            row_data = []
            for row.td in row:
                if row.td.a:
                    if re.search(r".pdf", row.td.a['href']):
                        filename = re.findall(r'-[\w,\s]*', row.td.a['href'])[0]
                        filename = filename.strip('- ')
                        url2 = re.findall(r'/.*', row.td.a['href'])[0]
                        row_data.append({"path": download_file(ses, url + "/" + url2, filename)})
                        break
                    elif re.search(r".html", row.td.a['href']):
                        row_data.append(
                            {"description": get_html_content(ses, url + 'forms/' + row.td.a['href'])})
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
                    if "path" == x:
                        log.info(row[3][x])
                        newsdata = NewsData(row[0], row[1], row[2], "", row[3][x])
                        finaldata.update({key: newsdata})
                    else:
                        newsdata = NewsData(row[0], row[1], row[2], row[3]["description"], "")
                        finaldata.update({key: newsdata})
                    db.session.add(newsdata)
                    db.session.commit()

        log.info("fetched all data !")
        return finaldata
