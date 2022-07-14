## rasa_backend

场景：rasa配置主要以yaml文件为主，在多机部署的时候有点不方便，model支持http存储但是官方没有给出详细的model服务端方法。

本项目支持：
1. model的http存储服务端；
2. 配置文件内容移植到mongo中，方便中心化管理；
3. model通过api训练，直接上传到http存储服务端，本地无需存储model文件。

使用方法：
1. http存储服务端和rasa客户端最好不要在一台机器上；
2. 进入model_server,修改nginx/conf.d/default.conf的your_server替换为服务端ip或者域名。执行docker-compose up -d；
3. 进入rasa_server,修改rasa_server/rasafront/config.py的recieve_url替换为http服务端或者域名。执行docker-compose up -d；
4. 测试数据上传的mongo：可以通过修改yaml2mongo.py脚本中文件路径进行上传（后续会改成接口方式）。测试数据参考《Rasa实战：构建开源对话机器人》中第三章的内容。

Todo：
- [ ] 前端界面暂时没有想好怎么做，所以对yaml的拆解比较简单，后续会补全。
- [ ] 管理端界面。
