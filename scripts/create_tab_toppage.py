# -*- coding: utf-8 -*-
"""
Tabページ以下のTopページにあたる index.mdを自動生成する
"""

import os
import os.path
import re
import codecs
import glob

EXCLUSION = [".git", ".github", ".vscode", ".history", "_book",
             "node_modules", "stylesheets", "javascripts", 'pycache', 'workflows', 'ipynb']


def getTitle(path):

    with codecs.open(path, 'r', 'utf-8') as f:
        for l in f.readlines():
            if re.search("^title:.*", l):
                return l.strip("title:").strip()
    return None


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
                title = getTitle(path)
                mdPath = path.replace(f"{rootDir}/", "")
                indent = len(mdPath.split("/")) - 1
                writeLines.append(f"{indent * '    '}- [{title}]({mdPath})")

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
