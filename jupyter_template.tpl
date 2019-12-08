{% extends 'markdown.tpl'%}

{% block header %}
{% endblock header %}

# Markdownは表示しない
{% block markdowncell%}
{% endblock markdowncell%}

{% block in_prompt %}
{% if cell.execution_count > 0%}
#### [{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endif %}
{% endblock in_prompt %}

{% block input%}
{% if cell.execution_count > 0 %}
{{ super() }}
{% endif %}
{% endblock input%}

{% block output %}
!!! info
    ```
{{ super() }}
    ```
{%- endblock output %}

