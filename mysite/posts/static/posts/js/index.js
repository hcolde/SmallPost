//发帖
$("#PostSubmit").click(function(){
	title = $("input[name='PostTitle']").val();
	patern = /^\s+$/;
	if (title=="" || title==undefined || patern.exec(title)){
		alert("请填写必填信息");
	}else{
		nickName = getCookie('nickName');
		if (nickName!=null && nickName!=""){
			$("form[name='PostForm']").submit();
		}else{
			alert("请登录后再发帖");
		}
	}
});