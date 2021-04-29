from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader, RequestContext
#from django_search import searchURLs
from Searcher import Searcher

def index(request):
    #context = {'result_list' : ['result 1', 'result 2', 'result 3'] , 'query' : 'climate related websites'}
    context = {}

    template = loader.get_template('search/index.html')
    requestContext = RequestContext(request, context)
    return  HttpResponse(template.template.render(requestContext))

def search(request):
    #query = request.POST['query']
    query = request.POST.get('query')

    if (query):
        searcher = Searcher()
        resultDict = searcher.searchURLs(request, query, 50)
    else:
        resultDict = {' ':[]}
        query = ' '
    
    context = {'result_list' : resultDict.get(query) , 'query' : query }
    template = loader.get_template("search/results.html") 
    requestContext = RequestContext(request, context)
    return HttpResponse(template.template.render(requestContext))
    #return render(request, 'search/results.html', context)

