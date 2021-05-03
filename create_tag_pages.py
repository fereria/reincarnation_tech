#!python3.6
# -*- coding: utf-8 -*-
"""
mkdocs用のDir用ファイル自動生成
"""

import os
import os.path
import re
import codecs
import glob
import sys

EXCLUSION = [".git", ".vscode", ".history", "_book", "node_modules", "stylesheets", "javascripts"]

TAG_PAGE = """---
pagetype: tagpage
---

# Tag: {tag}"""


def getTags(mdFile):

    buff = []
    st = False
    lineCount = 0
    with codecs.open(mdFile, 'r', 'utf-8') as f:
        for i in f.readlines():
            if i.strip() == "---":
                lineCount += 1
            if i.strip() == "tags:":
                # タグの行がきた
                if not st:
                    # 次の行からTag扱い
                    st = True
            else:
                # タグの要素かもしれない
                if re.search("^- .*$", i.strip()):

                    if st:
                        if lineCount <= 1:
                            buff.append(i.strip().replace("- ", ""))
                else:
                    if st == True:
                        return buff
    return []


def create_pages(root_path):

    tags = []

    for root, dirs, files in os.walk(root_path):
        for file in files:
            path = os.path.join(root, file).replace("\\", "/")
            if os.path.splitext(path)[1] == ".md":
                tags += getTags(path)

    tags = list(set(tags))
    # ページを作る
    tagDir = os.getcwd() + "/docs/tags"
    os.makedirs(tagDir, exist_ok=True)
    for tag in tags:
        with open(f"{tagDir}/{tag}.md", 'w') as f:
            f.write(TAG_PAGE.format(tag=tag))


if __name__ == "__main__":
    create_pages(os.getcwd() + "/docs")
