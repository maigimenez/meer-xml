
        ListView listview_{{ string_array }} = (ListView) findViewById(R.id.list_{{ string_array }});
        String[] items = getResources().getStringArray(R.array.list_{{string_array}});
        ArrayAdapter<String> adapter_{{string_array}} = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, items);
        listview_{{string_array}}.setAdapter(adapter_{{string_array}});

        listview_{{ string_array }}.setOnItemClickListener(new OnItemClickListener() {
			public void onItemClick(AdapterView<?> adapterview, View view, int position, long id) {
				Toast.makeText(getApplicationContext(), 
						"Click ListItem Number " + position, Toast.LENGTH_LONG).show();
				Intent i = new Intent(getBaseContext(),Edit_radlex_rid29896_radlex_rid34261.class);
				startActivity(i);			
			}
		});