# period tracker-------------------------------
import datetime  
delay1=25
delay2=30
prevdate="20/10/2020"
prevd=datetime.datetime.strptime(prevdate,"%d/%m/%Y").date() 

def numOfDays(a,b):
    return (b-a).days

def nexperiod(date1):
    periodate1=datetime.datetime.strptime(date1,"%d/%m/%Y").date() 
    newdate1 = periodate1 + datetime.timedelta(days=delay1)
    newdate2= periodate1 + datetime.timedelta(days=delay2)
    prevd=periodate1
    return (newdate1,newdate2)

date1=input("What was your last period date? (in DD/MM/YYYY) ") 
d1,d2=nexperiod(date1) 
print("your period will come between")
print(d1)
print(d2)

def newdelay(date2):
    periodate2=datetime.datetime.strptime(date2,"%d/%m/%Y").date()
    datenow1 = prevd
    datenow2 = periodate2
    delay1=numOfDays(datenow1, datenow2)
    delay2=delay1+5 
    return nexperiod(date2)

date2=input("Have you already got your period? (in DD/MM/YYYY) ")  
d3,d4=newdelay(date2)
print("your next period will come between")
print(d3)
print(d4)
