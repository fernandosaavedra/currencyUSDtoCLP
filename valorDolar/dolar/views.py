from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dolar.models import Dolar
from dolar.serializers import DolarSerializer, ClpSerializer
import time
from bs4 import BeautifulSoup as bs
import requests


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def populate_db(request):
    """
    Pobla la base de datos desde el SII
    """
    if request.method == 'POST':
        # Tomamos los años disponibles del SII
        anos = [
            '1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
            '2010','2011','2012','2013','2014','2015','2016','2017','2018'
        ]
        # Recorremos los años
        for ano in anos:
            # Hacemos una request hacia el url del SII
            # Si el año es menor a 2013, se ejecuta la base http://www.sii.cl/pagina/valores/dolar/dolar'+ano+'.htm
            if ano < '2013':
                url = 'http://www.sii.cl/pagina/valores/dolar/dolar'+ano+'.htm'
                r = requests.get(url)
                soup = bs(r.text, "html.parser")
                rows = soup.findAll('tr')
            elif ano <= '2018':
                url = 'http://www.sii.cl/valores_y_fechas/dolar/dolar'+ano+'.htm'
                r = requests.get(url)
                soup = bs(r.text, "html.parser")
                div = soup.find("div", {"id": "mes_all"})
                rows = div.findAll('tr')
            i = 0
            for row in rows:
                j = 1
                if i > 0 and i < 32:
                    cols = row.findAll('td')
                    for col in cols:
                        # Asignamos valor a mes y día
                        month = '0'+str(j) if j < 10 else str(j)
                        day = '0'+str(i) if i < 10 else str(i)
                        valor = col.text.replace('\xa0','')
                        valor = valor.replace('>Â','')
                        if valor != '':
                            valor = float(valor.replace(",","."))
                            fecha = ano+month+day
                            if Dolar.objects.filter(date=fecha).exists() == False:
                                dolar = Dolar(date=fecha, value=valor)
                                dolar.save()
                        j = j+1
                        valor = ''
                i = i+1
        # Se retorna la respuesta si nada falla
        return HttpResponse('{"code":200,"status":"success","message":"Funciona impeque!"}',status=200,content_type="application/json")
    else:
        # De lo contrario, se retorna error
        return HttpResponse('{"code":401,"status":"error","message":"Petición HTTP no existente."}',status=404,content_type="application/json")

@csrf_exempt
def dolar_a_clp(request):
    """
    Cambia el valor desde dolar a CLP
    """
    date = request.GET.get('date','')

    if date == '':
        try:
            ultimoValorDolar = Dolar.objects.latest('date')
            date = ultimoValorDolar.date
        except Dolar.DoesNotExist:
            return HttpResponse('{"code":420,"status":"error","message":"No hay ningún campo de fecha. Por favor ingresarlo en formato YYYYmmdd"}',status=404,content_type="application/json")

    # El largo de la fecha no puede ser mayor a 8 al ser YYYYMMDD
    if len(date) != 8:
        return HttpResponse('{"code":410,"status":"error","message":"El campo date, debe tener un string de largo 8 correspondiente a la fecha en formato YYYYmmdd."}',status=404,content_type="application/json")

    # El campo date no puede ser mayor a la fecha de hoy
    currentDate = time.strftime("%Y%m%d")
    if date < '19910101' or date > currentDate:
        return HttpResponse('{"code":412,"status":"error","message":"El campo date, no puede ser superior a la fecha de hoy."}',status=404,content_type="application/json")

    # Tomamos el objeto de dolar, capturando la fecha
    try:
        dolar = Dolar.objects.get(date=date)
    except Dolar.DoesNotExist:
        return HttpResponse('{"code":411,"status":"error","message":"Valor del Dolar no encontrado"}',status=404,content_type="application/json")

    try:
        dolar.usd = int(request.GET.get('usd', 100))
    except ValueError:
        return HttpResponse('{"code":415,"status":"error","message":"La cantidad de dólares debe ser un valor entero"}',status=404,content_type="application/json")

    if request.method == 'GET':
        serializer = DolarSerializer(dolar)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse('{"code":401,"status":"error","message":"Petición HTTP no existente."}',status=404,content_type="application/json")

@csrf_exempt
def clp_a_dolar(request):
    """
    Retrieve, update or delete a serie.
    """
    date = request.GET.get('date','')

    if date == '':
        try:
            ultimoValorDolar = Dolar.objects.latest('date')
            date = ultimoValorDolar.date
        except Dolar.DoesNotExist:
            return HttpResponse('{"code":420,"status":"error","message":"No hay ningún campo de fecha. Por favor ingresarlo en formato YYYYmmdd"}',status=404,content_type="application/json")

    if date == '':
        return HttpResponse('{"code":420,"status":"error","message":"No hay ningún campo de fecha. Por favor ingresarlo en formato YYYYmmdd"}',status=404,content_type="application/json")

    # El largo de la fecha no puede ser mayor a 8 al ser YYYYMMDD
    if len(date) != 8:
        return HttpResponse('{"code":410,"status":"error","message":"El campo date, debe tener un string de largo 8 correspondiente a la fecha en formato YYYYmmdd."}',status=404,content_type="application/json")

    # El campo date no puede ser mayor a la fecha de hoy
    currentDate = time.strftime("%Y%m%d")
    if date < '19910101' or date > currentDate:
        return HttpResponse('{"code":412,"status":"error","message":"El campo date, no puede ser superior a la fecha de hoy."}',status=404,content_type="application/json")

    # Tomamos el objeto de dolar, capturando la fecha
    try:
        dolar = Dolar.objects.get(date=date)
    except Dolar.DoesNotExist:
        # Si no existe, retornamos una respuesta de error
        return HttpResponse('{"code":411,"status":"error","message":"Valor del Dolar no encontrado"}',status=404,content_type="application/json")

    # Añadimos al objeto dolar el valor en pesos a transformar
    try:
        dolar.clp = int(request.GET.get('clp', 100))
    except ValueError:
        return HttpResponse('{"code":416,"status":"error","message":"El valor en pesos debe ser un valor entero"}',status=404,content_type="application/json")

    if request.method == 'GET':
        serializer = ClpSerializer(dolar)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse('{"code":401,"status":"error","message":"Petición HTTP no existente."}',status=404,content_type="application/json")
