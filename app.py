import tkinter as tk
from tkinter import *
from playsound import playsound
import os

#Initialization
temp_list=[]
item_set=[]
item_val=[]
files=[]
selected=[]
audio_files=[]
add_areas=[]
play_areas=[]
directories=[]
path= os.getcwd()
folder_count=0
file_count=0

#Data Adder
def add_data(args):
    if not selected:
        pass
    else:
        file3=open("transaction.txt","a")
        file3.write("\n")
        for i in range(len(selected)):
            file3.write(files[add_areas.index(selected[i])])
            if(not(i==len(selected)-1)):
                file3.write(",")
        file3.close
    

#Transaction Reader
def transaction_reader():
    file1= open("transaction.txt","r")
    transactions=file1.readlines()
    for i in range(len(transactions)):
        transactions[i]=transactions[i].replace("\n","")
        transactions[i]=transactions[i].split(",")
    return transactions
    file1.close()

#Counter
def counter(li,transaction):
    counter_li=0
    if(type(li)==str):
        temp=[]
        temp.append(li)
    else:
        temp=li
    for i in transaction:
        set1= set(temp)
        set2= set(i)
        if set1.issubset(set2):
            counter_li+=1
    return counter_li
#itemset Creator
def itemset_creator(copy_files,in_files):
    temp_files=[]
    return_files=[]
    for i in range(len(copy_files)):
        for j in in_files:
            if (j in copy_files[i]):
                continue
            if (type(copy_files[i])==str):
                temp_files.append(copy_files[i])
            else:
                for k in copy_files[i]:
                    temp_files.append(k)
            temp_files.append(j)
            return_files.append(temp_files)
            temp_files=[]
    return return_files

def check_files(copy_files,in_files):
    for i in in_files:
        flag=0
        for j in copy_files:
            if(i in j):
                flag=1
                break
        if(flag==0):
            in_files.remove(i)
    return in_files

#Recommendation System Calculator
def calculation():
    transactions=transaction_reader()
    copy_files=files.copy()
    in_files=copy_files.copy()
    min_support=int(len(transactions)*50/100)
    while(len(copy_files)>1):
        removal_files=[]
        for i in copy_files:
            counter_i=counter(i,transactions)
            if (counter_i<min_support):
                removal_files.append(i)
            else:
                item_set.append(i)
                item_val.append(counter_i)
        for j in removal_files:
            copy_files.remove(j)
        in_files=check_files(copy_files,in_files)
        copy_files=itemset_creator(copy_files,in_files)

#Application
directories=os.listdir(os.path.join(path,"Data"))

#Functions
def finder(x,y,play_area):
    for i in range(len(play_area)):
        if(play_area[i][0]<x and play_area[i][2]>x and play_area[i][1]<y and play_area[i][3]>y):
            return i
    else:
        return -1

def playing(event):
    clicked =finder(event.x,event.y,play_areas)
    if (clicked==-1):
        return 0
    playsound(os.path.join(path,"Data",audio_files[clicked]))

def adder(event):
    clicked= finder(event.x,event.y,selected)
    if (clicked==-1):
        clicked= finder(event.x,event.y,add_areas)
        if(clicked==-1):
            return 0
        canvas.create_rectangle(add_areas[clicked][0],add_areas[clicked][1],add_areas[clicked][2],add_areas[clicked][3],fill="#060",width=0,tags="addbutton")
        selected.append((add_areas[clicked][0],add_areas[clicked][1],add_areas[clicked][2],add_areas[clicked][3]))
    else:
        canvas.create_rectangle(selected[clicked][0],selected[clicked][1],selected[clicked][2],selected[clicked][3],fill="#ababff",width=0,tags="addbutton")
        selected.pop(clicked)
#GUI
for i in directories:
    data_files=os.listdir(os.path.join(path,"Data",i))
    for j in data_files:
        j=j.replace(".wav","")
        files.append(j)
calculation()
root= tk.Tk()
canvas=tk.Canvas(root,height=500,width=500)
canvas.create_text(250,50,text="Drum Recommendation System",font=("Papayrus",20))

for i in directories:
    folder_count+=1
    canvas.create_text(50,folder_count*120,text=i,font=("Papayrus",10))
    data_files=os.listdir(os.path.join(path,"Data",i))
    for j in data_files:
        audio_files.append(os.path.join(i,j))
        j=j.replace(".wav","")
        file_count+=1
        canvas.create_text(20+file_count*50,60+folder_count*120,text=j,font=("Papayrus",8))
        flag=1
        for x in item_set:
            if(j in x):
                flag=0
                break
        if(flag==1):
            canvas.create_rectangle(file_count*50, 10+folder_count*120, file_count*50+40, 50+folder_count*120,fill="#ccc",width=0,tags="playbutton")
        else:
            canvas.create_rectangle(file_count*50, 10+folder_count*120, file_count*50+40, 50+folder_count*120,fill="#000",width=0,tags="playbutton")
        play_areas.append((file_count*50, 10+folder_count*120, file_count*50+40, 50+folder_count*120))
        canvas.create_rectangle(file_count*50,70+folder_count*120,file_count*50+40,90+folder_count*120,fill="#ababff",width=0,tags="addbutton")
        add_areas.append((file_count*50,70+folder_count*120,file_count*50+40,90+folder_count*120))
    file_count=0
canvas.create_rectangle(200,475,300,500,fill="#00f",width=0,tags="addata")
canvas.tag_bind("addbutton","<Button-1>",adder)
canvas.tag_bind("playbutton","<Button-1>",playing)
canvas.tag_bind("addata","<Button-1>",add_data)
canvas.pack()

root.mainloop()