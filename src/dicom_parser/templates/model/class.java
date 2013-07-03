{{ package }}

public class {{ class_name }} {
    {% for attribute in attributes -%}
        {{attribute}}
    {% endfor %}
}