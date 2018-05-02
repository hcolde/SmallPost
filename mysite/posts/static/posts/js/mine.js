/*$("a[href='#Post']").bind("click", function() {
	$(this).unbind('click');
});*/

function FillIn(data, btn){
	$("div[class^='panel']").remove();
	var types = data.types;
	for(var i=0; i<data.title.length; i++){
		var title = data.title[i];
		var id = data.id[i];
		var date = data.date[i];
		var html = '<div class="panel panel-default"><div class="panel-heading" align="left">'+ date +'</div><div id="Operat"><span class="glyphicon glyphicon-edit" id="Edit" name="'+ id +'" value="'+ types +'"></span><span class="glyphicon glyphicon-remove" onclick="Remove('+ types +', '+ id +');"></span></div><div class="panel-body">'+ title +'</div></div>';
		if(btn=="POST")
			$("#Post").append(html);
		else
			$("#Comment").append(html);
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