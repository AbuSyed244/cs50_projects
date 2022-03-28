import re
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from markdown import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def viewentry(request, entry):
    return render(request, "encyclopedia/viewentry.html", {
            "entry": markdown(util.get_entry(entry)),
            "entrytitle": entry
        })

def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        entries = []
        searchentries = []

        for ent in util.list_entries():
            entries.append(ent.lower())
        if query.lower() in entries:        
            redirect_url = f"/wiki/{query}"
            return redirect(redirect_url)
        else:
            for entry in entries:
                if query.lower() in entry:
                    searchentries.append(entry)
                    entry =+ 1
                elif query.lower() not in entry:
                    entry =+ 1
            if len(searchentries) == 0:
                return render(request, "encyclopedia/search.html", {
                    "message": "Sorry, no entries found!"
                })
            else:
                return render(request, "encyclopedia/search.html", {
                "searchentries": searchentries,
                "message": "Here are the search entries:"
                    })

def newentry(request):
    if request.method == 'POST':
        n_title = request.POST.get('n_title')
        n_cont = request.POST.get('n_cont')
        mdtitle = f"# {n_title}\n"

        if n_title in util.list_entries():
            return render(request, "encyclopedia/viewentry.html", {
                "entrytitle": "Page Already Exists!",
                "entry": "Sorry, but the page you're trying to create already exits!"
            })
        else:
            util.save_entry(n_title, mdtitle + n_cont)
            return viewentry(request, n_title)
    else:
        return render(request, "encyclopedia/newentry.html")


def error_404(request, exception):
    return render(request, "encyclopedia/viewentry.html",{
        "entry": "Sorry, your requested URL was not found!",
        "entrytitle": "Entry not found"
    })

def error_500(request):
    return render(request, "encyclopedia/viewentry.html",{
        "entry": "Sorry, an error occurred!",
        "entrytitle": "Error"
    })
    
        

