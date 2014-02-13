private void saveState(){

    {% if its_multiple %}

    {{ parent_class }} parent = report.{{ get_parent_class }};
    {{ model_class }} aux = new {{model_class}}();
    // EditText
    {%- for etext_id in etext_list %}
    etext_{{ etext_id }} = (EditText) findViewById(R.id.etext_{{etext_id}});
    aux.set_{{ etext_id }}(etext_{{ etext_id }}.getText().toString());
    {%- endfor %}
    parent.add_{{ add_to_parent }}

    {% else %}

    // EditText
    {%- for etext_id in etext_list %}
    etext_{{ etext_id }} = (EditText) findViewById(R.id.etext_{{etext_id}});
    report.set_{{ etext_id }}(etext_{{ etext_id }}.getText().toString());
    {%- endfor %}

    {% endif %}
}