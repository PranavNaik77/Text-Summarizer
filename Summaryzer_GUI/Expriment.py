# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
import tkinter.font as tkFont
import wx;
from PIL import ImageTk,Image

# NLP Pkgs
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
from Abstractive_summary import abstractive_summarizer
from sumy_summarization import sumy_summarizer


# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

import mysql.connector
class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pranav0707",
    database="ratings"
)

mycursor = mydb.cursor()

# Structure and Layout
window = Tk()
window.title("Summaryzer GUI")
window.geometry("1000x600")
window.config(background='black')
window.option_add('*Font', 'Times 11')
#window.resizable(width=False, height=False)

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn', )

# TAB LAYOUT
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')

if __name__ == "__main__":
    tab1=VerticalScrolledFrame(tab_control,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,
        background="light gray")
    tab2 = VerticalScrolledFrame(tab_control,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,
        background="light gray")
    tab3 = VerticalScrolledFrame(tab_control,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,
        background="light gray")
    tab4 = VerticalScrolledFrame(tab_control,
        width=300,
        borderwidth=2,
        relief=tk.SUNKEN,
        background="light gray")
tab5 = ttk.Frame(tab_control)


tab1.pack(fill=tk.BOTH, expand=True)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^20s}')
tab_control.add(tab3, text=f'{"URL":^20s}')
tab_control.add(tab4, text=f'{"Comparer ":^20s}')
tab_control.add(tab5, text=f'{"About ":^20s}')




label3 = Label(tab3, text='URL', padx=5, pady=5)
label3.grid(column=0, row=0)


#label4 = Label(tab5, text='About', padx=5, pady=5, font=18)
#label4.grid(column=0, row=1)

label4 = Label(tab5, text='\n\nPrivacy Policy', padx=5, pady=5, font=18,anchor="center")
label4.grid(row=10, column=4)

privacy_text = "Since we started Summarizer GUI, we’ve built our Services with a set of strong privacy principles in mind. In our updated Terms and Privacy Policy you’ll find."
label4 = Label(tab5, text=privacy_text,anchor="center")
label4.grid(row=13, column=4)

privacy_text2 = "We do not allow third-party banner ads on Summarizer. We have no intention to introduce them, but if we ever do, we will update this policy."
label4 = Label(tab5, text=privacy_text2,anchor="center")
label4.grid(row=15, column=4)

privacy_text1 = "We operate and provide our Services, including providing customer support, and improving, fixing, and customizing our Services"
label4 = Label(tab5, text=privacy_text1,anchor="center")
label4.grid(row=17, column=4)

privacy_text1 = "We do not store your data, when you click the reset button, the data is gone from our side too"
label4 = Label(tab5, text=privacy_text1,anchor="center")
label4.grid(row=19, column=4)

tab_control.pack(expand=1, fill='both')

# Functions
done='False'

#here is the animation
def animate():
    while done == 'false':
        sys.stdout.write('\rloading |')
        window.sleep(0.1)
        sys.stdout.write('\rloading /')
        window.sleep(0.1)
        sys.stdout.write('\rloading -')
        window.sleep(0.1)
        sys.stdout.write('\rloading \\')
        window.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def get_summary():
    raw_text = str(entry.get('1.0', tk.END))
    #animate()
    #print(raw_text)
    final_text = abstractive_summarizer(raw_text)
    done='True'
    #print(final_text)
    result = '\nSummary:{}'.format(final_text)
    tab1_display.insert(tk.END, result)

def get_spacy_summary():
    raw_text = str(entry.get('1.0', tk.END))
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSummary:{}'.format(final_text)
    tab1_display.insert(tk.END, result)

# Clear entry widget
def clear_text():
    entry.delete('1.0', END)


def clear_display_result():
    tab1_display.delete('1.0', END)


# Clear Text  with position 1.0
def clear_text_file():
    displayed_file.delete('1.0', END)


# Clear Result of Functions
def clear_text_result():
    tab2_display_text.delete('1.0', END)


# Clear For URL
def clear_url_entry():
    url_entry.delete(0, END)


def clear_url_display():
    tab3_display_text.delete('1.0', END)


# Clear entry widget
def clear_compare_text1():
    entry1.delete('1.0', END)


def clear_compare_display_result():
    tab4_display.delete('1.0', END)


# Functions for TAB 2 FILE PROCESSER
# Open File to Read and Process
def openfiles():
    file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END, read_text)


def get_file_summary():
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = abstractive_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab2_display_text.insert(tk.END, result)

def get_key_sentence_summary():
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = text_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab2_display_text.insert(tk.END, result)


# Fetch Text From Url
def get_text():
    raw_text = str(url_entry.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    url_display.insert(tk.END, fetched_text)


def get_url_summary():
    raw_text = url_display.get('1.0', tk.END)
    final_text = abstractive_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab3_display_text.insert(tk.END, result)

def get_key_sent_url_summary():
    raw_text = url_display.get('1.0', tk.END)
    final_text = text_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab3_display_text.insert(tk.END, result)


# COMPARER FUNCTIONS

def use_spacy():
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSpacy Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)


def use_nltk():
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = nltk_summarizer(raw_text)
    print(final_text)
    result = '\nNLTK Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)


def use_gensim():
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = summarize(raw_text)
    print(final_text)
    result = '\nGensim Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)


def use_sumy():
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSumy Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)


def spacy_sel():
    selection = int(spacy_var.get())
    mycursor.execute("INSERT INTO spacy VALUES({});".format(selection))
    mydb.commit()
    getspacyaverage()


def gensim_sel():
    selection = str(gensim_var.get())
    mycursor.execute("INSERT INTO gensim VALUES({});".format(selection))
    mydb.commit()


def NLTK_sel():
    selection = str(NLTK_var.get())
    mycursor.execute("INSERT INTO NLTK VALUES({});".format(selection))
    mydb.commit()


def sumy_sel():
    selection = str(sumy_var.get())
    mycursor.execute("INSERT INTO sumy VALUES({});".format(selection))
    mydb.commit()


def getspacyaverage():
    mycursor.execute("SELECT AVG(ratings) FROM spacy")
    myresult = mycursor.fetchone()
    res = float(''.join(map(str, myresult)))
    return res;


def getgensimaverage():
    mycursor.execute("SELECT AVG(ratings) FROM gensim")
    myresult = mycursor.fetchone()
    res = float(''.join(map(str, myresult)))
    return res;


def getNLTKaverage():
    mycursor.execute("SELECT AVG(ratings) FROM NLTK")
    myresult = mycursor.fetchone()
    res = float(''.join(map(str, myresult)))
    return res;


def getsumyaverage():
    mycursor.execute("SELECT AVG(ratings) FROM sumy")
    myresult = mycursor.fetchone()
    res = float(''.join(map(str, myresult)))
    return res;

def update(event):
    #var.set(str(len(entry.get('1.0', tk.END))))
    raw_text = str(entry.get('1.0', tk.END))
    words=raw_text.split(" ")
    var1.set(str((len(words)-1))+'/2000 Words')

def update_file_count(event):
    #var.set(str(len(entry.get('1.0', tk.END))))
    raw_text = str(displayed_file.get('1.0', tk.END))
    words=raw_text.split(" ")
    var2.set(str((len(words)-1))+'/2000 Words')

def update_url_count(event):
    #var.set(str(len(entry.get('1.0', tk.END))))
    raw_text = str(url_display.get('1.0', tk.END))
    words=raw_text.split(" ")
    var3.set(str((len(words)-1))+'/2000 Words')

def update_comparer_count(event):
    #var.set(str(len(entry.get('1.0', tk.END))))
    raw_text = str(entry1.get('1.0', tk.END))
    words=raw_text.split(" ")
    var4.set(str((len(words)-1))+'/2000 Words')

# MAIN NLP TAB
fontStyle = tkFont.Font(size=24)
fontStyle2= tkFont.Font(size=14)

topframe = tk.Frame(tab1)
topframe.grid(row=0,column=0,padx=20,pady=10)

label1 = Label(topframe, text='Summaryzer', padx=5, pady=5,font=fontStyle)
label1.grid(column=1, row=0)

l1 = Label(topframe, text="Enter Text To Summarize",padx=5, pady=5,font=fontStyle2)
l1.grid(row=1, column=1)


entry_frame = tk.Frame(tab1,width=275, height=115)
entry_frame.grid(row=2,column=0,padx=20,pady=20)

entry = ScrolledText(entry_frame, height=18, width=140,font="TimesNewRoman 12")
entry.tag_configure("center",justify='center')

entry.tag_add("left",1.0,"end")
entry.grid(row=0, column=0,padx=10, pady=10)

var1=StringVar()
charCount1 = Label(entry_frame,textvariable=var1,font=fontStyle2)
charCount1.grid(row=1, column=0, pady=5, padx=5)

entry.bind("<KeyRelease>", update)



button_frame = tk.Frame(tab1,width=275, height=115)
button_frame.grid(row=5,column=0,padx=20,pady=20)
# BUTTONS
button1 = Button(button_frame, text="Reset", command=clear_text, width=18, bg='#03A9F4', fg='#fff')
button1.grid(row=0, column=0, padx=10, pady=10)

button3 = Button(button_frame, text="Clear Result", command=clear_display_result, width=18, bg='#03A9F4', fg='#fff')
button3.grid(row=0, column=6, padx=10, pady=10)

button2 = Button(button_frame, text="Key Sentences", command=get_spacy_summary, width=18, bg='#03A9F4', fg='#fff')
button2.grid(row=0, column=12,padx=10, pady=10)

button2 = Button(button_frame, text="Abstractive Mode", command=get_summary, width=18, bg='#03A9F4', fg='#fff')
button2.grid(row=0, column=18, padx=10, pady=10)

dispaly_frame = tk.Frame(tab1)
dispaly_frame.grid(row=7,column=0,padx=20,pady=20)
# Display Screen For Result

tab1_display = ScrolledText(dispaly_frame,height=15,width=120,font="TimesNewRoman 12")
tab1_display.tag_configure("center",justify='center')

tab1_display.tag_add("center",1.0,"end")
tab1_display.grid(row=0, column=2,padx=30,pady=10)


label2 = Label(tab1, text='Summarize any text with a click of a button', padx=5, pady=5,font=fontStyle)
label2.grid(column=0, row=12,padx=10,pady=10)

label3 = Label(tab1, text='Our summarizer can condense articles, papers, or documents down to the key points instantly. Our AI \n uses natural language processing to locate critical information while maintaining the original context.', font=fontStyle2, padx=5, pady=5)
label3.grid(column=0, row=13,padx=20,pady=10)

label2 = Label(tab1, text='Different algorithms gives Different Keysentences', padx=5, pady=5,font=fontStyle)
label2.grid(column=0, row=14,padx=10,pady=10)

label3 = Label(tab1, text='Our comparer gives you different choices of libraries to choose from. \n Users can select the most efficient one based on their input. Loved a particular library? Rate it in our comparer tab', font=fontStyle2, padx=5, pady=5)
label3.grid(column=0, row=15,padx=20,pady=10)


label4 = Label(tab1, text='You can Summarize in two ways', padx=5, pady=5,font=fontStyle2)
label4.grid(column=0, row=17,padx=4,pady=5)

image_frame = tk.Frame(tab1)
image_frame.grid(row=18,column=0,padx=30,pady=30)

image = Image.open('keysentences.png')
image=image.resize((350, 300), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(image)
panel = Label(image_frame, image = my_img)#
panel.grid(column=0,row=0,padx=10,pady=10)

image = Image.open('paragraph.png')
image=image.resize((350, 300), Image.ANTIALIAS)
my_img1 = ImageTk.PhotoImage(image)
panel = Label(image_frame, image = my_img1)
panel.grid(column=1,row=0,padx=10,pady=10)

label3 = Label(image_frame, text='Key Sentences gives you a bullet point list \n of the most important sentences.', font=fontStyle2, padx=5, pady=5)
label3.grid(column=0, row=1,padx=10,pady=10)

label3 = Label(image_frame, text='Abstractive mode gives you a unique paragraph summarizing \n the content. ', font=fontStyle2, padx=5, pady=5)
label3.grid(column=1, row=1,padx=10,pady=10)

label4 = Label(tab1, text='Whether you have a', padx=5, pady=5,font=fontStyle2)
label4.grid(column=0, row=19,padx=10,pady=10)

image_frame2 = tk.Frame(tab1)
image_frame2.grid(row=20,column=0,padx=10,pady=10)

news_image = Image.open('NewsArticle.png')
news_image=news_image.resize((150, 150), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(news_image)
panel1 = Label(image_frame2, image = img1)
panel1.grid(column=0,row=0)

research_image = Image.open('ResearchPaper.png')
research_image=research_image.resize((150, 150), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(research_image)
panel2 = Label(image_frame2, image = img2)
panel2.grid(column=1,row=0)

para_image = Image.open('confusingParagraph.png')
para_image=para_image.resize((150, 150), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(para_image)
panel3 = Label(image_frame2, image = img3)
panel3.grid(column=2,row=0)

label2 = Label(image_frame2, text='News \n Article', font=fontStyle2, padx=5, pady=5)
label2.grid(column=0, row=1,padx=10,pady=10)

label3 = Label(image_frame2, text='Research \n Paper', font=fontStyle2, padx=5, pady=5)
label3.grid(column=1, row=1,padx=10,pady=10)

label4 = Label(image_frame2, text='Confusing \n Paragraph', font=fontStyle2, padx=5, pady=5)
label4.grid(column=2, row=1,padx=10,pady=10)

label4 = Label(tab1, text='The summarizer tool will help you get the information that you need.', padx=5, pady=5,font=fontStyle2)
label4.grid(column=0, row=24,padx=20,pady=20)

# FILE PROCESSING TAB

fontStyle = tkFont.Font(size=24)
fontStyle2= tkFont.Font(size=14)

topframe = tk.Frame(tab2)
topframe.grid(row=0,column=0,padx=20,pady=10)

label1 = Label(topframe, text='Open File to Summarize', padx=5, pady=5,font=fontStyle)
label1.grid(column=1, row=0)

entry_frame = tk.Frame(tab2,width=275, height=115)
entry_frame.grid(row=2,column=0,padx=30,pady=30)

displayed_file = ScrolledText(entry_frame, height=18, width=130,font="TimesNewRoman 12")  # Initial was Text(tab2)
displayed_file.grid(row=0, column=0,padx=10, pady=10)


var2 = StringVar()
charCount2 = Label(entry_frame,textvariable=var2,font=fontStyle2)
charCount2.grid(row=1, column=0, pady=5, padx=5)

displayed_file.bind("<KeyRelease>", update_file_count)


# BUTTONS FOR SECOND TAB/FILE READING TAB
button_frame = tk.Frame(tab2,width=275, height=115)
button_frame.grid(row=5,column=0,padx=30,pady=30)

b0 = Button(button_frame, text="Open File", width=16, height=2,command=openfiles, bg='#b9f6ca',font=16)
b0.grid(row=0, column=0,padx=15,pady=15)

b1 = Button(button_frame, text="Reset ", width=12, command=clear_text_file, bg="#b9f6ca")
b1.grid(row=0, column=4,padx=15,pady=15)

b2 = Button(button_frame, text="Key Sentences", width=12, command=get_key_sentence_summary, bg='#b9f6ca')
b2.grid(row=0, column=6,padx=15,pady=15)

b5 = Button(button_frame, text="Abstractive Mode", width=12, command=get_file_summary, bg='#b9f6ca')
b5.grid(row=0, column=12,padx=15,pady=15)

b3 = Button(button_frame, text="Clear Result", width=12, command=clear_text_result,bg='#b9f6ca')
b3.grid(row=0, column=16,padx=15,pady=15)

b4 = Button(button_frame, text="Close", width=12, command=window.destroy,bg='#b9f6ca')
b4.grid(row=0, column=20,padx=15,pady=15)

# Display Screen
# tab2_display_text = Text(tab2)

dispaly_frame = tk.Frame(tab2)
dispaly_frame.grid(row=7,column=0,padx=30,pady=30)

tab2_display_text = ScrolledText(dispaly_frame, height=15,width=130,font="TimesNewRoman 12")
tab2_display_text.grid(row=0, column=2, columnspan=3, padx=5, pady=5)

# Allows you to edit
#tab2_display_text.config(state=NORMAL)

# URL TAB
fontStyle = tkFont.Font(size=24)
fontStyle2= tkFont.Font(size=14)

topframe = tk.Frame(tab3)
topframe.grid(row=0,column=0)

l1 = Label(topframe, text="Enter URL To Summarize",font=fontStyle)
l1.grid(row=1, column=0,padx=20,pady=20)

raw_entry = StringVar()
url_entry = Entry(topframe, textvariable=raw_entry, width=50,font="TimesNewRoman 12")
url_entry.grid(row=1, column=2,padx=20,pady=20)

# BUTTONS
button_frame = tk.Frame(tab3,width=275, height=115)
button_frame.grid(row=4,column=0,padx=30,pady=30)

button1 = Button(button_frame, text="Reset", command=clear_url_entry, width=12, bg='red', fg='#fff')
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = Button(button_frame, text="Get Text", command=get_text, width =12, bg='red', fg='#fff')
button2.grid(row=0, column=1, padx=10, pady=10)

button3 = Button(button_frame, text="Clear Result", command=clear_url_display, width=12, bg='red', fg='#fff')
button3.grid(row=0, column=2, padx=10, pady=10)

button4 = Button(button_frame, text="KeySentences", command=get_key_sent_url_summary, width=12, bg='red', fg='#fff')
button4.grid(row=0, column=3, padx=10, pady=10)

button5 = Button(button_frame, text="Abstractive Mode", command=get_url_summary, width=13, bg='red', fg='#fff')
button5.grid(row=0, column=4, padx=10, pady=10)

# Display Screen For Result
entry_frame = tk.Frame(tab3,width=275, height=115)
entry_frame.grid(row=7,column=0,padx=20,pady=20)

url_display = ScrolledText(entry_frame, height=18,width=140,font="TimesNewRoman 12")
url_display.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

var3 = StringVar()

charCount3 = Label(entry_frame,textvariable=var3,font=fontStyle2)
charCount3.grid(row=2, column=0, pady=5, padx=5)

url_display.bind("<KeyRelease>", update_url_count)


dispaly_frame = tk.Frame(tab3)
dispaly_frame.grid(row=9,column=0,padx=20,pady=20)

tab3_display_text = ScrolledText(dispaly_frame, height=15,width=120,font="TimesNewRoman 12")
tab3_display_text.grid(row=0, column=0, padx=20, pady=20)

# COMPARER TAB
fontStyle = tkFont.Font(size=24)
fontStyle2= tkFont.Font(size=14)

topframe = tk.Frame(tab4)
topframe.grid(row=0,column=0,padx=20,pady=20)

label3 = Label(topframe, text='Compare Summarizers', padx=5, pady=5,font=fontStyle)
label3.grid(column=2, row=0)

l1 = Label(topframe, text="Enter Text To Summarize",padx=5, pady=5,font=fontStyle2)
l1.grid(row=1, column=2)

entry_frame = tk.Frame(tab4,width=275, height=115)
entry_frame.grid(row=3,column=0,padx=20,pady=20)

entry1 = ScrolledText(entry_frame, height=18,width=130,font="TimesNewRoman 12")
entry1.grid(row=0, column=0, padx=10, pady=10)

var4 = StringVar()
charCount4 = Label(entry_frame,textvariable=var4,font=fontStyle2)
charCount4.grid(row=1, column=0, pady=5, padx=5)

entry1.bind("<KeyRelease>", update_comparer_count)


# BUTTONS
button_frame = tk.Frame(tab4,width=275, height=115)
button_frame.grid(row=6,column=0,padx=20,pady=20)

button1 = Button(button_frame, text="Reset", command=clear_compare_text1, width=12, bg='black', fg='#fff')
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = Button(button_frame, text="SpaCy", command=use_spacy, width=12, bg='black', fg='#fff')
button2.grid(row=0, column=1, padx=10, pady=10)

# scale for rating system
spacy_var = DoubleVar()
spacy_scale = Scale(button_frame, from_=0, to_=10, variable=spacy_var, orient=HORIZONTAL)
spacy_scale.grid(row=1, column=1, padx=10, pady=10)

rating_button = Button(button_frame, text="Submit", command=spacy_sel, bg='black', fg='#fff')
rating_button.grid(row=2, column=1, padx=10, pady=10)

button3 = Button(button_frame, text="Clear Result", command=clear_compare_display_result, width=12, bg='black', fg='#fff')
button3.grid(row=1, column=0, padx=10, pady=10)

button4 = Button(button_frame, text="NLTK", command=use_nltk, width=12, bg='black', fg='#fff')
button4.grid(row=0, column=3, padx=10, pady=10)

NLTK_var = DoubleVar()
NLTK_scale = Scale(button_frame, from_=0, to_=10, variable=NLTK_var, orient=HORIZONTAL)
NLTK_scale.grid(row=1, column=3, padx=10, pady=10)

rating_button = Button(button_frame, text="Submit", command=NLTK_sel, bg='black', fg='#fff')
rating_button.grid(row=2, column=3,padx=10, pady=10)

button4 = Button(button_frame, text="Gensim", command=use_gensim, width=12, bg='black', fg='#fff')
button4.grid(row=0, column=2, padx=10, pady=10)

gensim_var = DoubleVar()
gensim_scale = Scale(button_frame, from_=0, to_=10, variable=gensim_var, orient=HORIZONTAL)
gensim_scale.grid(row=1, column=2, padx=10, pady=10)

rating_button = Button(button_frame, text="Submit", command=gensim_sel, bg='black', fg='#fff')
rating_button.grid(row=2, column=2, padx=10, pady=10)

button4 = Button(button_frame, text="Sumy", command=use_sumy, width=12, bg='black', fg='#fff')
button4.grid(row=0, column=4, padx=10, pady=10)

sumy_var = DoubleVar()
sumy_scale = Scale(button_frame, from_=0, to_=10, variable=sumy_var, orient=HORIZONTAL)
sumy_scale.grid(row=1, column=4, padx=10, pady=10)

rating_button = Button(button_frame, text="Submit", command=sumy_sel, bg='black', fg='#fff')
rating_button.grid(row=2, column=4, padx=10, pady=10)

#Display Screen For Result
dispaly_frame = tk.Frame(tab4)
dispaly_frame.grid(row=8,column=0,padx=20,pady=20)

tab4_display = ScrolledText(dispaly_frame, height=15,width=130,font="TimesNewRoman 12")
tab4_display.grid(row=0, column=2, padx=30,pady=10)

text_frame = tk.Frame(tab4)
text_frame.grid(row=14,column=0,padx=10,pady=10)

l1 = Label(tab4, text="Based on Users Ratings", font=fontStyle)
l1.grid(row=12, column=0,padx=10,pady=10)

l1 = Label(text_frame, text="spacy", font=fontStyle2)
l1.grid(row=7, column=0)

l1 = Label(text_frame, text="gensim", font=fontStyle2)
l1.grid(row=7, column=2)

l1 = Label(text_frame, text="NLTK",font=fontStyle2)
l1.grid(row=7, column=4)

l1 = Label(text_frame, text="sumy", font=fontStyle2)
l1.grid(row=7, column=6)

l1 = Label(text_frame, text=getspacyaverage(), font=fontStyle2)
l1.grid(row=8, column=0)

l1 = Label(text_frame, text=getgensimaverage(), font=fontStyle2)
l1.grid(row=8, column=2)

l1 = Label(text_frame, text=getNLTKaverage(), font=fontStyle2)
l1.grid(row=8, column=4)

l1 = Label(text_frame, text=getsumyaverage(), font=fontStyle2)
l1.grid(row=8, column=6)


# About TAB
about_label = Label(tab5,
                    text="Summaryzer GUI V.0.0.1 \n\n Created by \n\n Pranav Naik \n\n Sahil Panchal \n\n Mitesh Goswami",
                    pady=5, padx=5,anchor="center")
about_label.grid(column=4, row=1)

window.mainloop()
