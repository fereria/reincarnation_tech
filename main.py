def declare_variables(variables, macro):

    @macro
    def twitter(url):
        return f'<blockquote class="twitter-tweet"><a href="{url}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'

    @macro
    def fontstyle(comment, size=1.0, color='#000000'):
        return f'<div style="font-size:{size * 100}%;color:{color}">{comment}</div>'
