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

BLOG_ROOT_DIR = "C:/reincarnation_tech"
GITHUB_ROOT = "https://github.com/fereria/reincarnation_tech/blob/master/"


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

    p = subprocess.Popen(['C:/Users/remiria/AppData/Local/Programs/Python/Python36/Scripts/jupyter',
                          'nbconvert',
                          '--to', 'markdown',
                          '--output', md,
                          '--template', f'{BLOG_ROOT_DIR}/jupyter_template.tpl',
                          ipynbFile])

    p.wait()

    buff = ipynbFile.split("/notebooks/")

    title = ['---',
             f'title: {title}',
             '---',
             f'ipynbFile: [{os.path.basename(ipynbFile)}]({GITHUB_ROOT}notebooks/{buff[1]})']

    with codecs.open(md, 'r', 'utf8') as f:
        lines = [x.replace("\n", "") for x in f.readlines()]

    lines = title + lines

    with codecs.open(md, 'w', 'utf8') as f:
        f.write("\n".join(lines))


if __name__ == "__main__":

    root = f"{BLOG_ROOT_DIR}/notebooks"
    md = f"{BLOG_ROOT_DIR}/docs/60_JupyterNotebook"

    if os.path.exists(md):
        shutil.rmtree(md, True)
    os.makedirs(md)

    ipynbFiles = glob.glob(root + "/*.ipynb")

    for ipynb in ipynbFiles:
        createNoteBookMD(ipynb, root, md)
