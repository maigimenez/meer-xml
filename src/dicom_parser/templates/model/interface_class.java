package {{ package }};

{% for import in imports -%}
	{{import}}
{% endfor %}
public interface {{ class_name }} {

    {% for attribute in attributes -%}
        {{attribute}}
    {% endfor %}
}