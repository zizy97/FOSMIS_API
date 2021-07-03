# from bs4 import BeautifulSoup


# def get_html_content(ses, url):
#     res = ses.get(url)
#     content_ = res.content
#     soup = BeautifulSoup(content_, "lxml")
#     data = soup.findAll("div", attrs={"id": "m"})
#     description = []
#     for des in data:
#         if des.text:
#             description.append(des.text)
#     return "\n".join(description)
