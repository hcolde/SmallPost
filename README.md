# SmallPost（小贴吧）
<div>开发的目的：最近想谋求一份django的实习工作，但苦于在校期间没学习过django，故现学现卖，让简历上多一些内容。</div>
项目目前还没开发完成！

***

功能：
- [x] 注册
- [x] 登录
- [x] 发帖
- [x] 分页
- [x] 浏览帖子列表
- [x] 浏览帖子详情
- [ ] 编辑帖子
- [ ] 删除帖子
- [ ] 评论
- [ ] 点赞
- [ ] （搭建uwsgi+nginx）

虽然功能看起来不算多，但前后端一起做，一个人就显得有些吃力了，以至于花了几天的时间。

***

相关配置/框架：
* 后端：python3.6 django2.0 pipenv<br>
* 前端：bootstrap3 jquery2.1

***

项目大致说明：
* 游客（未登录状态）可查看帖子，但发帖，留言以及点赞等操作必须登录后才可进行。
* 为了防止统一账户多人使用，当用户登录后，在后端保存一个token值，在客户端设置一个cookie也将该值保存。当用户进行相关操作时，对比cookie中的token是否与后端保存的相等。
