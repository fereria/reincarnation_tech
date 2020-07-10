
def returnHoge():
    return 'return hogehoge'


def define_env(env):
    @env.filter
    def twitter(url):
        return f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'

    @env.macro
    def fontstyle(comment, size=1.0, color='#000000'):
        return f'<div style="font-size:{size * 100}%;color:{color}">{comment}</div>'

    @env.filter
    def upper(x):
        return x.upper()

    env.macro('return hogehoge', 'hogevalue')

    @env.filter
    def macroprint(value):
        return "{{" + value + "}}"
