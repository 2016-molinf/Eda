from django.db import models
from .functions import get_structure_image

# Create your models here.

class Molecule(models.Model):
    name = models.CharField(max_length=99, blank=True)
    timestamp = models.DateField(auto_now_add=True)         # předělat na DatetimeField
    smiles = models.CharField(max_length=300, default="test")
    inchi = models.CharField(max_length=300, blank=True)
    inchikey = models.CharField(max_length=50, blank=True)
    summary_formula = models.CharField(max_length=99, blank=True)
    mol_weight = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=3)   # max 999 999.999
    pic = models.ImageField(upload_to="/pics", blank=True)
    
    #mol_weight = 
    #toxicity = 
    deleted = models.BooleanField(default=False)     # dle doporučení z nějaké knížky, lepší nemazat, jen přepnout switch na True
                        # to co bych smazal už nedostanu - není "undo"
    
    def get_pic(self):
        pic = get_structure_image(self.smiles)
        return pic
    
    def insert_single(self, name="", smiles="", pic=""):
        pass
        
    def insert_multiple(self, source):
        pass
        
    
    def delete_selected(self, select_conditions=""):
        pass