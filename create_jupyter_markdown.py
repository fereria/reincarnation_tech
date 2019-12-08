#!python3.6
# -*- coding: utf-8 -*-

import nbconvert
import nbformat
import codecs
import subprocess

import os.path
import re
import glob
import shutil


def createNoteBookMD(ipynbFile, root, exportPath):

    ipynbFile = re.sub("\\\\", "/", ipynbFile)
    ipynbFile = ipynbFile.replace("//", "/")
    root = re.sub("\\\\", "/", root)
    root = root.replace("//", "/")

    bn = os.path.splitext(os.path.basename(ipynbFile))[0]
    # FileNameは En__Title にする。
    # __がなければファイル名とタイトルは同じ。
    buff = bn.split("__")

    if len(buff) > 1:
        fileName = buff[0] + ".md"
        title = buff[1]
    else:
        fileName = bn + ".md"
        title = bn

    md_path = re.sub(root, "", os.path.dirname(ipynbFile))
    md = os.path.join(exportPath, md_path, fileName)

    p = subprocess.Popen(['jupyter',
                          'nbconvert',
                          '--to', 'markdown',
                          '--output', md,
                          '--template', 'C:/reincarnation_tech/jupyter_template.tpl',
                          ipynbFile])

    p.wait()

    title = ['---', f'title: {title}', '---']

    with codecs.open(md, 'r', 'utf8') as f:
        lines = [x.replace("\n", "") for x in f.readlines()]

    lines = title + lines

    with codecs.open(md, 'w', 'utf8') as f:
        f.write("\n".join(lines))


if __name__ == "__main__":

    root = "C:/reincarnation_tech/notebooks"
    md = "C:/reincarnation_tech/docs/60_JupyterNotebook"

    if os.path.exists(md):
        shutil.rmtree(md, True)
        os.makedirs(md)

    ipynbFiles = glob.glob(root + "/*.ipynb")

    for ipynb in ipynbFiles:
        createNoteBookMD(ipynb, root, md)
