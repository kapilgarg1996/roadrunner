from django.shortcuts import render

# Create your views here.

def route_form(request):
    form = forms.RouteForm()

    return render(request, 'runner/routeform.html', {'form':form})


def get_stops(request):
    cursor = connection.cursor()
    sql = """select Stop.ID as id, Stop.NAME as name, Stop.CITY as city from Stop where Stop.ID != -1"""
    cursor.execute(sql)
    queryset = dictfetchall(cursor)
    #queryset = Stop.objects.raw(sql)
    result = StopSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['POST', 'GET'],)


def get_routes(request):
    source = request.POST['source']
    dest = request.POST['dest']
    time = request.POST['time']
    now = '2016-02-10 17:00:00'
    sql = ROUTE_SEARCH_QUERY
    queryset = Route.objects.raw(sql, (source, dest, now, time, time) )
    result = RouteSerializer(queryset, many=True)
    return Response(result.data)

@api_view(['GET'])

@api_view(['GET'])


def get_route_detail(request, id):
    cursor = connection.cursor()
    rid = id
    sql = ROUTE_DETAIL_QUERY
    cursor.execute(sql, (rid,))
    queryset = dictfetchall(cursor)
    #nqueryset = lower_keys(queryset)
    result = RouteDetailSerializer(queryset, many=True)
    return Response(result.data)

