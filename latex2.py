from pynput import keyboard, mouse
from collections import deque
import tempfile 
import subprocess
import os 
from time import sleep
def open_editor(filename):
    subprocess.run([
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

print("Shit")
latex()