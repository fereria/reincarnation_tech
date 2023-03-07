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


def createGroupPages(dirs, titles, rootDir):

    createDir = f"{rootDir}"
    for d in dirs:
        createDir += f"/{d}"
        path = f"{createDir}/.pages"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(f'title: {titles[d]}')

    return createDir


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

    items = {}
    for i in db['results']:
        items[i['id']] = i

    # ディレクトリ階層を作る
    for i in db['results']:
        # ページItemを探す
        if len(i['properties']['subItem']['relation']) == 0 and i['properties']['publish']['checkbox']:
            dirs = []
            titles = {}
            parent = i['properties']['parentItem']['relation']
            while True:
                if len(parent) == 0:
                    break
                item = items[parent[0]['id']]
                dirname = item['properties']['dir']['rich_text'][0]['plain_text']
                dirs.insert(0, dirname)
                parent = item['properties']['parentItem']['relation']
                title = item['properties']['Name']['title'][0]['plain_text']
                titles[dirname] = title

            # # 子を持つGroupの場合、サブフォルダと .pages を作る
            mdSaveDir = createGroupPages(dirs, titles, md_root)
            createPage(i, mdSaveDir)


if __name__ == '__main__':

    os.environ['NOTION_TOKEN'] = sys.argv[1]
    os.environ['NOTION_DATABASE_ID'] = sys.argv[2]

    print('a')

    createNotionPages()
