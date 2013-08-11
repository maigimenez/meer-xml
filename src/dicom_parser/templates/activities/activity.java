package {{ package_name }};

{#  TODO: Handle imports properly 
	{% for import in imports -%}
		{{import}}
	{% endfor %}
#}
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

    {% for spinner_id in spinners %}
        private Spinner spinner_{{spinner_id}};
    {% endfor %}

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{{ layout_file }});
        {% if childview is defined -%}
        {{ childview }}
        {% endif %}
        {% for spinner_id in spinners %}
			ArrayAdapter<CharSequence> adapter_{{ spinner_id }} = ArrayAdapter.createFromResource(
				this, R.array.list_RID5958, android.R.layout.simple_spinner_item);
        		spinner_{{spinner_id}} = (Spinner) findViewById(R.id.spinner_{{spinner_id}});
        		adapter_{{ spinner_id }}.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
         
        		spinner_{{spinner_id}}.setAdapter(adapter_{{ spinner_id }});
        {% endfor %}
    }

}
