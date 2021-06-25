{% extends 'markdown_base.tpl'%}

{% block header %}
{% endblock header %}

# Markdownはそのまま表示
{% block markdowncell%}
{{ super() }}
{% endblock markdowncell%}

{% block in_prompt %}
{% if cell.execution_count %}
:fa-angle-double-right: In [{{ cell.execution_count }}]:
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
