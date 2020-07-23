import os
from datetime import datetime
from git import Repo


def returnHoge():
    return 'return hogehoge'


def define_env(env):

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

    env.macro('return hogehoge', 'hogevalue')

    @env.filter
    def macroprint(value):
        return "{{" + value + "}}"
