import re,requests,pymysql,time
from bs4 import BeautifulSoup

headers={"Host":"www.itellyou.cn","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0","Referer":"http://www.itellyou.cn/"}

s=requests.session()

def itellyou_post(url,data):
    try:
        r=s.post(url,data=data,headers=headers,timeout=10)
        print(url,data,"\n",r.text)
    except:
        time.sleep(5)
        print("访问异常",url,data)
        itellyou_post(url, data)
    else:
        if r.status_code !=200:
            time.sleep(5)
            itellyou_post(url, data)
        else:
            time.sleep(1)
            #爬虫访问间隔e
            return r



re_lang=r'{"status":true,"result":(.*)}'
conn=pymysql.connect(host='localhost', port=3306, user='root', password="q117971371", db='smzdm', charset='utf8')
cur = conn.cursor()
增_sql ="""INSERT INTO itellyou (menu,name,country,version,FileName,SHA1,dt,PostDataString,DownLoad) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');"""
#定义数据库链接



r=s.get("http://www.itellyou.cn",headers=headers,timeout=10)
r=BeautifulSoup(r.text)
h4=r.find_all("h4")

#获取全站目录
time.sleep(1)

for a in h4:
    data = {"id":a.a["data-menuid"]}
    url="http://msdn.itellyou.cn/Category/Index"
    r=itellyou_post(url,data)
    #获取软件目录
    r = eval(r.text)

    for i in r:
        data={"id":i["id"]}
        url="http://msdn.itellyou.cn/Category/GetLang"
        r1=itellyou_post(url,data)
        if r1.text=='{"status":true,"result":[]}':
            x["lang"], y["name"], z["FileName"], z["SHA1"], z["size"], z["PostDateString"], z[
                "DownLoad"] = "", "", "", "", "", "", ""
            cur.execute(增_sql % (
                a.a.text, i["name"], x["lang"], y["name"], z["FileName"], z["SHA1"], z["size"], z["PostDateString"],
                z["DownLoad"]))
            conn.commit()
            continue
        else:
            lang=eval(re.findall(re_lang,r1.text)[0])

        #获取软件语言列表

        for x in lang:
            data = {"id": i["id"], "lang": x["id"], "filter": "true"}
            url="http://msdn.itellyou.cn/Category/GetList"
            r2 = itellyou_post(url, data)
            #获取文件列表


            if r2.text == '{"status":true,"result":[]}':
                x["lang"], y["name"], z["FileName"], z["SHA1"], z["size"], z["PostDateString"], z[
                    "DownLoad"] = "", "", "", "", "", "", ""
                cur.execute(增_sql % (a.a.text, i["name"], x["lang"], y["name"], z["FileName"], z["SHA1"], z["size"], z["PostDateString"],z["DownLoad"]))
                conn.commit()
                continue
            else:
                data2 = eval(re.findall(re_lang, r2.text)[0])


            for y in data2:
                data={"id":y["id"]}
                url="http://msdn.itellyou.cn/Category/GetProduct"
                r3=itellyou_post(url, data)
                #获取文件详细信息.
                try:
                    z=eval(re.findall(re_lang, r3.text)[0])
                except:
                    x["lang"],y["name"],z["FileName"],z["SHA1"],z["size"],z["PostDateString"],z["DownLoad"]="","","","","","",""
                else:
                    cur.execute(增_sql%(a.a.text,i["name"],x["lang"],y["name"],z["FileName"],z["SHA1"],z["size"],z["PostDateString"],z["DownLoad"]))
                    conn.commit()