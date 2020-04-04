#!python3.6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
# -*- coding: utf-8 -*-

import os
import os.path
import re
import codecs
import yaml
import glob

# 定数
GITBOOK_ROOT = u"C:/reincarnation_tech"
GITBOOK_DOCS = GITBOOK_ROOT + u"/docs"
MKDOCS       = "mkdocs.yml"
MKDOCS_BASE  = "mkdocs_base.yml"

# 日本語のIndexにしたいものは、フォルダ名から↓の名前に置換する
FOLDER_REPLACE_STRING = {
    "basic_operation": u"基本操作",
    "data_structure": u"データ構造",
    "terms": u"用語",
    "modifier": u"モディファイアの使い方",
    "back-to-top-button": u"検証・考察",
    "study_materials": u"NodeEditorマテリアル学習",
    "study_scripts_reading": u"サンプルコード読んで学習",
    "imitate": u"Houdini写経",
    "Env_Maya": u"Maya作業環境構築",
    "PySide_Basic": u"PySide_基本編",
    "python_module": u"Pythonモジュールの使い方",
    "pipeline_study": "Pipeline/Workflow学習・考察"

}

# 無視するフォルダ
EXCLUSION = [".git", ".vscode", ".history", "_book", "node_modules", "stylesheets", "javascripts"]

# --------------------------------------------------------- #


def get_mkdocs_yml():

    # Jsonのように扱える
    with codecs.open(MKDOCS_BASE, 'r', 'utf-8') as file:
        return "".join(file.readlines())


def has_markdown(path):
    """
    指定フォルダ以下にMarkdownファイルが存在する場合Trueを返す
    """
    buff = glob.glob(path + u"/*.md")
    if len(buff) == 0:
        if len(os.listdir(path)) == 0:
            return False
    return True


def is_exclusion_path(path):
    # 除外ファイルの場合Trueを返す
    for i in EXCLUSION:
        if re.search("/" + i, path) is not None:
            return True
    return False


def get_summary_word(path):
    """
    引数のPathのMarkdownファイルにあるサマリー用の名前を取得する
    """
    print(path)
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()

    # サマリーのタイトル名の行を取得する
    for i in lines:
        if re.search('<!--.*SUMMARY:.*-->', i) is not None:
            buff = i
            for j in ["<!--", "-->", " "]:
                buff = buff.replace(j, "")
            buff = buff.split(":")
            return buff[1].strip()
    return ""


def isWriting(path):
    """
    書き途中か調べる
    """
    with codecs.open(path, 'r', 'utf-8') as f:
        lines = f.readlines()
    for i in lines:
        if re.search('<!--WRITING_NOW-->', i) is not None:
            return True
    return False


def replace_title_folder_name(name):

    buff = name
    for key in FOLDER_REPLACE_STRING.keys():
        buff = buff.replace(key, FOLDER_REPLACE_STRING[key])
    return buff


def create_pages(summary_path, root_path, indent_space="  "):

    write_val = ["nav:", indent_space + u"- 更新履歴: update_log.md", indent_space + u"- Markdownサンプル: md_sample.md"]

    def recursive_file_check(path):

        if os.path.isdir(path):
            # Folderのとき
            if root_path != path:
                gb_path = path.replace("\\", "/").replace(root_path + "/", "")
                # プリント処理
                if has_markdown(path):
                    buff    = gb_path.split("/")
                    indent  = (len(buff)) * indent_space
                    if is_exclusion_path(path) is False:
                        write_val.append(indent + "- " + replace_title_folder_name(re.sub("^[0-9][0-9]_", "", buff[-1])) + ":")
                        if os.path.exists(path + "/index.md"):
                            write_val.append(indent + "  - " + buff[0] + "/index.md")

            files = os.listdir(path)
            for file in files:
                recursive_file_check(path + "/" + file)
        else:
            bn, ext = os.path.splitext(os.path.basename(path))
            if ext == ".md":
                if bn != "SUMMARY" and bn != "index":
                    relative_path = path.replace("\\", "/").replace(root_path + "/", "")
                    buff = relative_path.split('/')
                    summary_keyword = get_summary_word(path)
                    if not isWriting(path):
                        if summary_keyword == "":
                            write_val.append((len(buff)) * indent_space + u"- {0}".format(relative_path))
                        elif is_exclusion_path(path) is False:
                            if len(relative_path.split("/")) > 1:
                                write_val.append((len(buff)) * indent_space + u"- {0}: {1}".format(summary_keyword, relative_path))

    recursive_file_check(root_path)

    yml_base = get_mkdocs_yml()
    yml_base = yml_base + "\n".join(write_val)

    with codecs.open(MKDOCS, 'w+', "utf-8") as f:
        f.write(yml_base)


if __name__ == "__main__":
    create_pages(GITBOOK_ROOT,
                 GITBOOK_DOCS)