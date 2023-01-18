# -*- coding: utf-8 -*-

import os
import shutil
import codecs
import sys
import copy

from notion2md.exporter.block import MarkdownExporter
from notion_client import Client


def getParentItem(parentId):

    notion = Client(auth=os.environ['NOTION_TOKEN'])
    return notion.pages.retrieve(parentId)


def createGroupPages(data, rootDir):

    dirName = data['properties']['dir']['rich_text']

    if len(dirName) == 0:
        # ルートの場合はなにもしない
        return

    title = data['properties']['Name']['title'][0]['plain_text']

    path = f"{rootDir}/{dirName[0]['text']['content']}/.pages"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f'title: {title}')


def createPage(data, outputPath):
    # 引数の dataをもとにMarkdownのページを作る

    title = data['properties']['Name']['title'][0]['plain_text']
    tags = [x['name'] for x in data['properties']['Tags']['multi_select']]
    subdir = data['properties']['dir']['rich_text']
    description = data['properties']['description']['rich_text']

    # Markdownのヘッダに追加する文字列を作る
    header = ["---"]
    header.append(f'title: {title}')
    header.append('tags:')
    header.append(f"    - NotionMemo")
    for tag in tags:
        header.append(f"    - {tag}")
    if len(description):
        header.append(f"description: {description[0]['plain_text']}")
    header.append('---')

    savePath = copy.deepcopy(outputPath)

    p = data['properties']['parentItem']['relation']

    if len(p) > 0:
        parentData = getParentItem(p[0]['id'])
        dirName = parentData['properties']['dir']['rich_text']
        if len(dirName) > 0:
            savePath = savePath + "/" + dirName[0]['text']['content']

    print(savePath)

    if len(subdir) > 0:
        savePath = savePath + "/" + subdir[0]['text']['content']

    MarkdownExporter(block_id=data['id'], output_path=savePath, download=True, unzipped=True).export()

    markdownName = f"{savePath}/{data['id']}.md"

    with codecs.open(markdownName, 'r', 'utf-8') as f:
        lines = [x + "\n" for x in header] + f.readlines()

    with codecs.open(markdownName, 'w', 'utf-8') as f:
        f.write("".join(lines))

    fname = data['properties']['filename']['rich_text']
    if len(fname):
        os.rename(markdownName, f"{savePath}/{fname[0]['plain_text']}.md")


def createNotionPages():

    md_root = f"{os.getcwd()}/docs/70_Memo"

    # ファイルは作り直し
    if os.path.exists(md_root):
        shutil.rmtree(md_root)
    os.makedirs(md_root)

    notion = Client(auth=os.environ['NOTION_TOKEN'])

    # markdown化したいページを取得
    db = notion.databases.query(
        **{
            'database_id': os.environ['NOTION_DATABASE_ID']
        }
    )

    for i in db['results']:

        if len(i['properties']['subItem']['relation']):
            # 子を持つGroupの場合、サブフォルダと .pages を作る
            createGroupPages(i, md_root)

        if not i['properties']['publish']['checkbox']:
            # publishがFalseのものはファイルを作らない
            continue

        createPage(i, md_root)


if __name__ == '__main__':

    debug = True

    os.environ['NOTION_TOKEN'] = sys.argv[1]
    os.environ['NOTION_DATABASE_ID'] = sys.argv[2]

    createNotionPages()
