    public {{ class_name }}(){
        {% for array_attr in array_attributes %}
        this.{{array_attr.var}}= new ArrayList<{{array_attr.clss}}>();
        {% endfor %}
    }