# coding=utf-8
import os

from sdk.plugin.base import BasePlugin
from sdk.plugin import PROCESSING_MODE
from sdk.recv import RECV_CATEGORY, RECV_MSG_TYPE
from sdk.reply.factory import WXMPReplyShortcut
from plugins.forward2wp.wxhtml import WXHtml
from plugins.forward2wp.wp import WordPress
from sdk.plugin.config import BasePluginConfig, CharField
from plugins.forward2wp.transfer import Transfer

from sdk.api import Api

class PluginConfig(BasePluginConfig):
    # wordpress site information
    wp_username = CharField(label='WordPress Admin Username')
    wp_password = CharField(label='WordPress Admin Password', secure=True)
    wp_xmlrpc_url = CharField(label='WordPress XML RPC URL',
                              help_text='Complete XML RPC call URL(e,g: http://blog.test.com/xmlrpc.php)')

    # static server part
    ssh_host = CharField(label='SSH host', help_text='Static servers hostname or ip')
    ssh_port = CharField(label='SSH port', help_text='Server used to host static files')
    ssh_username = CharField(label='SSH username', help_text='SSH username to access static server')
    ssh_password = CharField(label='SSH password', help_text='SSH password to access static server', secure=True)

    static_root =  CharField(label='Static Root',
                            help_text='The root directory hosts static files, e,g: /var/www/html/static')
    static_url = CharField(label='Static URL',
                           help_text='The root url to access static files, e,g: http://x.x.x.x/pages/')

    def get_layout(self):
        layout = [
            {'WordPress Setting': [ 'wp_username', 'wp_password', 'wp_xmlrpc_url'] },
            {'Staic Server Setting': ['ssh_host', 'ssh_port', 'ssh_username', 'ssh_password', 'static_root', 'static_url']},
        ]

        return layout

class Plugin(BasePlugin):
    NAME = "Forward2WP"
    VERSION = "0.0.1"
    DESCRIPTION = "When receives article reply to Weixin Media Platform, forward it to workdpress site"
    AUTHOR = "Ryan Fan"
    WEBSITE = ""

    def is_matched(self, recv):
        if recv.category == RECV_CATEGORY.MESSAGE and recv.type == RECV_MSG_TYPE.LINK:
            print "Forward to wordpress matched!"
            return True

        return False

    def save(self, wxhtml):
        transfer = Transfer(self.config)

        # save WXHTML meta file
        meta = wxhtml.get_meta()
        transfer.save_content(meta['dir'], meta['filename'], meta['content'])

        # save html
        transfer.save_content(wxhtml.dir, wxhtml.filename, wxhtml.final_content)

        # save internal objects
        for obj in wxhtml.internal_objects:
            transfer.save_content(obj.dir, obj.filename, obj.get_content())

        transfer.close()

    def process(self, recv):
        print "foward2wp process url: {0}".format(recv.url)

        # process wxhtml
        wxhtml = WXHtml(recv.title, recv.url)
        wxhtml.process()

        # save wxhtml to static servers
        self.save(wxhtml)

        # new wordpress post to embed above html file in iframe
        wordpress = WordPress(self.config)
        src_html = os.path.join(self.config.static_url, wxhtml.dir, wxhtml.filename)
        content = '[advanced_iframe securitykey="a5bf057fa6484f8aa91052097420283a0deaa16e" src="{0}"]'.format(src_html)
        post_id = wordpress.new_post(recv.title, wxhtml.excerpt, content)

        # reply with result
        reply = WXMPReplyShortcut(recv).createServiceText("Successfully created new WordPress post: {0}".format(post_id))
        Api.send_service_reply(reply)

    def get_processing_mode(self):
        return PROCESSING_MODE.ASYNC


