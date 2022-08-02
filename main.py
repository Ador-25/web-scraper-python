import os
from html import parser
from urllib.parse import urljoin

import pyodbc
import urllib
from urllib.request import urlopen

import requests, PyPDF2
from io import BytesIO
from bs4 import BeautifulSoup


list=[]

def GetPdfContent(url):
    try:
        response = requests.get(url)
        my_raw_data = response.content
        str = ""
        with BytesIO(my_raw_data) as data:
            read_pdf = PyPDF2.PdfFileReader(data)

            for page in range(read_pdf.getNumPages()):
                str = str + read_pdf.getPage(page).extractText()
            return str
    except:
        return ""


def GetTxtContent(url):
    try:
        str = ""
        file = urllib.request.urlopen(url)
        for line in file:
            decoded_line = line.decode("utf-8")
            str = str + decoded_line
        return str;
    except:
        return ""



def GetNonHtml(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def GetDocx(url):
    doctxt = ""
    folder_location = r'./docx/'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select("a[href$='.doc']"):
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url, link['href'])).content)
            raw = parser.from_file(filename)
            pt = str(raw['content'])
            doctxt += pt
            #print(doctxt)
        return doctxt
    except:
        print("EXCEPTION")
        return "NONE"

list=[]
def read(conn):
    cursor=conn.cursor()
    cursor.execute("select urlstring from [AuthDb].[dbo].[ExtendedCluster] where ClusterId = '02c1d3b9-b98f-4a58-eca3-08d9ca8fba6c'" )
    for row in cursor:
        list.append(row.urlstring)

def write(conn,link,data):
    if(len(data)>0):
        try:
            temp = "insert into [AuthDb].[dbo].[ClusterData] (urlid,data) values('"
            sql = temp + link + "'," + "'" + data + "')"
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print("Inserted for: " + link)

        except:
            print("ERROR for: " + link)
    else:
        print("error: "+link)



conn = pyodbc.connect(
    "Driver={Sql Server Native Client 11.0};"
    "Server=.;"
    "Database=AuthDb;"
    "Trusted_Connection=yes;"
)



read(conn)
for elem in list:
    try:
        if (elem[-4:] == ".pdf"):
            data = GetPdfContent(elem)
            write(conn, elem, data.replace("'"," "))
        if (elem[-4:] == ".txt"):
            data = GetTxtContent(elem)
            write(conn, elem, data.replace("'"," "))
        if (elem[-4:] == "docx" or elem[-4:] == ".doc"):
            data = GetDocx(elem)
            write(conn, elem, data.replace("'"," "))
        else:
            data = GetNonHtml(elem)
            write(conn, elem, data.replace("'"," "))
    except:
        print("error")






