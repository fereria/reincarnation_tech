{% extends 'markdown.tpl'%}

{% block header %}
{% endblock header %}

# Markdownは表示しない
{% block markdowncell%}
{{cell.source}}
{% endblock markdowncell%}

{% block in_prompt %}
{% if cell.execution_count > 0%}
#### [{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endif %}
{% endblock in_prompt %}

{% block stream %}
!!! success
    ```
{{ super()}}
    ```
{% endblock stream %}

{% block execute_result%}
!!! success
    ```
{{ super()}}
    ```
{% endblock execute_result%}

{% block error %}
!!! error
{{ super() }}
{% endblock error %}
