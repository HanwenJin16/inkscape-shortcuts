import mouse
import keyboard
from collections import deque
import tempfile 
import subprocess
import os 
from time import sleep
def open_editor(filename):
    subprocess.run(['sudo','-u','hanwen'
        'urxvt',
        '-name', 'popup-bottom-center',
        '-e', "vim",
        f"{filename}",
    ])


def latex_document(latex):
    return r"""\documentclass[14pt,border=12pt]{minimal}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{amsmath, amssymb}
\usepackage{xcolor}
\pagestyle{empty}
\begin{document}
    """ + latex + r"""
\end{document}"""
def latex():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    old_dir=os.getcwd()
    #Move to tmp directory to avoid being too messy
    os.chdir("tmp")
    m = tempfile.NamedTemporaryFile(suffix=r".tex",mode='w+', delete=False)
    m.close()
    print(m.name)
    open_editor(m.name)

    f=open(m.name,"r")
    latex=f.readline()
    f.close()

    g=open(m.name,"w")
    g.write(latex_document(latex))
    g.close()
    subprocess.run(
            ['pdflatex', m.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    seedname=m.name.split(r".")[0]
    seedname=seedname.split("/")[-1]

    print(seedname)
    #Convert to svg
    subprocess.run(
            ['pdf2svg', f'{seedname}.pdf', f'{seedname}.svg'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    #Copy to clipboard 
    with open(f'{seedname}.svg') as svg:
            subprocess.run(
                ['xclip', '-selection', 'c', '-target', 'image/x-inkscape-svg'],
                stdin=svg
            )
    os.chdir(old_dir)

os.environ["VIMRUN"]="F"
# Create a deque with a maximum length of 2
events = deque(maxlen=2)

def on_key_event(e):
    key = e.name  # Name of the key
    if e.event_type == 'down':  # Key press event
        if key == 't' or key == 'T':
            print("Yes")
            events.append("T")
        else:
            events.append("NT")

def on_click_event(e):
    if e.event_type == 'down':  # Mouse button press event
        if e.button == mouse.LEFT:
            events.append("LK")
            # Check the sequence
            if len(events) == 2 and events[0] == "T" and events[1] == "LK":
                subprocess.run(['sudo','-u','hanwen',
                'python3','latex2.py',
                ]) 
        else:
            events.append("NLK")


A=[0]
# Hook events
keyboard.hook(on_key_event)
mouse.hook(on_click_event)

# Keep the program running
keyboard.wait()