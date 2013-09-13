package {{ package }};

{% for import in imports -%}
	{{import}}
{% endfor %}
public {{class_type}} {{ class_name }} {{ implements_class }}{

    {% for attribute in attributes -%}
        {{attribute}}
    {% endfor %}

    {% for method in methods -%}
        {{method}}
    {% endfor %}
}