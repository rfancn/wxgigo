from django import forms
from web.admin.config.models import WXMPConfig, MSG_ENCRYPT_METHOD

class ConfigForm(forms.ModelForm):
    msg_encrypt_method  = forms.ChoiceField(choices=MSG_ENCRYPT_METHOD, widget=forms.RadioSelect)

    class Meta:
        model = WXMPConfig
