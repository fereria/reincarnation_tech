{% extends 'markdown.tpl'%}

{% block header %}
{% endblock header %}

# Markdownはそのまま表示
{% block markdowncell%}
{% endblock markdowncell%}

{% block in_prompt %}
{% if cell.execution_count > 0%}
:fa-angle-double-right: {{ cell.execution_count if cell.execution_count else ' ' }}
{% endif %}
{% endblock in_prompt %}

{% block input %}
```python
{{cell.source}}
```
{% endblock input %}

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
    ```
{{ super()}}
    ```
{% endblock error %}