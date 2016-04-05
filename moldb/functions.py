# pomocné funkce

# IMPORTY
from datetime import datetime as dt

from rdkit import Chem
from rdkit.Chem import AllChem

from rdkit.Chem import Draw
#-----------
from .models import Molecule


# FUNKCE
#-------

# nahrání sdf souboru
def handle_uploaded_sdf(soubor, titul):
    cas = dt.strftime(dt.now(), '%Y_%m_%d_%H.%M.%S')
    kam = 'moldb/upload/up_' + titul + '_' + cas + '.sdf'
    with open(kam, 'wb+') as destination:
        for chunk in soubor.chunks():
            destination.write(chunk)
        print("file saved")
    return kam
        
# vytvoření obrázku
def structure_image(request, id):
    mol_obj = get_object_or_404(Structure, id=id)
    mol = Chem.MolFromSmiles(str(mol_obj.mol))
    image = Draw.MolToImage(mol)
    response = HttpResponse(content_type="image/png")
    image.save(response,"PNG")
    return response

# zpracování nahraných multi sdf souborů    
def sdf_parser(soubor):
    mol_counter = 0
    suppl = Chem.SDMolSupplier(soubor)
    for mol in suppl:
        if mol is None: continue
        print(mol.GetNumAtoms())
        mol_counter += 1
        new_inchi = Chem.MolToInchi(mol)
        new_inchikey = Chem.InchiToInchiKey(new_inchi)
        # kontrola jestli je molekula již v databázi dle inchikey - ten by měl být unikátní
        
        if Molecule.objects.filter(inchikey=new_inchikey).exists():
            print(mol, "already exists")
        
        else:
            new_smiles = Chem.MolToSmiles(mol)
            new_summaryForm = AllChem.CalcMolFormula(mol)
            new_molweigth = AllChem.CalcExactMolWt(mol)
            
            if mol.HasProp('PUBCHEM_SUBSTANCE_SYNONYM'):
                new_name = mol.GetProp('PUBCHEM_SUBSTANCE_SYNONYM').split("\n")[0]
            
            
            newInsertedMolecule = Molecule(name=new_name, 
                                           smiles=new_smiles, 
                                           mol_weight=new_molweigth, 
                                           inchi=new_inchi, 
                                           inchikey=new_inchikey, 
                                           summary_formula=new_summaryForm)
            newInsertedMolecule.save()
        
        """
        new_name = django_form.cleaned_data['new_name']
        new_smiles = django_form.cleaned_data.get('new_smiles', '')
        new_summaryForm = django_form.cleaned_data.get('new_summaryForm', '')
        newInsertedMolecule = Molecule(name=new_name, smiles=new_smiles, summary_formula=new_summaryForm)
        newInsertedMolecule.save()
        """
        
        # ulož do databáze, naparsuj atd.
    #mols = [x for x in suppl]
    return mol_counter


def get_name_from_sdf(soubor):
    pass
     