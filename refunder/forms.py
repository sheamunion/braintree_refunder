from django import forms

class RefunderForm(forms.Form):
    ENV_CHOICES = (('production', 'Production',),('sandbox','Sandbox',))
    environment = forms.ChoiceField(widget=forms.RadioSelect, choices=ENV_CHOICES)
    merchant_id = forms.CharField(label='Merchant ID', max_length=32, widget=forms.PasswordInput())
    public_key  = forms.CharField(label='Public Key', max_length=64, widget=forms.PasswordInput())
    private_key = forms.CharField(label='Private Key', max_length=128, widget=forms.PasswordInput())
    source_csv  = forms.FileField()
