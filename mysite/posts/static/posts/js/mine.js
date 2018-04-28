$("a[href='#Post']").bind("click", function() {
	$(this).unbind('click');
});

function FillIn(data){
	$("div[class^='panel']").remove();
	for(var i=0; i<data.title.length; i++){
		var title = data.title[i];
		var id = data.id[i];
		var date = data.date[i];
		var html = '<div class="panel panel-default"><div class="panel-heading" align="left">'+ date +'</div><div class="panel-body">'+ title +'</div></div>';
		$("#Post").append(html);
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