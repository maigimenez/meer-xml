   private ArrayList<{{ container_class }}_Group> SetChildren() {
       ArrayList<{{ container_class }}_Group> children = new ArrayList<{{ container_class }}_Group>();
       String[] groups = getResources().getStringArray(R.array.list_{{ string_array }});
		
		for (int i=0;i<groups.length;i++){
			{{ container_class }}_Group child = new {{ container_class }}_Group();
			child.set_type(groups[i]);
			child.set_children(new ArrayList<{{ container_class }}_Children>());
			children.add(child);
		}
		
		return children;
	}