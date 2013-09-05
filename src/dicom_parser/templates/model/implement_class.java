package {{ package }};

{% for import in imports -%}
	{{import}}
{% endfor %}
public class {{ class_name }} implements {{ parent_class }}{

    {% for attribute in attributes -%}
        {{attribute}}
    {% endfor %}

    {% for method in methods -%}
        {{method}}
    {% endfor %}
}