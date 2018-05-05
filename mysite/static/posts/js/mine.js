function FillIn(data, btn){
	$("div[class^='panel']").remove();
	var types = data.types;
	for(var i=0; i<data.title.length; i++){
		var title = data.title[i];
		var id = data.id[i];
		var date = data.date[i];
		var edit = '<span class="glyphicon glyphicon-edit" onclick="Edit(' + id + ')"></span>';
		var remove = '<span class="glyphicon glyphicon-remove" onclick="Remove('+ types +', '+ id +');"></span>';
		var html_start = '<div class="panel panel-default"><div class="panel-heading" align="left">'+ date +'</div><div id="Operat">';
		var html_end = '</div><div class="panel-body">'+ title +'</div></div>';
		if(btn=="POST"){
			var html = html_start + edit + remove + html_end;
			$("#Post").append(html);
		}
		else{
			var html = html_start + remove + html_end;
			$("#Comment").append(html);
		}
	}
}

function Turn(btn,page){
	if(!page){
		btn.attr("style", "color:#ABABAB;");
		btn.attr("disable", "true");
	}else{
		btn.attr("style", "color:#000000;");
		btn.attr("disable", "false");
		btn.val(page);
	}
}