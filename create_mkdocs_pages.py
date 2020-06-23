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

# 日本語のIndexにしたいものは、フォルダ名から↓の名前に置換する
FOLDER_REPLACE_STRING = {
    "basic_operation": "基本操作",
    "data_structure": "データ構造",
    "terms": "用語",
    "modifier": "モディファイアの使い方",
    "back-to-top-button": "検証・考察",
    "study_materials": "NodeEditorマテリアル学習",
    "study_scripts_reading": "サンプルコード読んで学習",
    "imitate": "Houdini写経",
    "Env_Maya": "Maya作業環境構築",
    "PySide_Basic": "PySide_基本編",
    "python_module": "Pythonモジュールの使い方",
    "pipeline_study": "Pipeline/Workflow学習・考察",
    "defaultLib": "標準ライブラリ"

}

# 無視するフォルダ
EXCLUSION = [".git", ".vscode", ".history", "_book", "node_modules", "stylesheets", "javascripts"]

# --------------------------------------------------------- #


def replace_title_folder_name(name):

    buff = re.sub("[0-9][0-9]_", "", name)
    for key in FOLDER_REPLACE_STRING.keys():
        buff = buff.replace(key, FOLDER_REPLACE_STRING[key])
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
