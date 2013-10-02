
        children = SetChildren();
        {{ string_array }}_elist = (ExpandableListView) findViewById(R.id.list_{{ string_array }});
        adapter = new {{string_array}}_ListAdapter({{ activity_name }}.this,children);
        {{string_array}}_elist.setAdapter(adapter);