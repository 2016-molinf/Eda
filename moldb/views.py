# views (=logika) pro chemoinfo django projekt

# importy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404

from django.db.models import Q      # slovník v ve funci search...?


#----- importy v rámci django projektu
from .models import Molecule
from .forms import MoldbInsertForm, MoldbSearchForm, UploadFileForm
from .functions import handle_uploaded_sdf, sdf_parser

#----- importy standardních knihoven používaných ve funkcích
import datetime
from rdkit import Chem
from rdkit.Chem import Draw

# funkce
# ------

def upload_sdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = handle_uploaded_sdf(request.FILES['file'], request.POST['title'])
            molecules_uploaded = sdf_parser(uploaded_file)
            return successful_upload('/successful_upload', {'molecules_uploaded' : molecules_uploaded} )
    else:
        form = UploadFileForm()
    return render(request, 'upload_sdf.html', {'form': form})


def moldb_insert(request):
    """ django formuláře (což jsou classy, které mám uložené ve forms.py) - insert do databáze """
    
    # validace vstupů:
    if request.method == 'POST':
        django_form = MoldbInsertForm(request.POST)
        # pokud platí, tak udělám novou instanci modelu Molecule a tu uložím
        if django_form.is_valid():
            new_name = django_form.cleaned_data['new_name']
            new_smiles = django_form.cleaned_data.get('new_smiles', '')
            new_summaryForm = django_form.cleaned_data.get('new_summaryForm', '')
            newInsertedMolecule = Molecule(name=new_name, smiles=new_smiles, summary_formula=new_summaryForm)
            newInsertedMolecule.save() 
            
    else:
        django_form = MoldbInsertForm()
        
    return render(request, 'moldb_insert.html', {'form': django_form})

def search(request):
    query = request.GET.get('q', '')
    # nejdřív testuju, jestli nechce všechno
    if query and query == "all":
        qset = Q(name__icontains="")
        results = Molecule.objects.filter(qset).distinct()
        
        return render_to_response("search.html", {"results" : results, "query": "all DBS objects"})
    # pak testuju, jakou že to query vlastně chce    
    if query:
        qset = (
        Q(name__icontains=query) |
        Q(smiles__icontains=query) |
        Q(summary_formula__icontains=query)
            )
        results = Molecule.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("search.html", {"results": results, "query": query})


def structure_image(request, id):
    mol_obj = get_object_or_404(Molecule, id=id)
    mol = Chem.MolFromSmiles(mol_obj.smiles)
    image = Draw.MolToImage(mol)
    response = HttpResponse(content_type="image/png")
    image.save(response,"PNG")
    return response    


def export_search_results(request):
    if request.method == 'POST':
        print(request)
    
#-----------------
def all_search(request):
    if request.method == 'POST':
        django_form = MoldbSearchForm(request.POST)
        # pokud platí, tak udělám novou instanci modelu Molecule a tu uložím
        if django_form.is_valid():
            seach_name = django_form.cleaned_data['search_name', '']
            seach_smiles = django_form.cleaned_data.get('seach_smiles', '')
            seach_summaryForm = django_form.cleaned_data.get('seach_summaryForm', '')
        
        # chaining filter objects!!! (https://docs.djangoproject.com/en/1.9/topics/db/queries/)
        #results = Molecule.objects.filter(co???).distinct()
        
    else:
        django_form = MoldbSearchForm()
    
    return render(request, 'all_search.html', {'form': django_form})
#----------------
    

def aktualni_cas(request):
    """ testovací funkce 1"""
    cas = datetime.datetime.now()
    html = """<html><body>
    <h2>==Under construction==</h2>
    <p>Not implemented yet, why don't you have a look at the current time instead...</p>
    <p>The current date and time is <b>%s.</b></p>
    <p><font size=2>See, you have got the date for free!!</font></p>
    </body></html>""" % cas
    
    
    return HttpResponse(html)
    
    
def scitani(request, prvni, druhy):
    """ testovací funkce 2 - parsování pretty url pomocí regexpu"""
    vysledek = int(prvni) + int(druhy)
    html = "<html><body>%s plus %s se rovná %s.</body></html>" % (prvni, druhy, vysledek)
    return HttpResponse(html)
    
def main_page(request):
    """ hlavní stránka - test složky templates, nastavení TEMPLATES_DIR v settings.py
    a django.shortcuts.render_to_response"""
    return render_to_response("main_page.html") # tady by mohl být i context ("main_page.html", Contex slovník)


def chemdoodle(request):
    """ stránka s chemdoodle java aplikací """
    return render_to_response("chemdoodle.html")
    
def jsme(request):
    """ stránka s jsme java aplikací """
    return render_to_response("jsme.html")

def successful_upload(request, context):
    return render_to_response("successful_upload.html", context)
