# django forms for Moldb database/model

from django import forms


"""
# can be used for multiple choise html form (menu)
TOPIC_CHOICES = (
                ('general', 'General enquiry'),
                ('bug', 'Bug report'),
                ('suggestion', 'Suggestion'),
                    )
"""

class MoldbInsertForm(forms.Form):
    #topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    new_name = forms.CharField(label="Name*")
    new_smiles = forms.CharField(required=False, label="SMILES")
    new_summaryForm = forms.CharField(required=False, label="Summary formula")
    
class MoldbSearchForm(forms.Form):
    search_name = forms.CharField(label="Name")
    search_smiles = forms.CharField(required=False, label="SMILES")
    search_summaryForm = forms.CharField(required=False, label="Summary formula")
    
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()