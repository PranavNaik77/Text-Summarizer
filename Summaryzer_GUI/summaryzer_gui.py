# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
import wx;

# NLP Pkgs
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization  import nltk_summarizer
from sumy_summarization import sumy_summarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pranav0707",
  database="ratings"
)

mycursor=mydb.cursor()



 # Structure and Layout
window = Tk()
window.title("Summaryzer GUI")
window.geometry("1000x600")
window.config(background='black')
window.option_add('*Font', 'Times 11')




style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn',)



# TAB LAYOUT
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')



tab1= ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)



# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^20s}')
tab_control.add(tab3, text=f'{"URL":^20s}')
tab_control.add(tab4, text=f'{"Comparer ":^20s}')
tab_control.add(tab5, text=f'{"About ":^20s}')



label1 = Label(tab1, text= 'Summaryzer',padx=5, pady=5)
label1.grid(column=0, row=0)
 
label2 = Label(tab2, text= 'File Processing',padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text= 'URL',padx=5, pady=5)
label3.grid(column=0, row=0)

label3 = Label(tab4, text= 'Compare Summarizers',padx=5, pady=5)
label3.grid(column=0, row=0)

label4 = Label(tab5, text= 'About',padx=5, pady=5,font=18)
label4.grid(column=0, row=0)

label4 = Label(tab5, text='\n\nPrivacy Policy',padx=5, pady=5,font=18)
label4.grid(row=9,column=0)

privacy_text="Respect for your privacy is coded into our DNA. Since we started Summarizer GUI, we’ve built our Services with a set of strong privacy principles in mind. In our updated Terms and Privacy Policy you’ll find."
label4 = Label(tab5, text=privacy_text)
label4.grid(row=12,column=0)

privacy_text2="We do not allow third-party banner ads on Summarizer. We have no intention to introduce them, but if we ever do, we will update this policy."
label4 = Label(tab5, text=privacy_text2)
label4.grid(row=14,column=0)

privacy_text1="We operate and provide our Services, including providing customer support, and improving, fixing, and customizing our Services"
label4 = Label(tab5, text=privacy_text1)
label4.grid(row=16,column=0)

privacy_text1="We do not store your data, when you click the reset button, the data is gone from our side too"
label4 = Label(tab5, text=privacy_text1)
label4.grid(row=18,column=0)


tab_control.pack(expand=1, fill='both')

# Functions 
def get_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSummary:{}'.format(final_text)
	tab1_display.insert(tk.END,result)


# Clear entry widget
def clear_text():
	entry.delete('1.0',END)

def clear_display_result():
	tab1_display.delete('1.0',END)


# Clear Text  with position 1.0
def clear_text_file():
	displayed_file.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
	tab2_display_text.delete('1.0',END)

# Clear For URL
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab3_display_text.delete('1.0',END)


# Clear entry widget
def clear_compare_text1():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab4_display.delete('1.0',END)




# Functions for TAB 2 FILE PROCESSER
# Open File to Read and Process
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)


def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab2_display_text.insert(tk.END,result)

# Fetch Text From Url
def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display_text.insert(tk.END,result)	


# COMPARER FUNCTIONS

def use_spacy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_nltk():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = nltk_summarizer(raw_text)
	print(final_text)
	result = '\nNLTK Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_gensim():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = summarize(raw_text)
	print(final_text)
	result = '\nGensim Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_sumy():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSumy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def spacy_sel():
	selection=int(spacy_var.get())
	mycursor.execute("INSERT INTO spacy VALUES({});".format(selection))
	mydb.commit()
	getspacyaverage()

def gensim_sel():
	selection=str(gensim_var.get())
	mycursor.execute("INSERT INTO gensim VALUES({});".format(selection))
	mydb.commit()

def NLTK_sel():
	selection=str(NLTK_var.get())
	mycursor.execute("INSERT INTO NLTK VALUES({});".format(selection))
	mydb.commit()

def sumy_sel():
	selection=str(sumy_var.get())
	mycursor.execute("INSERT INTO sumy VALUES({});".format(selection))
	mydb.commit()

def getspacyaverage():
	mycursor.execute("SELECT AVG(ratings) FROM spacy")
	myresult=mycursor.fetchone()
	res = float(''.join(map(str, myresult)))
	return res;

def getgensimaverage():
	mycursor.execute("SELECT AVG(ratings) FROM gensim")
	myresult=mycursor.fetchone()
	res = float(''.join(map(str, myresult)))
	return res;

def getNLTKaverage():
	mycursor.execute("SELECT AVG(ratings) FROM NLTK")
	myresult=mycursor.fetchone()
	res = float(''.join(map(str, myresult)))
	return res;

def getsumyaverage():
	mycursor.execute("SELECT AVG(ratings) FROM sumy")
	myresult=mycursor.fetchone()
	res = float(''.join(map(str, myresult)))
	return res;



# MAIN NLP TAB
l1=Label(tab1,text="Enter Text To Summarize")
l1.grid(row=1,column=0)

entry=Text(tab1,height=14,width=150)
entry.grid(row=2,column=0,columnspan=2,padx=5,pady=5)

# BUTTONS
button1=Button(tab1,text="Reset",command=clear_text, width=12,bg='#03A9F4',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab1,text="Extractive Summarizer",command=get_summary, width=14,bg='#03A9F4',fg='#fff')
button2.grid(row=4,column=0,padx=10,pady=10)

button3=Button(tab1,text="Clear Result", command=clear_display_result,width=12,bg='#03A9F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button2=Button(tab1,text="Abstractive Summarizer",command=get_summary, width=14,bg='#03A9F4',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)



# Display Screen For Result
tab1_display = Text(tab1)
tab1_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


#FILE PROCESSING TAB
l1=Label(tab2,text="Open File To Summarize")
l1.grid(row=1,column=1)

displayed_file = ScrolledText(tab2,height=7)# Initial was Text(tab2)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab2,text="Open File", width=12,command=openfiles,bg='#c5cae9')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab2,text="Reset ", width=12,command=clear_text_file,bg="#b9f6ca")
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg='blue',fg='#fff')
b2.grid(row=3,column=2,padx=10,pady=10)

b3=Button(tab2,text="Clear Result", width=12,command=clear_text_result)
b3.grid(row=5,column=1,padx=10,pady=10)

b4=Button(tab2,text="Close", width=12,command=window.destroy)
b4.grid(row=5,column=2,padx=10,pady=10)

# Display Screen
# tab2_display_text = Text(tab2)
tab2_display_text = ScrolledText(tab2,height=10)
tab2_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

# Allows you to edit
tab2_display_text.config(state=NORMAL)


# URL TAB
l1=Label(tab3,text="Enter URL To Summarize")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab3,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)

# BUTTONS
button1=Button(tab3,text="Reset",command=clear_url_entry, width=12,bg='#03A9F4',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab3,text="Get Text",command=get_text, width=12,bg='#03A9F4',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab3,text="Clear Result", command=clear_url_display,width=12,bg='#03A9F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab3,text="Summarize",command=get_url_summary, width=12,bg='#03A9F4',fg='#fff')
button4.grid(row=5,column=1,padx=10,pady=10)

# Display Screen For Result
url_display = ScrolledText(tab3,height=10)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


tab3_display_text = ScrolledText(tab3,height=10)
tab3_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)


# COMPARER TAB
l1=Label(tab4,text="Enter Text To Summarize")
l1.grid(row=1,column=0)

entry1=ScrolledText(tab4,height=10)
entry1.grid(row=2,column=0,columnspan=3,padx=5,pady=3)

# BUTTONS
button1=Button(tab4,text="Reset",command=clear_compare_text1, width=12,bg='#03A9F4',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab4,text="SpaCy",command=use_spacy, width=12,bg='red',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)

#scale for rating system
spacy_var=DoubleVar()
spacy_scale=Scale(tab4, from_= 0, to_= 10, variable = spacy_var,orient=HORIZONTAL)
spacy_scale.grid(row=5,column=1,padx=10,pady=10)

rating_button=Button(tab4,text="Submit",command=spacy_sel)
rating_button.grid(row=6,column=1,padx=10,pady=10)


button3=Button(tab4,text="Clear Result", command=clear_compare_display_result,width=12,bg='#03A9F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab4,text="NLTK",command=use_nltk, width=12,bg='#03A9F4',fg='#fff')
button4.grid(row=4,column=3,padx=10,pady=10)

NLTK_var=DoubleVar()
NLTK_scale=Scale(tab4, from_= 0, to_= 10, variable = NLTK_var,orient=HORIZONTAL)
NLTK_scale.grid(row=5,column=3,padx=10,pady=10)

rating_button=Button(tab4,text="Submit",command=NLTK_sel)
rating_button.grid(row=6,column=3,padx=10,pady=10)



button4=Button(tab4,text="Gensim",command=use_gensim, width=12,bg='#03A9F4',fg='#fff')
button4.grid(row=4,column=2,padx=10,pady=10)

gensim_var=DoubleVar()
gensim_scale=Scale(tab4, from_= 0, to_= 10, variable = gensim_var,orient=HORIZONTAL)
gensim_scale.grid(row=5,column=2,padx=10,pady=10)

rating_button=Button(tab4,text="Submit",command=gensim_sel)
rating_button.grid(row=6,column=2,padx=10,pady=10)

button4=Button(tab4,text="Sumy",command=use_sumy, width=12,bg='#03A9F4',fg='#fff')
button4.grid(row=4,column=4,padx=10,pady=10)


sumy_var=DoubleVar()
sumy_scale=Scale(tab4, from_= 0, to_= 10, variable = sumy_var,orient=HORIZONTAL)
sumy_scale.grid(row=5,column=4,padx=10,pady=10)

rating_button=Button(tab4,text="Submit",command=sumy_sel)
rating_button.grid(row=6,column=4,padx=10,pady=10)

l1=Label(tab4,text="Based on Users Ratings",height=1,font=18)
l1.grid(row=8,column=0,padx=13,pady=13)


l1=Label(tab4,text="spacy",height=1,font=16)
l1.grid(row=9,column=0)

l1=Label(tab4,text="gensim",height=1,font=16)
l1.grid(row=9,column=1)

l1=Label(tab4,text="NLTK",height=1,font=16)
l1.grid(row=9,column=2)

l1=Label(tab4,text="sumy",height=1,font=16)
l1.grid(row=9,column=3)

l1=Label(tab4,text=getspacyaverage(),height=1,font=14)
l1.grid(row=10,column=0,sticky="N")

l1=Label(tab4,text=getgensimaverage(),height=1,font=14)
l1.grid(row=10,column=1,sticky="N")

l1=Label(tab4,text=getNLTKaverage(),height=1,font=14)
l1.grid(row=10,column=2,sticky="N")

l1=Label(tab4,text=getsumyaverage(),height=1,font=14)
l1.grid(row=10,column=3,sticky="N")

# Display Screen For Result
tab4_display = ScrolledText(tab4,height=15)
tab4_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


# About TAB
about_label = Label(tab5,text="Summaryzer GUI V.0.0.1 \n\n Bhole saves @NpranavTech \n\n Bhole saves @PsahilTech \n\n Jesus saves @GmiteshTech",pady=5,padx=5)
about_label.grid(column=0,row=1)

window.mainloop()



# Jesse JCharis
# J-Secur1ty
# Jesus saves@JCharisTech