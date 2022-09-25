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
            # Folderのとき
            if root_path != path:
                dirname = path.split("/")[-1]
                if dirname not in EXCLUSION:
                    title = replace_title_folder_name(dirname)
                    print(f"create .pages {path}/{dirname}")
                    with codecs.open(path + "/.pages", 'w', 'utf-8') as f:
                        f.write(f"title: {title}")
            files = os.listdir(path)
            for file in files:
                recursive_file_check(path + "/" + file)

    recursive_file_check(root_path)


if __name__ == "__main__":
    create_pages(os.getcwd() + "/docs")
