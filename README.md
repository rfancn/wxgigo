# 写在前面的话

如果大家觉得还好用的话，相信同样喜欢分享的你一定会记得去[**关系Go!**](http://www.guanxigo.com)帮忙点击下广告来支持项目的继续开发和运营哦！有时候我们一个微小不经意的举动，却是最好的肯定与支持，先谢谢了!

If you feels it is helpful, pls kindly support me by clicking AD in websiste [**guanxigo**](http://www.guanxigo.com) if you have free time, thanks in advance!

## wxgigo(Experimental)

The framework for developing applications with Tencent Wechat public platform or Wechat API

### Python compatibility

As most depended application needs at least Python2.7 or later

### Wechat Media Platform application workflow (Draw on https://textik.com/)
                          |-- Send Message ---|
                          |                   |
+--------+ Trigger Event  |-- Scan QRCode ----|     +---------------+
|  User  |--------------->|   ...             |---> | Weixin Server |
+--------+                |-- Click Menu  ----|     +---------------+
                          |                   |             ^
                          |                   |             |
                                                        XML Message
                                                            |
                                                            v
                         +--------------------------------------------------------------------+
                         |                          +-----------------+                       |
                         |  WXGIGO Agent Server     | Nginx or Apache |                       |
                         |                          +-----------------+                       |
                         |                                  ^                                 |
                         |                                  |                                 |
                         |                            WSGI Protocal                           |
                         |                                  |                                 |
                         |                                  v                                 |
                         |          +--------------------------------------------+            |
                         |          |                       |                    |            |
                         |          v                       v                    v            |
                         |  +-----------------+    +-----------------+   +-----------------+  |
                         |  |WSGI Application |    |WSGI Application |   |WSGI Application |  |
                         |  +-----------------+    +-----------------+   +-----------------+  |
                         |          |                       |                    |            |
                         |          |                       |                    |            |
                         |          +--------------------------------------------+            |
                         |                                  |                                 |
                         +----------------------------------|---------------------------------+
                                                            ^
                                                            |
                                                      AMQP Protocal
                                                            |
                                                            v
                                                 +----------------------+
                                                 |      AMQP Broker     |
                                                 +----------------------+
                                                            ^
                                                       AMQP |Protocal
                                                            v
                         +---------------------------------------------------------------------+
                         |  WXGIGO App Server               ^                                  |
                         |                       Msg1, Msg2, Msg3, ..., MsgN                   |
                         |                                  |                                  |
                         |                     Task1, Task2, Taks3,... TaskN                   |
                         |                                  |                                  |
                         |                                  |                                  |
                         |          Work1, Worker2 ........................ WorkerN            |
                         |                                                                     |
                         +---------------------------------------------------------------------+
                                                             ^
                                                             |
                                                             v
                         +---------------------------------------------------------------------+
                         | WXGIGO DB Server            Result Backend                          |
                         |                             (DB Or Cache)                           |
                         +---------------------------------------------------------------------+

### Server Roles
Based on workflow, there are three kinds of server role when deploying application for Weixin Media Platform,
Now I implements below setup, it will support more combination implemenation in the future:

1. Wxgigo Agent Server: nginx+ uwsgi + django app(wxgigo-agent)
2. Wxgigo App Server: wxgigo-appserver
3. Wxgigo DB Server: redis

Note:
* Wxgigo Agent Server only needed when developing application for Weixin Media Platform

## Switch to Develope mode
$ sudo python setup.py develop

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

