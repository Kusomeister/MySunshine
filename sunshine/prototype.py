import os, json, requests
import plotly.express as px
from tkinter import *
from tkcalendar import Calendar
root = Tk()
root.title("You are my sunshine")
root.geometry("800x550")

bg = PhotoImage(file = "gradient.png")
canvas1 = Canvas( root, width = 800,height = 550)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, image = bg, anchor = "nw")

poczatek=""
koniec=""
root.wm_iconbitmap('ikona.ico')

longitude = 49.690289
latitude = 21.754990
okresy = "daily"
data = ""
def grad_date1():
    result = cal1.get_date()
    result = result.split(sep="/")
    global poczatek
    poczatek=""
    for x in result:
        if len(x)<2:
            poczatek+= "0"+x
        else:
            poczatek+=x
            
            

def grad_date2():
    result = cal2.get_date()
    result = result.split(sep="/")
    global koniec
    koniec=""
    for x in result:
        if len(x)<2:
            koniec+= "0"+x
        else:
            koniec+=x

def dateConv(date):
    result=[]
    for x in date:
        result.append(x)
    date = result
    result = ""
    flag = 1
    for x in range(4):
        result += date.pop(0)
    
    while len(date)> 0:
        result += "/"
        result += date.pop(0)
        result += date.pop(0)
    return result
            
        
        
    
def wykres():
    grad_date1()
    grad_date2()
    output = r""
    base_url = r"https://power.larc.nasa.gov/api/temporal/{okresy}/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={longitude}&latitude={latitude}&start={poczatek}&end={koniec}&format=JSON"
    if okresy == "monthly":
        global poczatek
        global koniec
        resp=""
        resk=""
        for x in range(4):
            resp += poczatek[x]
            resk += koniec[x]
        poczatek = resp
        koniec = resk
    api_request_url = base_url.format(longitude=longitude, latitude=latitude,poczatek=poczatek, koniec=koniec, okresy=okresy)

    response = requests.get(url=api_request_url, verify=True, timeout=30.00)
    print(response)
    print(api_request_url)
    content = json.loads(response.content.decode('utf-8'))
    data=content
    data = data["properties"]["parameter"]['ALLSKY_SFC_SW_DWN']
    dzien = []
    moc = []

    for a, b in data.items():
        a = dateConv(a)
        dzien.append(a)
        moc.append(b)
    data = (dzien, moc)
    fig=px.bar(data,y=moc, x=dzien)
    fig.update_layout(yaxis_title= content["parameters"]["ALLSKY_SFC_SW_DWN"]["units"], xaxis_title="Date")
    fig.show()

    
cal1 = Calendar(root, selectmode = 'day',
               year = 2020, month = 10,
               day = 5, date_pattern="y/m/d")
cal2 = Calendar(root, selectmode = 'day',
               year = 2020, month = 10,
               day = 15, date_pattern="y/m/d")
 
cal1.place(x = 100, y = 50)
cal2.place(x= 440, y = 50)


def hourly():
    global okresy
    okresy = "hourly"
def daily():
    global okresy
    okresy = "daily"
def monthly():
    global okresy
    okresy = "monthly"
    
color3 = "#757DAA"

Button(root, text = "Hourly", command = hourly, width = 25, height = 5, bg = color3).place(x= 100, y = 300)
Button(root, text = "Daily", command = daily, width = 25, height = 5, bg = color3).place(x= 300, y = 300)
Button(root, text = "Monthly", command = monthly, width = 25, height = 5, bg = color3).place(x= 506, y = 300)

 

 
grabButton = Button(root, text = "Run", command = wykres, width = 83, height = 5, bg = "#5C79EC").place(x = 100, y = 400)

date = Label(root, text = "")
date.pack(pady = 20)
root = mainloop()
