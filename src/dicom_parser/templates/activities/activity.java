package {{ package_name }};


{% for import in imports -%}
	{{import}}
{% endfor %}

import android.os.Bundle;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;
import android.app.Activity;
import android.widget.Toast;
import android.view.View;
import android.content.Intent;
import android.widget.Spinner;

public class {{ activity_name }} extends Activity {

    {%- for spinner_id in spinners %}
        private Spinner spinner_{{spinner_id}};
    {%- endfor %}

    {%- if childview -%}
       {{ attributes }}
    {%- endif %}

    {% for etext_id in etext_list %}
    private EditText etext_{{etext_id}}; 
    {%- endfor %}

    private {{ app_classname }} app = null;
    private {{ report_classname }} report = null;

    public void onCreate(Bundle savedInstanceState) {
        // Get global app shared variable. 
        app = ({{app_classname}}) getApplication();
        report = app.get_report();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.{{ layout_file }});
        {% if childview -%}
        {{ childview }}
        {% endif -%}

        // Spinners 
        {% for spinner_id in spinners %}
		ArrayAdapter<CharSequence> adapter_{{ spinner_id }} = ArrayAdapter.createFromResource(
		    this, R.array.list_RID5958, android.R.layout.simple_spinner_item);
        spinner_{{spinner_id}} = (Spinner) findViewById(R.id.spinner_{{spinner_id}});
        adapter_{{ spinner_id }}.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
         
        spinner_{{spinner_id}}.setAdapter(adapter_{{ spinner_id }});
        {% endfor -%}

        // EditText
        {% for etext_id in etext_list %}
        etext_{{etext_id}} = (EditText) findViewById(R.id.etext_{{etext_id}});
        etext_{{etext_id}}.setOnClickListener(
                      new View.OnClickListener() {
                          public void onClick(View v) {
                          }
                      });
        {% endfor %}
    }

    {% if childview %}
{{ setChildren }}
    {% endif %}

}
