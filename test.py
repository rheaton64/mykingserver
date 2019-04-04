import datetime

omit = [datetime.date(2018, 9, 10), datetime.date(2018, 9, 19), datetime.date(2018, 10, 8) 
, datetime.date(2018, 11, 12), datetime.date(2018, 11, 21), datetime.date(2018, 11, 22), datetime.date(2018, 11, 23)
, datetime.date(2018, 12, 24), datetime.date(2018, 12, 25), datetime.date(2018, 12, 26), datetime.date(2018, 12, 27), datetime.date(2018, 12, 28)
, datetime.date(2018, 12, 31), datetime.date(2019, 1, 1), datetime.date(2019, 1, 2), datetime.date(2019, 1, 3), datetime.date(2019, 1, 4)
, datetime.date(2019, 1, 21), datetime.date(2019, 2, 14), datetime.date(2019, 2, 15), datetime.date(2019, 2, 18)
, datetime.date(2019, 3, 11), datetime.date(2019, 3, 12), datetime.date(2019, 3, 13), datetime.date(2019, 3, 14), datetime.date(2019, 3, 15)
, datetime.date(2019, 3, 18), datetime.date(2019, 3, 19), datetime.date(2019, 3, 20), datetime.date(2019, 3, 21), datetime.date(2019, 3, 22)
, datetime.date(2019, 4, 19), datetime.date(2019, 5, 27)]

startDate = datetime.date(2018, 9, 6)


now = datetime.date(2019, 4, 10)
deltaDays = now - startDate
days = deltaDays.days

print("Days: " + str(days))
weekends = days/7.0
print("Weekends: " + str(weekends))

weekends = round(weekends)

print("New Weekends: " + str(weekends))



days -= 2*weekends

count = 0

for d in omit:
    if (now-d).days >= 0:
        count += 1
        days -= 1

days = round(days)

days += 1

print("Omitted: " + str(count))

print("New Days: " + str(days))



letterNum = days % 8
letter = int(letterNum)
letterDay = ""
if(letter == 0):
    letterDay = "A"
if(letter == 1):
    letterDay = "B"
if(letter == 2):
    letterDay = "C"
if(letter == 3):
    letterDay = "D"
if(letter == 4):
    letterDay = "E"
if(letter == 5):
    letterDay = "F"
if(letter == 6):
    letterDay = "G"
if(letter == 7):
    letterDay = "H"

print("Letter: " + str(letter))
print(letterDay)