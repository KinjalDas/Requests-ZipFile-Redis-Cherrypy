from datetime import date, timedelta
import requests, zipfile, io, redis, csv

today = date.today()
redisClient = redis.StrictRedis(host='localhost',port=6379,db=0)
while True:
    date_now = today.strftime("%d%m%y")
    url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"+ date_now +"_CSV.ZIP"
    r = requests.get(url)
    print(url , r.ok)
    if r.ok:
        filename = "EQ" + date_now + ".CSV"
        print(filename)
        break
    else:
        today = today - timedelta(days=1)
        continue

z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
reader = csv.DictReader(open(filename))
records = 0
for raw in reader:
	print("Writing at index : " + str(records) + " : " + str(raw))
	redisClient.hset(records, "code" , raw["SC_CODE"])
	redisClient.hset(records, "name" , raw["SC_NAME"])
	redisClient.hset(records, "open" , raw["OPEN"])
	redisClient.hset(records, "high" , raw["HIGH"])
	redisClient.hset(records, "low" , raw["LOW"])
	redisClient.hset(records, "close" , raw["CLOSE"])
	records = records + 1
    #print (raw)
print ("records : " + str(records))
redisClient.set("records",records)
# for i in range(records):
# 	print(redisClient.hgetall(i))
