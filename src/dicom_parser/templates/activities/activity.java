package {{ package_name }};

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.app.Activity;

public class {{ activity_name }} extends Activity {

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{{ layout_file }});
        {% if childview is defined -%}
        {{ childview }}
        {% endif %}
    }

}
