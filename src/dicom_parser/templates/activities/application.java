package {{ package }};

import {{ model_package }}.{{ report_class }};

import android.app.Application;

public class {{report_class}}_Application extends Application {

	private {{ report_class }} report;
	
	public {{ report_class }} get_report(){
		return report;
	}
	
	public void setReport({{ report_class }} report){
		this.report = report;
	}
	public void onCreate(){
		this.report = new {{ report_class }}();
	}
}
