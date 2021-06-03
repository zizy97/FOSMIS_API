import re
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session

from . import download_file, get_html_content, NewsData, db, logging, Source

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
                        filename = filename.split('-')
                        filename = ' '.join(filename)
                        url2 = re.findall(r'/.*', row.td.a['href'])[0]
                        row_data.append(download_file(ses, url + "/" + url2, filename))
                    elif re.search(r".html", row.td.a['href']):
                        row_data.append(
                            {"description": get_html_content(ses, url + 'forms/' + row.td.a['href'])})
                row_data.append(row.td.text)
            news.append(row_data)

        log.info("updating db ...")
        key = 0

        # get current database newsdata
        data = NewsData.query.all()

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

                if time_gone > 2:
                    recent = False
                else:
                    recent = True
                for x in row[3]:
                    if "path" == x:
                        newsdata = NewsData(key, date, row[2], "", Source(row[3][x]['view'], row[3][x]['download']),
                                            recent)
                    else:
                        newsdata = NewsData(key, date, row[2], row[3]["description"], None, recent)

                    # finaldata.update({key: newsdata})
                    log.info(f"{newsdata.title} inserting to db")
                    flag = 0
                    for news in data:
                        if newsdata.title == news.title:
                            if newsdata.date == news.date:
                                flag = 1
                                break
                    if flag == 0:
                        newsdata.id = len(data) + 1
                        data.append(newsdata)
                        db.session.add(newsdata)
                        db.session.commit()
                        log.info(f"{newsdata.title} inserted")
                    else:
                        log.info(f"{newsdata.title} exist abort insert")

        log.info("fetched all data !")
