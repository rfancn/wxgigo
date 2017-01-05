# 写在前面的话

如果大家觉得还好用的话，相信同样喜欢分享的你一定会记得去[**关系Go!**](http://www.guanxigo.com)帮忙点击下广告来支持项目的继续开发和运营哦！有时候我们一个微小不经意的举动，却是最好的肯定与支持，先谢谢了!

If you feels it is helpful, pls kindly support me by clicking AD in websiste [**guanxigo**](http://www.guanxigo.com) if you have free time, thanks in advance!

## wxgigo(Experimental)

The framework for developing private Tencent Wechat public platform

Currently it is under active development, no meaningful commit comments for all changes, as all may be reset in the future.

## Installation

1. Download and extract "dist" directory into any linux server
2. Edit "dist/config.ini" as you needed or leave it empty
3. Run `$ sh dist/setup.sh`

## Configuration

All configuration can be defined in config.ini, or you can leave empty for all configuration items and input it in interactive mode.
```
[DEFAULT]
ssh_host = The hostname or IP address of linux server to deploy on
ssh_user = The SSH username to access linux server
ssh_password = The SSH password to access linux server
wxgigo_home= The wxgigo project home, by default it is: /opt/wxgigo
deploy_user= The user/group for wxgigo project files

[HOST_WEIXIN]
Options to deploy Wechat server

[HOST_DB]
Options to deploy DB server

[HOST_APP]
Options to deploy App server

[SERVICE_NGINX]
server_name = 'server_name' defined in Nignx configuration
server_port = 'port' defined in Nginx configuration
static_dir = The static dir to accomandate HTTP static stuff, like js, image, css

[SERVICE_UWSGI]
process_num = uwsgi process number
thread_num = uwsgi thread number
```

> Note: You can override all options from DEFAULT section for Wechat/DB/App server in it's own section,
e,g: Deploy Wechat server in wechat.test.com, and deploy DB server in db.test.com:

```
[HOST_WEIXIN]
ssh_host = wechat.test.com
ssh_user = ryan
ssh_password = ******

[HOST_DB]
ssh_host = db.test.com
ssh_user = oracle
ssh_password = ******
```
