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
             "node_modules", "stylesheets", "javascripts", 'pycache', 'workflows', 'ipynb']


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

    for root, dirs, files in os.walk(rootDir):

        files.sort()

        if root != rootDir:
            root = root.replace("\\", "/")
            dirName = root.replace(rootDir + "/", "")
            for e in EXCLUSION:
                if e in dirName:
                    break
            buff = dirName.split("/")
            dirTitle = re.sub("[0-9][0-9]_", "", buff[-1])
            dirIndent = len(buff) - 1
            writeLines.append(f"{'    ' * dirIndent}- {dirTitle}")

        for f in files:
            path = os.path.join(root, f).replace("\\", "/")
            if os.path.splitext(path)[1] == ".md":
                header = getHeader(path)
                mdPath = path.replace(f"{rootDir}/", "")
                indent = len(mdPath.split("/")) - 1
                line = f"{indent * '    '}- [{header['title']}]({mdPath})"
                if 'description' in header:
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


if __name__ == "__main__":
    main()
