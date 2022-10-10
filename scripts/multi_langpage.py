# -*- coding: utf-8 -*-
"""
headerに multi_lang:true がある場合は
指定の言語を生成する
"""

from venv import create
import utils
import yaml
import os.path
import os
import re
import codecs


def createHeader(data, lang):
    # headerから指定のLangのHeaderを生成する
    # 分離したDict型にする
    retVal = ['---']

    if lang == 'ja':
        for i in yaml.dump(data, allow_unicode=True).split("\n"):
            if i.strip() != "":
                retVal.append(re.sub("^- ", "    - ", i))
    else:
        if 'multi_lang' in data and lang in data['multi_lang']:
            for i in yaml.dump(data['multi_lang'][lang], allow_unicode=True).split("\n"):
                if i.strip() != "":
                    retVal.append(re.sub("^- ", "    - ", i))

    retVal.append("---")

    return retVal


def createMultiLangMd(path):

    data = utils.getHeaderYaml(path)
    docs = utils.getMainDocs(path)

    exportDocs = {'ja': createHeader(data, 'ja')}

    if data and 'multi_lang' not in data:
        # multi_langフラグがないものはなにもしない
        return
    elif data:
        for lang in data['multi_lang']:
            exportDocs[lang] = createHeader(data, lang)

    currentLang = None

    for i in docs:
        # 言語切り分けタグがあった場合の処理
        search = re.search("(<!---lang:)(.*)(--->)", i)
        if search:
            buff = search.groups()
            if buff[1] == "end":
                # endだったら、言語切り出しをやめる
                currentLang = None
            else:
                currentLang = buff[1]
        else:
            # 言語用タグ以外の行の場合
            if currentLang:
                # 指定言語がある場合かつ、multi_lang指定されている
                if currentLang in exportDocs:
                    exportDocs[currentLang].append(re.sub("\n$", "", i))
            else:
                # 言語指定がない場合、 exportDocsのすべての行に足す
                for l in exportDocs.keys():
                    exportDocs[l].append(re.sub("\n$", "", i))

    # 書き出し

    bn, ext = os.path.splitext(os.path.basename(path))
    dirName = os.path.dirname(path)

    for i in exportDocs.keys():
        with codecs.open(f"{dirName}/{bn}.{i}.md", 'w', 'utf-8') as f:
            f.write("\n".join(exportDocs[i]))


def create_pages(root_path):

    for root, dirs, files in os.walk(root_path):
        for file in files:
            path = os.path.join(root, file).replace("\\", "/")
            ext = os.path.splitext(path)[1]
            if ext == ".mdlang":
                print(path)
                createMultiLangMd(path)


if __name__ == '__main__':

    debug = False
    if debug:
        sampleFile = r"D:\docs\webpages\reincarnation_tech\docs\10_Programming\99_Documentation\mult_lang.mdlang"
        createMultiLangMd(sampleFile)
    else:
        create_pages(os.getcwd() + "/docs")
