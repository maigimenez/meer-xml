package {{ package }};

{% for import in imports -%}
	{{import}}
{% endfor %}
public class {{ class_name }} {

    {% for attribute in attributes -%}
        {{attribute}}
    {% endfor %}
}