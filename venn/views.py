from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .Circle import Circle
from . import logicFuncs, makeVenn
import json


# Create your views here.

def about(request):
    return render(request, 'venn/about.html', {})

def index(request):
    context = {
        'userInput': None,
        'circles': None,
        'pixelData': None,
        'JSON': None,
    }

    if request.POST:
        for i in request.POST.keys():
            print(i + ": " + request.POST[i])
        context['userInput'] = request.POST['userInput']
        variables = []
        if request.POST['userInput']:
            variables = logicFuncs.getVars(request.POST['userInput'])
            sets = []
            for k in request.POST.keys():
                if 'set' in k:
                    print('here')
                    sets.append((k.split('_')[0],
                        list(map(lambda x: int(x.strip()), request.POST[k].split(',')))))
                    context[k] = request.POST[k]
            # sizes = list(map(lambda x: (x[0], len(x[1])), sets))
            try:
                venn = makeVenn.makeVenn(request.POST['userInput'], sets)
            except:
                return HttpResponseNotFound("Error. Please try again.")   
            context['circles'] = venn['circles']
            context['pixelData'] = venn['imgData']
            context['cardinalities'] = venn['cardinalities']
            context['final'] = venn['final'][1]
            context['finalCardinality'] = venn['final'][0]
            # print([c['circle'].getDict() for c in context['circles']])
            # context['JSON'] = json.dumps(context['circles'][0]['circle'].getDict())
            context['JSON'] = json.dumps([c['circle'].getDict() for c in context['circles']])


    return render(request, 'venn/venn.html', context)