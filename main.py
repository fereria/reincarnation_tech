import os
import os.path
import re
import codecs
from datetime import datetime
from git import Repo
from nbconvert import TemplateExporter, exporters
import nbformat
import utils

FUKIDASHI_HTML = """<div class="balloon5">
  <div class="faceicon">
    <img src="{icon}">
  </div>
  <div class="chatting">
    <div class="says">
      <p>{comment}</p>
    </div>
  </div>
</div>
"""


def returnHoge():
    return 'return hogehoge'


def define_env(env):

    def getTitle(md):
        if os.path.exists(md):
            with codecs.open(md, 'r', 'utf8') as f:
                for i in f.readlines():
                    if re.search("^title:", i):
                        return i.strip().split(":")[1]
        return None

    @env.macro
    def update_info(num, header="##"):

        repo = Repo(os.getcwd())
        msg = []
        for commit in repo.iter_commits('master', max_count=num):
            dt = datetime.fromtimestamp((commit.committed_date))
            buff = commit.message.split("\n")
            msg.append(f"{header} {dt.strftime('%Y-%m-%d %H:%M:%S')} {buff[0]}")
            msg.append("")
            if len(buff) > 2:
                # 更新コメントがちゃんと書いてあったら詳細を書く
                msg += buff[2:]
            # 更新ページ
            files = commit.stats.files.keys()
            count = len(files)
            if count > 5:
                # いっぱいあるときは省略する
                files = files[0:5]
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext == ".md":
                    if re.search("{.* => .*}", f):
                        # FilePathを移動したパターンの場合
                        buff = f.split("}")
                        buff2 = buff[0].replace("{", "").split(" => ")
                        f = buff2[1] + buff[1]
                        msg.append(f"{buff[1]} を {buff2[0]}から{buff2[1]} に移動\n")
                    link = re.sub("^docs/", "", f.replace("\\", "/"))
                    title = getTitle(os.getcwd() + "/" + f)
                    if not title:
                        title = link
                    msg.append(f"* [{title}]({link})")
            if count > 5:
                msg.append("...省略")
        return "\n".join(msg)

    @env.macro
    def fontstyle(comment, size=1.0, color='#000000'):
        return f'<div style="font-size:{size * 100}%;color:{color}">{comment}</div>'

    @env.filter
    def twitter(url):
        return f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'

    @env.filter
    def gist(gist_id, user='fereria'):
        return f'<script src="https://gist.github.com/{user}/{gist_id}.js"></script>'

    @env.filter
    def upper(x):
        return x.upper()

    @env.filter
    def img(path):
        return f"![]({utils.getGithubRoot()}/img/{path})"

    @env.macro
    def embedIpynb(ipynbPath, cells=None):
        # 引数のipynbをmarkdownに変換して返す
        path = os.getcwd() + "/" + ipynbPath  # root以下からのPathで指定
        if os.path.exists(path):
            try:
                with codecs.open(path, 'r', 'utf-8') as f:
                    lines = f.readlines()
                f = nbformat.reads("".join(lines), as_version=4)
                if cells:
                    # 表示したいCellが指定されてる場合
                    showCells = cells
                else:
                    # 指定がなければ全部表示
                    showCells = [int(x['execution_count'])
                                 for x in f.cells if 'execution_count' in x and x['execution_count'] is not None]

                buff = []
                for i in f.cells:
                    if 'execution_count' in i and i['execution_count']:
                        if int(i['execution_count']) in showCells:
                            buff.append(i)
                f.cells = buff
                exporter = TemplateExporter(template_file="template/embed_markdown.tpl")
                (body, reources) = exporter.from_notebook_node(f)

                buff = ["    " + x for x in body.split("\n") if x != ""]

                text = [f"!!! example \"\"",
                        *buff,
                        f"    :fa-bookmark: [{os.path.basename(ipynbPath)}]({utils.getGithubRoot()}/tree/master/{ipynbPath})"]
                return "\n".join(text)
            except Exception as f:
                import traceback
                return f"ConvertEerror!! ->{ipynbPath}\n{traceback.format_exc()}"
        else:
            return f"Not Found -> {ipynbPath}"

    @env.macro
    def fukidashi(comment, icon="default"):
        # 参考: https://saruwakakun.com/html-css/reference/speech-bubble
        path = {
            "remiria": "https://gyazo.com/a9c6c9adfb619505393a13240d010325.jpg",
            "default": "https://gyazo.com/3df214f13e2b6b8a4e903a0f9a3a35c0.png"
        }
        return FUKIDASHI_HTML.format(comment=comment, icon=path[icon])

    @env.macro
    def include(includeFilePath):

        path = os.getcwd() + "/docs/" + os.path.dirname(env.variables['page'].file.src_path) + "/" + includeFilePath
        if os.path.exists(path):
            with codecs.open(path, 'r', 'utf-8') as f:
                lines = []
                skip = False
                for i in f.readlines():
                    if "HEADER:START" in i:  # 指定文字列に挟まれている部分はスキップする
                        skip = True
                        continue
                    if "HEADER:END" in i:
                        skip = False
                        continue
                    if not skip:
                        lines.append(i)

                if os.path.splitext(path)[1] == ".py":
                    lines.insert(0, "```python\n")
                    lines.append("```\n")
                return "".join(lines)
        return path + " not found."

    env.macro('return hogehoge', 'hogevalue')

    @env.filter
    def green_badge(comment):
        return f'<span class="green-badge badge-all">{comment}</span>'

    @env.filter
    def blue_badge(comment):
        return f'<span class="blue-badge badge-all">{comment}</span>'

    @env.filter
    def macroprint(value):
        return "{{" + value + "}}"
