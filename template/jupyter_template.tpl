{% extends 'markdown_base.tpl'%}

{% block header %}
{% endblock header %}


{% block markdowncell%}
{{cell.source}}
{% endblock markdowncell%}

{%- block input -%}
{% if cell.source != ""%}
```python
{{cell.source}}
```
{% endif %}
{%- endblock input -%}


{% block in_prompt %}
{% if cell.execution_count and cell.source != "" %}
#### In [{{ cell.execution_count}}]:
{% endif %}
{% endblock in_prompt %}

{% block stream %}
{% if cell.execution_count %}
!!! success
    ```
{{ super()}}
    ```
{% endif %}
{% endblock stream %}

{% block execute_result%}
{% if cell.execution_count %}
!!! success
    ```
{{ super()}}
    ```
{% endif %}
{% endblock execute_result%}

{% block error %}
!!! error
{{ super() }}
{% endblock error %}
