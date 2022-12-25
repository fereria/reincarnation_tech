# -*- coding: utf-8 -*-

import os
import shutil
import codecs
import sys

from notion2md.exporter.block import MarkdownExporter
from notion_client import Client


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
        title = i['properties']['Name']['title'][0]['plain_text']
        tags = [x['name'] for x in i['properties']['Tags']['multi_select']]
        subdir = i['properties']['dir']['rich_text']
        description = i['properties']['description']['rich_text']

        if not i['properties']['publish']['checkbox']:
            # publishがFalseのものはファイルを作らない
            continue

        header = ["---"]
        header.append(f'title: {title}')
        if len(tags):
            header.append('tags:')
        for tag in tags:
            header.append(f"    - {tag}")
        if len(description):
            header.append(f"description: {description[0]['plain_text']}")
        header.append('---')

        outputPath = md_root

        if len(subdir):
            outputPath += "/" + subdir[0]['plain_text']

        MarkdownExporter(block_id=i['id'], output_path=outputPath, download=True, unzipped=True).export()

        markdownName = f"{outputPath}/{i['id']}.md"

        with codecs.open(markdownName, 'r', 'utf-8') as f:
            lines = [x + "\n" for x in header] + f.readlines()

        with codecs.open(markdownName, 'w', 'utf-8') as f:
            f.write("".join(lines))

        fname = i['properties']['filename']['rich_text']
        if len(fname):
            os.rename(markdownName, f"{outputPath}/{fname[0]['plain_text']}.md")


if __name__ == '__main__':

    os.environ['NOTION_TOKEN'] = sys.argv[1]
    os.environ['NOTION_DATABASE_ID'] = sys.argv[2]

    createNotionPages()
