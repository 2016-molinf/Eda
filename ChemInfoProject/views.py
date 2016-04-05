# views (=logika) pro chemoinfo django projekt

# importy
from django.http import HttpResponse
from django.shortcuts import render_to_response

#-----
import datetime

# funkce
# ------

def aktualni_cas(request):
    """ testovací funkce 1"""
    cas = datetime.datetime.now()
    html = "<html><body><h1>Nadpis<h2><p>Časová služba oznámí %s hodin.</p><h2>Nadpis 2</h2></body></html>" % cas
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
    
