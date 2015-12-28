from math import sin
from Tkinter import *
import tkMessageBox
import tkFileDialog

from image import *
from save import *

import codecs

top = Tk()
top.resizable(width=FALSE, height=FALSE)
top.geometry("960x674")
top.wm_title("Editor")

LAST_FILENAME = ""
SINGLE_IMAGE = IntVar()
SINGLE_ANSWER_FILE = ""
IMAGE_FILE = ""
ANSWER_FRAMES = []
ANSWER_NUM = 0
MUSIC_FILE = ""

def switchSigleImageMode():
    global imageCanvas
    global IMAGE_FILE
    IMAGE_FILE = ""
    if SINGLE_IMAGE.get() == 1:
        imageCanvas.pack_forget()
        imageCanvas = Canvas(imageFrame, width=960, height=640);
        imageCanvas.bind('<Button-1>', loadImageFile)
        imageFrame.config(width=960)
        nextSceneButton.pack(fill=X, side=LEFT, anchor=W)
    else:
        imageCanvas.pack_forget()
        imageCanvas = Canvas(imageFrame, width=320, height=640);
        imageCanvas.bind('<Button-1>', loadImageFile)
        imageFrame.config(width=320)
        nextSceneButton.pack_forget()

def loadImageFile(*args):
    global IMAGE_FILE
    img = tkFileDialog.askopenfilename(filetypes=[('5-bit encoded image', '.BIN')], initialdir=".")
    if img != "":
        IMAGE_FILE = img
        renderImage()

def load_music_file():
    global MUSIC_FILE
    snd = tkFileDialog.askopenfilename(filetypes=[('encoded soundtrask', '.SND')], initialdir=".")
    if snd != "":
        MUSIC_FILE = snd
        musicButton.config(text=MUSIC_FILE.split("/")[-1])
    
def renderImage():
    print IMAGE_FILE
    if IMAGE_FILE != "":
        if draw_image(*(load_image(IMAGE_FILE) + (imageCanvas,))):
            imageCanvas.pack()

def reloadAnswers():
    global ANSWER_NUM
    for answer in ANSWER_FRAMES:
        if answer is not None:
            answer.hide()
    ANSWER_NUM = 0
    for answer in ANSWER_FRAMES:
        if answer is not None:
            answer.show(ANSWER_NUM)
            ANSWER_NUM += 1

def deleteAnswerButton(num):
    print num
    if ANSWER_FRAMES[num].filename == "":
        tkMessageBox.showinfo("", "Cannot delete empty answer")
    else:
        ANSWER_FRAMES[num].hide()
        ANSWER_FRAMES[num] = None
    reloadAnswers()

def loadAnswerFileSingle():
    global SINGLE_ANSWER_FILE
    SINGLE_ANSWER_FILE = tkFileDialog.askopenfilename(filetypes=[('editor encoded files', '.TXT')], initialdir=".")
    if SINGLE_ANSWER_FILE != "":
        nextSceneButton.config(text=SINGLE_ANSWER_FILE.split("/")[-1])

def loadAnswerFile(num):
    shouldAdd = ANSWER_FRAMES[num].filename == ""
    ANSWER_FRAMES[num].filename = tkFileDialog.askopenfilename(filetypes=[('editor encoded files', '.TXT')], initialdir=".")
    if ANSWER_FRAMES[num].filename != "":    
        ANSWER_FRAMES[num].pick.config(text=ANSWER_FRAMES[num].filename.split("/")[-1])
        ANSWER_FRAMES[num].remove.pack(side=LEFT)
        
        if shouldAdd:
            ANSWER_FRAMES.append(answerFrame(answerTable, len(ANSWER_FRAMES)))
        
        reloadAnswers()

def saveToFile():
    global LAST_FILENAME
    while True:    
        filename = tkFileDialog.asksaveasfilename(initialfile=LAST_FILENAME, defaultextension=".TXT", filetypes=[('editor encoded files', '.TXT')], initialdir=".")

        if filename == "":
            return
        
        LAST_FILENAME = filename.split("/")[-1]
        top.wm_title(LAST_FILENAME)
                
        if len(filename.split("/")[-1].split(".")[0]) != 8 or filename.split("/")[-1].split(".")[1] != "TXT":
                tkMessageBox.showwarning("", "Wrong file name")
        else:
            break
    names = filename.split("/")
    names[-1] = names[-1].upper()
    filename = "/".join(names)
    
    if SINGLE_IMAGE.get() == 1:
        if validate_full(MUSIC_FILE, IMAGE_FILE, SINGLE_ANSWER_FILE)[0]:
            with open(filename, "w") as out:
                out.write(code_full(MUSIC_FILE, IMAGE_FILE, SINGLE_ANSWER_FILE).encode('utf-8'))
        else:
            tkMessageBox.showwarning("", validate_full(MUSIC_FILE, IMAGE_FILE, SINGLE_ANSWER_FILE)[1])
    else:
        if validate_third(MUSIC_FILE, IMAGE_FILE, mainText.get("1.0",END), [(x.entry.get(), x.pick.config('text')[-1]) for x in ANSWER_FRAMES if x is not None])[0]:
            with open(filename, "w") as out:
                out.write(code_third(MUSIC_FILE, IMAGE_FILE, mainText.get("1.0",END), [(x.entry.get(), x.pick.config('text')[-1]) for x in ANSWER_FRAMES if x is not None]).encode('utf-8'))
        else:
            tkMessageBox.showwarning("", validate_third(MUSIC_FILE, IMAGE_FILE, mainText.get("1.0",END), [(x.entry.get(), x.pick.config('text')[-1]) for x in ANSWER_FRAMES if x is not None])[1])

def new(newanswer=True):
    global MUSIC_FILE
    global ANSWER_FRAMES
    global SINGLE_ANSWER_FILE
    global IMAGE_FILE
    imageOnlyCheckButton.deselect()
    switchSigleImageMode()
    for answer in ANSWER_FRAMES:
        if answer is not None:
            answer.hide()
    ANSWER_FRAMES = []
    SINGLE_ANSWER_FILE = ""
    MUSIC_FILE = ""
    IMAGE_FILE = ""
    ANSWER_NUM = 0
    if newanswer:
        ANSWER_FRAMES.append(answerFrame(answerTable, len(ANSWER_FRAMES)))
    reloadAnswers()
    nextSceneButton.config(text="Pick scene")
    musicButton.config(text="Pick soundtrack")
    mainText.delete("1.0",END)

def open_file():
    global LAST_FILENAME
    global ANSWER_FRAMES
    global SINGLE_ANSWER_FILE
    global IMAGE_FILE
    global MUSIC_FILE
    filename = tkFileDialog.askopenfilename(filetypes=[('editor encoded files', '.TXT')], initialdir=".")
    if filename != "":
        new(newanswer=False)
        with codecs.open(filename, "r", encoding='utf-8') as infile:
            settings = decode(infile.read())
            if settings.get("single_resource") is not None:
                LAST_FILENAME = filename.split("/")[-1]
                top.wm_title(LAST_FILENAME)
                SINGLE_ANSWER_FILE = settings.get("single_resource", "Pick scene")
                nextSceneButton.config(text=SINGLE_ANSWER_FILE)
                imageOnlyCheckButton.select()
                switchSigleImageMode()
                IMAGE_FILE = settings.get("image")
                renderImage()
                MUSIC_FILE = settings.get("sound")
                musicButton.config(text=MUSIC_FILE)
            elif settings.get("image") is not None:
                LAST_FILENAME = filename.split("/")[-1]
                top.wm_title(LAST_FILENAME)
                imageOnlyCheckButton.deselect()
                switchSigleImageMode()
                IMAGE_FILE = settings.get("image")
                renderImage()
                mainText.insert("1.0",settings.get("text", ""))
                for answer in settings.get("variants"):
                    a = answerFrame(answerTable, len(ANSWER_FRAMES))
                    a.entry.insert("0",answer[0])
                    a.pick.config(text=answer[1])
                    a.remove.pack(side=LEFT)
                    a.filename = answer[1]
                    ANSWER_FRAMES.append(a)
                ANSWER_FRAMES.append(answerFrame(answerTable, len(ANSWER_FRAMES)))
                MUSIC_FILE = settings.get("sound")
                musicButton.config(text=MUSIC_FILE)
            else:
                tkMessageBox.showwarning("", "wrong file format")

menuFame = Frame(top); menuFame.pack(fill=X)
newButton = Button(menuFame, text = "  New  ", command=new); newButton.pack(fill=X, side=LEFT, anchor=W)
openButton = Button(menuFame, text = "  Open ", command=open_file); openButton.pack(fill=X, side=LEFT, anchor=W)
saveAsButton = Button(menuFame, text = "Save as", command=saveToFile); saveAsButton.pack(fill=X, side=LEFT, anchor=W)
musicButton = Button(menuFame, text = "Pick soundtrack", command=load_music_file); musicButton.pack(fill=X, side=LEFT, anchor=W)
imageOnlyCheckButton = Checkbutton(menuFame, text="image only", variable=SINGLE_IMAGE, command=switchSigleImageMode); imageOnlyCheckButton.pack(fill=X, side=LEFT, anchor=W)
nextSceneButton = Button(menuFame, text="Pick scene", command = loadAnswerFileSingle)

mainFrame = Frame(top); mainFrame.pack()

imageFrame = Frame(mainFrame, width=320, height=640); imageFrame.pack(side = LEFT)
imageLoadButton = Button(imageFrame, text="Set image", command=loadImageFile); imageLoadButton.place(relx=0.5, rely=0.5, anchor=CENTER);

imageCanvas = Canvas(imageFrame, width=320, height=640)
imageCanvas.bind('<Button-1>', loadImageFile)

editWindow = PanedWindow(mainFrame, orient=VERTICAL, sashrelief=RAISED); editWindow.pack(fill=BOTH, side = LEFT)

mainText = Text(editWindow, width=100)
editWindow.add(mainText)

answerTable = Frame(editWindow, width=640)
editWindow.add(answerTable);

class answerFrame(object):
    def __init__(self, parent, index):
        global ANSWER_NUM
        self.num = ANSWER_NUM
        ANSWER_NUM += 1
        self.frame = Frame(parent); self.frame.grid(column=0, row=self.num)
        self.entry = Entry(self.frame, width=60); self.entry.pack(fill=X, side=LEFT, expand=True)
        self.pick = Button(self.frame, text="pick scene", command=lambda: loadAnswerFile(index)); self.pick.pack(side=LEFT)
        self.remove = Button(self.frame, text="X", command=lambda: deleteAnswerButton(index));
        self.filename = ""
            
    def hide(self):
        self.frame.pack_forget()
        self.entry.pack_forget()
        self.pick.pack_forget()
        self.remove.pack_forget()
    
    def show(self, num):
        self.frame.grid(column=0, row=num)
        self.entry.pack(fill=X, side=LEFT, expand=True)
        self.pick.pack(side=LEFT)
        self.remove.pack(side=LEFT)
    
ANSWER_FRAMES.append(answerFrame(answerTable, len(ANSWER_FRAMES)))
top.mainloop()
