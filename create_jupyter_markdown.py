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
    md = exportPath + "/" + md_path + "/" + fileName
    md = md.replace("//", "/")
    if not os.path.exists(os.path.dirname(md)):
        os.makedirs(os.path.dirname(md))

    p = subprocess.Popen(['python',
                          '-m', 'nbconvert',
                          '--to', 'markdown',
                          '--output', md,
                          '--template', 'template/jupyter_template.tpl',
                          ipynbFile])

    print(f"convert ipynb to markdown -> {md}")

    p.wait()

    # 行の頭にリポジトリへのリンクを追加
    buff = ipynbFile.split("/notebooks/")

    title = ['---',
             f'title: {title}',
             '---',
             f'**ipynbFile** [{os.path.basename(ipynbFile)}]({GITHUB_ROOT}notebooks/{buff[1]})']

    with codecs.open(md, 'r', 'utf8') as f:
        lines = [x.replace("\n", "") for x in f.readlines()]

    lines = title + lines

    with codecs.open(md, 'w', 'utf8') as f:
        f.write("\n".join(lines))


def getIpynbFile():

    retVal = []
    for rootDir, dirs, files in os.walk(root):
        for f in files:
            if os.path.splitext(f)[1] == ".ipynb":
                retVal.append(os.path.join(rootDir, f))
    return retVal


if __name__ == "__main__":

    root = f"notebooks"
    md_root = f"docs/60_JupyterNotebook"

    if os.path.exists(md_root):
        shutil.rmtree(md_root, True)
    os.makedirs(md_root)

    # ipynbFiles = glob.glob(root + "/*.ipynb")
    ipynbFiles = getIpynbFile()
    print(ipynbFiles)

    for ipynb in ipynbFiles:
        createNoteBookMD(ipynb, root, md_root)
