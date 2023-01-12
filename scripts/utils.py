import os
import yaml
import codecs


def getGithubRoot():

    with codecs.open(os.getcwd() + "/mkdocs.yml", 'r', 'utf-8') as f:
        obj = yaml.safe_load(f)
        if 'repo_url' in obj:
            return obj['repo_url']
    return ""


def getFolderReplaceString():

    with codecs.open(os.getcwd() + "/mkdocs.yml", 'r', 'utf-8') as f:
        obj = yaml.safe_load(f)
        if 'replace_foldername' in obj:
            buff = {}
            for i in obj['replace_foldername']:
                buff.update(i)
            return buff
    return {}


def getHeaderYaml(path):
    """
    mdのヘッダーに書かれているYaml形式のメタデータをDictで取得する
    """

    with codecs.open(path, "r", 'utf-8') as f:
        lines = f.readlines()

    flg = False

    retVal = []

    for i in lines:
        if flg and i.strip() == "---":
            # 最後の ---
            break
        elif not flg and i.strip() == "---":
            # 最初の ---
            flg = True
        else:
            retVal.append(i.replace("\t", "    "))

    if len(retVal):
        if flg:
            return yaml.safe_load("".join(retVal))
    return None


def getMainDocs(path):

    with codecs.open(path, "r", 'utf-8') as f:
        lines = f.readlines()

    flg = 0

    docs = []

    for i in lines:
        i = i.strip()
        if i == "---":
            flg += 1
        else:
            if flg == 2:
                docs.append(i)

    return docs
