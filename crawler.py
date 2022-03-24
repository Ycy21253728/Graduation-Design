from bs4 import BeautifulSoup
import sqlite3
import xlwt
import urllib.request,urllib.error
import re


def main():
    baseurl="https://movie.douban.com/top250?start="
    #爬取网页
    datalist=getData(baseurl)
    #解析数据
    #保存数据
    dbpath="movie250.db"
    saveData(datalist, dbpath)


#爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,10):    
        url=baseurl + str(i*25)
        html=askURL(url)
        
        findlink=re.compile(r'<a href="(.*?)">')
        findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)
        findTitle=re.compile(r'<span class="title">(.*)</span>')
        findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
        findComment=re.compile(r'<span>(\d*)人评价</span>')
        findInq=re.compile(r'<span class="inq">(.*)</span>')
        findBd=re.compile(r'<p class="">(.*?)</p>',re.S)

        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data=[] #保存每一部电影的所有信息
            item=str(item)
            # print(item)
            # break
            title=re.findall(findTitle, item)
            
            if(len(title)==2):
                ctitle=title[0]
                data.append(ctitle)
                otitle=title[1].replace("/","")
                otitle=re.sub('\s', " ", otitle)
                data.append(otitle)
            else:
                data.append(title[0])
                data.append('') 
            
            link=re.findall(findlink, item)[0]
            data.append(link)
            imgsrc=re.findall(findImgSrc, item)[0]
            data.append(imgsrc)
            inq=re.findall(findInq, item)
            data.append(inq[0] if(len(inq)) else "")
            rating=re.findall(findRating, item)[0]
            data.append(rating)
            comment=re.findall(findComment, item)[0]
            data.append(comment)
            bd=re.findall(findBd, item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd=re.sub('/', " ", bd)
            bd=re.sub('\s', "", bd)
            data.append(bd.strip())
            datalist.append(data)
    return datalist

def askURL(url):
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71"
    }
    data = bytes(urllib.parse.urlencode({'name':'eric'}),encoding='utf-8')
    req = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(req)
    return response

def saveData(datalist,dbpath):
    # initDb(dbpath)
    conn=sqlite3.connect(dbpath)
    c=conn.cursor()
    n=1
    for data in datalist:
        for i in range(len(data)):
            data[i] = '"'+data[i]+'"'
        sql='''insert into movie250
                values(%d,%s)
        '''%(n,",".join(data))
        c.execute(sql)
        conn.commit()
        print("爬取成功")
        
    c.close()
    conn.close()

def initDb(dbpath):
    sql='''create table movie250(
        id integer primary key autoincrement,
        cname varchar,
        oname varchar,
        info_link text,
        img_link text,
        inq text,
        rating numeric,
        comment numeric,
        info text
    )'''
    conn=sqlite3.connect(dbpath)
    c=conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

if __name__=="__main__":
    
    url1="http://httpbin.org/post"
    initDb("movie250.db")
    main()

