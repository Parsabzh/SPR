from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import component
from .data.engine.elastic_search import ElasticSearchManager


# def index(request):
# return HttpResponse("Hello, world. You're at the polls index.")


def input_view(request):
    return render(request, 'crs/form.html')


def result_view(request):
    features = [
        "Resource utilization", "Co-existence", "Installability", "Availability",
        "Authenticity", "Appropriateness recognizability", "User interface aesthetics",
        "Time behaviour", "Functional completeness", "Modifiability", "Learnability",
        "Recoverability", "Operability", "Modularity", "Maturity", "Functional correctness",
        "Confidentiality", "Functional appropriateness", "Adaptability", "Capacity",
        "Reusability", "Fault tolerance", "Integrity", "Accessibility", "User error protection",
        "Testability", "Analysability", "Interoperability", "Accountability",
        "Non-repudiation", "Replaceability"
    ]
    search = ElasticSearchManager()
    data = request.GET.get('require')
    response_bm25 = search.search("package_index", data)
    response_dfi = search.search_dfi("package_index", data)
    response_ib = search.search_ib("package_index", data)
    print(response_bm25)

    lst = []
    for item in response_bm25:
        lst.append(item["name"])
    print(lst)
    return render(request, 'crs/result.html', {'results': response_bm25, 'features': features})
