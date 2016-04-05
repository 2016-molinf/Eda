# html templáty pro projekt

from django.http import HttpResponse

def main_page(request):
    main_page = """
<html>
<body>
<h1>Cheminfo projekt</h1>
<h2>Blablabla - n&aacute;zev:</h2>
<h3><em>Eda Ehler</em></h3>
<p>Popis aplikace a toho co děl&aacute;...</p>
<p>vysvětlin&iacute; hlavn&iacute;ch funkčn&iacute;ch celků...</p>
<p>Nějak&yacute; odkazy&nbsp;<a title="nevim" href="projekt.stranka1">odkaz1</a>,&nbsp;<a href="cas">zkouska - funkce cas</a>,&nbsp;<a href="scitani/4/5">zkouska pretty url funkce scitani</a>.</p>
<p>Funkčn&iacute; čudl&iacute;ky, kter&eacute; budou spou&scaron;tět vkl&aacute;d&aacute;n&iacute; do datab&aacute;ze a dal&scaron;&iacute; funkce.</p>
<table style="height: 19px;" width="463">
<tbody>
<tr>
<td style="text-align: center;"><span style="color: #ffffff; background-color: #008000;">button1</span></td>
<td style="text-align: center;"><span style="color: #ffffff; background-color: #008000;">button2</span></td>
<td style="text-align: center;"><span style="color: #ffffff; background-color: #008000;">button3</span></td>
<td style="text-align: center;"><span style="color: #ffffff; background-color: #008000;">button4</span></td>
<td style="text-align: center;"><span style="color: #ffffff; background-color: #008000;">button5</span></td>
</tr>
</tbody>
</body>
</html>
"""
    return HttpResponse(main_page)