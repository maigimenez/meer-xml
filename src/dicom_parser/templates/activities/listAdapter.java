package {{ package_name }}

import java.util.ArrayList;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseExpandableListAdapter;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

{% for import in imports -%}
	{{import}}
{% endfor %}

public class {{string_array}}_ListAdapter extends BaseExpandableListAdapter {
	private Context context;	
	private ArrayList<{{ container_class }}_Group> groups;
	
	private static final int[] EMPTY_STATE_SET = {};
    private static final int[] GROUP_EXPANDED_STATE_SET =
            {android.R.attr.state_expanded};
    private static final int[][] GROUP_STATE_SETS = {
        EMPTY_STATE_SET, // 0
        GROUP_EXPANDED_STATE_SET // 1
	};
    
	public {{ string_array }}_ListAdapter (Context context, ArrayList<{{ container_class }}_Group> children){
		this.context = context;
		this.groups = children;
	}
	
	public long getChildId(int groupPosition, int childPosition) {
		return childPosition;
	}

	public Object getChild(int groupPosition, int childPosition) {
		ArrayList<{{ container_class }}_Children> children = groups.get(groupPosition).get_children();
		return children.get(childPosition);
	}

	public View getChildView(int groupPosition, int childPosition, boolean isLastChild, View convertView, ViewGroup parent) {
		View v = convertView;
		final {{ container_class }}_Children child = ({{ container_class }}_Children) getChild(groupPosition, childPosition);
		
		if (v == null){
			LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			v = inflater.inflate(R.layout.child, parent, false);
		}
		TextView tv = (TextView) v.findViewById(R.id.item_tv);
		tv.setText(child.get_snomed_ct_118522005());
		
		return v;
	}

	public int getChildrenCount(int groupPosition) {
		return groups.get(groupPosition).get_children().size();
	}

	public Object getGroup(int groupPosition) {
		return groups.get(groupPosition);
	}

	public int getGroupCount() {
		return groups.size();
	}

	public long getGroupId(int groupPosition) {
		return groupPosition;
	}

	public View getGroupView(final int groupPosition, boolean isExpanded, View convertView, ViewGroup parent) {
		View v = convertView;
		final {{ container_class }}_Group group = ({{ container_class }}_Group) getGroup(groupPosition);
		
		if (v == null){
			LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			v = inflater.inflate(R.layout.group, parent, false);
		}
		View expander = v.findViewById(R.id.explist_indicator);
		if (expander !=null){
			ImageView expander_button = (ImageView) expander;
			if (groupPosition==3){	
				expander_button.setVisibility(View.INVISIBLE);
			}
			else{
				expander_button.setVisibility(View.VISIBLE);
				int stateSetIndex =  ( isExpanded ? 1 : 0) ;
				Drawable drawable = expander_button.getDrawable();
				drawable.setState(GROUP_STATE_SETS[stateSetIndex]);
			}
		}
		TextView tv = (TextView) v.findViewById(R.id.group_tv);
		tv.setText(group.get_type());
		
		ImageButton add_button = (ImageButton) v.findViewById(R.id.add_group_button);
		add_button.setFocusable(false);
		
		if (groupPosition==3){	
			add_button.setOnClickListener(new ImageButton.OnClickListener() {
			    public void onClick(View v) {
			    	Toast.makeText(context, 
							"Add node type: " +Integer.toString(groupPosition), Toast.LENGTH_LONG).show();
			    	//context.startActivity(new Intent(context,DetailNodeActivity.class));

			    }
			});	
		}
		else{
			add_button.setOnClickListener(new ImageButton.OnClickListener() {
			    public void onClick(View v) {
			    	Toast.makeText(context, 
							"Caca: " +Integer.toString(groupPosition), Toast.LENGTH_LONG).show();
			    	//context.startActivity(new Intent(context,DetailNodeActivity.class));

			    }
			});	
		}
		return v;
	}

	public boolean hasStableIds() {
		// TODO Auto-generated method stub
		return true;
	}

	public boolean isChildSelectable(int arg0, int arg1) {
		// TODO Auto-generated method stub
		return true;
	}

}