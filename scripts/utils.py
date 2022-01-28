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
