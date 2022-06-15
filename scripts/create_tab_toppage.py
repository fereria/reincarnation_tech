# -*- coding: utf-8 -*-
"""
Tabページ以下のTopページにあたる index.mdを自動生成する
"""

import os
import os.path
import re
import codecs
import glob
import yaml

EXCLUSION = [".git", ".github", ".vscode", ".history", "_book",
             "node_modules", "stylesheets", "javascripts", 'pycache', 'workflows', 'ipynb',
             'blender_samplecode', 'pyside_samplecode', 'python_samplecode']


def getHeader(path):

    yamlValue = []

    st = False

    with codecs.open(path, 'r', 'utf-8') as f:
        for i in f.readlines():
            if '---' in i:
                if st:
                    break
                else:
                    st = True
            elif i == "":
                continue
            else:
                yamlValue.append(i.strip())
    if st:
        return yaml.load("\n".join(yamlValue))
    else:
        return {'title': ""}


def createIndexMd(rootDir):

    writeLines = []

    for root, dirs, files in os.walk(rootDir, topdown=False):

        files.sort()

        if root != rootDir:
            root = root.replace("\\", "/")
            dirName = root.replace(rootDir + "/", "")

            flg = False
            for e in EXCLUSION:
                if e == dirName:
                    flg = True

            if not flg:
                buff = dirName.split("/")
                dirTitle = re.sub("[0-9][0-9]_", "", buff[-1])
                dirIndent = len(buff) - 1

                if len(glob.glob(root + "/*.md")) > 0:
                    writeLines.append(f"\n#{'#' * dirIndent}{dirTitle}\n")

                for f in files:
                    path = os.path.join(root, f).replace("\\", "/")
                    if os.path.splitext(path)[1] == ".md":
                        header = getHeader(path)
                        mdPath = path.replace(f"{rootDir}/", "")
                        line = f"- [{header['title']}]({mdPath})"
                        if 'description' in header and header['description']:
                            line += f": {header['description']}"
                        writeLines.append(line)

    with codecs.open(f"{rootDir}/index.md", 'w', 'utf-8') as f:
        f.write("\n".join(writeLines))


def main():

    docs = (os.getcwd() + "/docs").replace("\\", "/")

    for d in os.listdir(docs):
        if re.search('[0-9][0-9]_', d):
            path = docs + "/" + d
            if not os.path.exists(path + "/index.md"):
                createIndexMd(path)


def samplecode():

    docs = (os.getcwd() + "/docs").replace("\\", "/")
    createIndexMd(f"{docs}/11_PySide")


if __name__ == "__main__":
    main()
