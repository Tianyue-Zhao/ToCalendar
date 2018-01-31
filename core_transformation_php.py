def find_keywords(table):
    date=-1
    week=-1
    assignment=-1
    description=-1
    day1=-1
    day2=-1
    day3=-1
    flag1=0
    flag2=0
    flag3=0
    flag4=0
    flag5=0
    flag6=0
    flag7=0
    #flag8=0 #for absolute date, or adate
    row=table.rows[0]
    i=0
    for cell in row.cells:
        result=re.search(r"da[y|te]",cell.text,re.I)
        if(result!=None):
            if(flag1==0):
                date=i
                flag1=1
            #else:
                #print("multiple matches for date!")
        result = re.search("week", cell.text, re.I)
        if (result != None):
            if (flag2 == 0):
                week=i
                flag2=1
            #else:
                #print("multiple matches for week!")
        result = re.search("assignment", cell.text, re.I)
        if (result != None):
            if (flag3 == 0):
                assignment = i
                flag3 = 1
            #else:
                #print("multiple matches for assignment!")
        result=re.search("homework",cell.text,re.I)
        if(result!=None):
            if(flag3==0):
                assignment=i
                flag3=1
        result = re.search("description", cell.text, re.I)
        if (result != None):
            if (flag4 == 0):
                description = i
                flag4 = 1
            #else:
                #print("multiple matches for description!")
        result = re.search("day 1",cell.text,re.I)
        if(result!=None):
            flag5=1
            day1=i
        result=re.search("day 2",cell.text,re.I)
        if(result!=None):
            flag6=1
            day2=i
        result=re.search("day 3",cell.text,re.I)
        if(result!=None):
            flag7=1
            day3=i
        #result=re.sesarch("absolute date",cell.text,re.I)
        #if(result!=None):
        #    flag8=1
        #    adate=i
        i+=1
    return date,week,assignment,description,day1,day2,day3


from docx import Document
import re
from icalendar import Calendar,Event
import datetime
import sys

#definition of variables
#constants:
schedule=[]
tmp=[0,1,3]
schedule.append(tmp)
tmp=[0,2,3]
schedule.append(tmp)
tmp=[0,2,4]
schedule.append(tmp)
tmp=[1,2,4]
schedule.append(tmp)
tmp=[1,3,4]
schedule.append(tmp)
tmp=[0,2,4]
schedule.append(tmp)
tmp=[1,3,4]
schedule.append(tmp)
#header marks:
potential_headers=4
keywordlocs=[]
keywords=[]
date=-1    #these four rows are the column numbers of the respective fields.
#adate=-1
week=-1
assignment=-1
description=-1
day1=-1
day2=-1
day3=-1
#for going through rows:
curmonth=0
curstart=0
curday=0
curyear=0
year=2017
period=''
name=""    #name of assignment
details=""    #detailed description of assignment
finalm=[]
finals=[]
finald=[]
finaly=[]
finalname=[]
finaldescription=[]

#open document
#filename="AP_stats.docx"
filename=sys.argv[1]
period=sys.argv[2]
course=sys.argv[3]
directory="../../toicalendar/Files/"
#note the directory is from the perspective of the location of upload.php
document=Document(directory+filename)
table=document.tables[0]
debug=open("debug.txt",'w')

#determine the meanings of the headers
[date,week,assignment,description,day1,day2,day3]=find_keywords(table)
if(date!=-1):
    if(week!=-1):
        keywordlocs.append(date)
        keywordlocs.append(week)
        keywords.append("date")
        keywords.append("week")
    else:
        keywordlocs.append(date)
        keywords.append("mixeddate")
#elif(adate!=-1):
#    keywordlocs.append(adate)
#    keywords.append("adate")
else:
    debug.write("no_date!")
    print(9/0)
if(assignment!=-1):
    if(description!=-1):
        keywords.append("description")
        keywords.append("assignment")
        keywordlocs.append(description)
        keywordlocs.append(assignment)
    else:
        keywords.append("mixeddescription")
        keywordlocs.append(assignment)
elif(description!=-1):
    keywords.append("mixeddescription")
    keywordlocs.append(description)
elif(day1!=-1 and day2!=-1 and day3!=-1):
    keywords.append("day1")
    keywords.append("day2")
    keywords.append("day3")
    keywordlocs.append(day1)
    keywordlocs.append(day2)
    keywordlocs.append(day3)
else:
    debug.write("no_description")
    print(9/0)
period=period.upper()

#go through the rows, and construct the calendar
rows=table.rows
for i in range(1,len(rows)):
    curday=-1
    cells=rows[i].cells
    for k in range(0,len(keywordlocs)):
        if(keywords[k]=="mixeddate"):
            #result=re.search(r"[01]?[0-9]/[0|1|2|3]?[0-9]/[0-9]*",cells[keywordlocs[k]].text,flags=0) #enabled, previously not enabled
            #result=None  #add recording to see which teachers use the full notation?
            #if(result!=None):
            #    tmp=result.group()
            #    tmp=tmp.split('/')
            #    curmonth=int(tmp[0])
            #    curstart=int(tmp[1])
            #    curday=int(tmp[2])
            #else:
            result=re.search(r"[01]?[0-9]/[0|1|2|3]?[0-9]",cells[keywordlocs[k]].text,flags=0) #search in form of "mm/dd"
            if(result!=None):
                tmp=result.group()
                tmp=tmp.split('/')
                curmonth=int(tmp[0])
                curstart=int(tmp[1])
            result=re.search(r"day [1|2|3]",cells[keywordlocs[k]].text,re.I)
            if(result!=None):
                tmp=result.group()
                tmp=tmp.split()
                curday=int(tmp[1])
                #print(curmonth,curstart,curday)
            else:
                result=re.search(r"[1|2|3]",cells[keywordlocs[k]].text,flags=0)
                if(result!=None):
                    tmp=result.group()
                    curday=int(tmp)
        if(keywords[k]=="week"):
            result=re.search(r"[01]?[0-9]/[0|1|2|3]?[0-9]",cells[keywordlocs[k]].text,flags=0)
            if(result!=None):
                tmp = result.group()
                tmp = tmp.split('/')
                curmonth = int(tmp[0])
                curstart = int(tmp[1])
        if(keywords[k]=="date"):
            result=re.search(r"[1|2|3]",cells[keywordlocs[k]].text,flags=0)
            if (result != None):
                tmp = result.group()
                curday=int(tmp)
                #print(curmonth, curstart, curday)
            else:
                continue
        if(keywords[k]=="description"):
            details=cells[keywordlocs[k]].text
        if(keywords[k]=="assignment"):
            name=cells[keywordlocs[k]].text
        if(keywords[k]=="mixeddescription"):
            name = cells[keywordlocs[k]].text
            details="No"
        if(keywords[k]=="day1"):
            name=cells[keywordlocs[k]].text
            details="No"
        if(keywords[k]=="day2"):
            name=cells[keywordlocs[k]].text
            details="No"
        if(keywords[k]=="day3"):
            name=cells[keywordlocs[k]].text
            details="No"
    if(1<=curmonth<=12 and 1<=curstart<=31):
        if(curmonth<8):
            curyear=year+1
        else:
            curyear=year
        finalm.append(curmonth)
        finals.append(curstart)
        finald.append(curday)
        finaly.append(curyear)
        finalname.append(name)
        finaldescription.append(details)
#creating the calendar itself
filename=filename.split('.')[0]
for i in range(0,len(period)):
    cal=Calendar()
    curperiod=ord(period[i])-65
    for k in range(0,len(finalm)):
        if(not finaldescription[k]==''):
            if(not finald[k]==3): #this helps display the due date, not the date assigned
                event=Event() #the date in the following 2 lines are deliberatly postponed by 1 class day to display the due date
                event.add("dtstart",datetime.date(finaly[k],finalm[k],finals[k])+datetime.timedelta(days=schedule[curperiod][finald[k]]))
                event.add("dtend",datetime.date(finaly[k],finalm[k],finals[k])+datetime.timedelta(days=schedule[curperiod][finald[k]]))
                event.add("summary",course+':'+finalname[k])
            else: #if the assignment is assigned on class day 3, the due date will be class day 1 of the next week
                event=Event()
                event.add("dtstart",datetime.date(finaly[k],finalm[k],finals[k])+datetime.timedelta(days=schedule[curperiod][0]+7))
                event.add("dtend",datetime.date(finaly[k],finalm[k],finals[k])+datetime.timedelta(days=schedule[curperiod][0]+7))
                event.add("summary",course+':'+finalname[k])
            if(finaldescription[k]!="No"):
                event.add("description",finaldescription[k])
            cal.add_component(event)
    outfile=open(directory+period[i]+"_period_"+course+".ics",'w')
    outfile.write(cal.to_ical())
    outfile.close()
debug.close()
