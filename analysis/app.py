from flask import Flask,render_template,request
import datetime
import sqlite3


app = Flask(__name__)

@app.route("/")
def toindex():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/movie")
def movie():
    datalist=[]
    con = sqlite3.connect("movie250.db")
    c=con.cursor()
    sql='''
        select * from movie250
    '''
    data = c.execute(sql)
    #不能直接断开数据库，data因为游标的关闭而缺失数据，先保存
    for i in data:
        datalist.append(i)
    con.commit()
    con.close()
    return render_template("movie.html", list=datalist)

@app.route("/analysis")
def score():
    num=[]
    score=[]
    cname=[]
    comment=[]
    rank=[]
    rate=[]
    combine=[]
    con = sqlite3.connect("movie250.db")
    c1 = con.cursor()
    c2 = con.cursor()
    c3 = con.cursor()
    sql1 = '''
        select rating,count(rating) from movie250 group by rating
    '''
    data1 = c1.execute(sql1)
    sql2 = '''
        select cname,comment from movie250 where id between 1 and 10 group by cname
    '''
    data2 = c2.execute(sql2)
    sql3 = '''
            select rating,id from movie250
        '''
    data3 = c3.execute(sql3)

    for i in data1:
        score.append(i[0])
        num.append(i[1])
    for j in data2:
        cname.append(j[0])
        comment.append(j[1])
    for k in data3:
        rate.append(k[0])
        rank.append(k[1])

    for a in range(250):
        combine.append([rank[a],rate[a]])
    print(combine)

    con.commit()
    con.close()
    return render_template("analysis.html", score=score, num=num, cname=cname, comment=comment, combine=combine)

@app.route("/wordcloud")
def word():
    return render_template("wordcloud.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)


