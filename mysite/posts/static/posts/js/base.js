//自动运行
window.onload = function(){ 
	var msg = getCookie("msg");
	if (msg=="100"){
		var nickName = getCookie("nickName");
		$("#Register").hide();
		$("#Login").hide();
		$("#Welcome").html("<a>"+nickName+"，欢迎您</a>");
		$("#Welcome").show();
		$("#Logout").show();
	}else if(msg!=""){
		switch(msg){
			case "001"||"010":
				alert("用户名或密码有误");
				break;
			case "011":
				alert("该用户名已被注册");
				break;
			case "101":
				alert("该昵称已被使用");
				break;
			case "110":
				alert("注册成功");
				break;
			case "000":
				alert("发帖失败，请检查该账号是否可用");
				break;
		}
		deleteCookie('msg');
	}
};

//获取cookie
function getCookie(name){
	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
};

//删除cookie
function deleteCookie(name){
	document.cookie=name+"=";
};

//退出登录
$("#Logout").click(function(){
	deleteCookie('msg');
	deleteCookie('nickName');
	deleteCookie('sex');
	deleteCookie('headPortrait');
	deleteCookie('token');
	$("#Welcome").hide();
	$("#Logout").hide();
	$("#Register").show();
	$("#Login").show();
});

//注册按钮
$("#Register").click(function(){
	//设置模态框标题
	$("#myModalLabel").html("<label>注册</label>");
	//隐藏所有警告提示
	$("p.alert").hide();
	//显示*号
	$("span.marked").show();
	//显示"重复输入"、"昵称"、"性别"、"头像"输入框
	$("#againGroup").show();
	$("#nickNameGroup").show();
	$("#sexGroup").show();
	$("#headPortraitGroup").show();
	//设置用户名、密码的占位符
	$("input[name='account']").attr("placeholder","以字母开头，由字母或数字组成的5-11个字符");
	$("input[name='password1']").attr("placeholder","由字母以及数字组成的8-18个字符");
	//post一个belong值，区分表单是注册还是登陆
	$("input[name='belong']").val("Register");
});

//登陆按钮
$("#Login").click(function(){
	//设置模态框标题
	$("#myModalLabel").html("<label>登录</label>");
	//隐藏所有警告提示
	$("p.alert").hide();
	//隐藏*号
	$("span.marked").hide();
	//显示"重复输入"、"昵称"、"性别"、"头像"输入框
	$("#againGroup").hide();
	$("#nickNameGroup").hide();
	$("#sexGroup").hide();
	$("#headPortraitGroup").hide();
	//取消用户名、密码的占位符
	$("input[name='account']").attr("placeholder","");
	$("input[name='password1']").attr("placeholder","");
	//post一个belong值，区分表单是注册还是登陆
	$("input[name='belong']").val("Login");
});

//提交按钮
$("#submit").click(function(){
	$("p.alert").hide();
	var account = $("input[name='account']").val();
	var password1 = $("input[name='password1']").val();
	var password2 = $("input[name='password2']").val();
	var nickName = $("input[name='nickName']").val();
	var sex = $("input:radio[name='sex']:checked").val();
	var isAccount = /^(?!\d+$)[a-zA-Z\d]{5,10}$/;
	var isPassword = /^(?!\d+$)(?![a-zA-Z]+$)[a-zA-Z\d]{8,18}$/;
	if ($("input[name='belong']").val() == "Login"){
		switch(false){
			//账号是否符合要求
			case isAccount.exec(account)!=null:
				$("p.alert").hide();
				$("p#accountAlert").show();
				break;
			//密码是否符合要求
			case isPassword.exec(password1)!=null:
				$("p.alert").hide();
				$("p#passwordAlert").show();
				break;
			default:
				$("p.alert").hide();
				$("#FormSubmit").click();
		}
	}else{
		switch(false){
			//账号是否符合要求
			case isAccount.exec(account)!=null:
				$("p.alert").hide();
				$("p#accountAlert").show();
				break;
			//密码是否符合要求
			case isPassword.exec(password1)!=null:
				$("p.alert").hide();
				$("p#passwordAlert").show();
				break;
			//两次输入的密码是否一致
			case password1==password2:
				$("p.alert").hide();
				$("p#againAlert").show();
				break;
			//昵称是否为空
			case nickName!="":
				$("p.alert").hide();
				$("p#nickNameAlert").show();
				break;
			//性别是否选择
			case sex!=undefined:
				$("p.alert").hide();
				$("p#sexAlert").show();
				break;
			//提交表单
			default:
				$("p.alert").hide();
				$("#FormSubmit").click();
		}
	}
});