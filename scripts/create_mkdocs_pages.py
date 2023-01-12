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

import utils

# 無視するフォルダ
EXCLUSION = [".git", ".vscode", ".history", "_book", "node_modules", "stylesheets", "javascripts", "__pycache__"]

# --------------------------------------------------------- #


def replace_title_folder_name(name):

    replaceString = utils.getFolderReplaceString()

    buff = re.sub("[0-9][0-9]_", "", name)
    buff = re.sub("_", " ", buff)
    for key in replaceString.keys():
        buff = buff.replace(key, replaceString[key])
    return buff


def create_pages(root_path):

    def recursive_file_check(path):

        if os.path.isdir(path):

            files = os.listdir(path)

            nav = []
            md = []

            for f in files:
                i = f"{path}/{f}"
                if os.path.isdir(i):
                    if len(glob.glob(i + "/*.md")) > 0:
                        nav.append(f"    - {f}")
                    elif len([x for x in os.listdir(i) if os.path.isdir(os.path.join(i, x))]):
                        nav.append(f"    - {f}")
                elif os.path.splitext(f)[1] == ".md":
                    md.append(f)

            # ソートする
            md_dict = {}
            for i in md:
                header = utils.getHeaderYaml(os.path.join(path, i))
                if header and 'order' in header:
                    md_dict[i] = header['order']
                else:
                    md_dict[i] = 9999

            if len(nav + md) > 0:
                nav.insert(0, 'nav:')

            for i in sorted(list(md_dict.keys()), key=lambda x: md_dict[x]):
                nav.append(f"    - {i}")

            # Folderのとき
            if root_path != path:
                dirname = path.split("/")[-1]
                if dirname not in EXCLUSION:
                    title = replace_title_folder_name(dirname)
                    nav.insert(0, f"title: {title}")
                    print(f"create .pages {path}/{dirname}")
                    with codecs.open(path + "/.pages", 'w', 'utf-8') as f:
                        f.write("\n".join(nav))

            for file in files:
                recursive_file_check(path + "/" + file)

    recursive_file_check(root_path)


if __name__ == "__main__":
    create_pages(os.getcwd() + "/docs")
