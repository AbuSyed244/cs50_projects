import re
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from markdown import markdown

from . import util

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def viewentry(request, entry):

    try:
        return render(request, "encyclopedia/viewentry.html", {
                "entry": markdown(util.get_entry(entry)),
                "entrytitle": entry
            })
    except:
        return render(request, "encyclopedia/viewentry.html", {
            "entry": "Sorry, the page you requested does not exist!",
            "entrytitle": "Page Not Found"
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
                "message": "Are you looking for:"
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
        return render(request, "encyclopedia/modifyentry.html", {
            "label": "Create a new entry",
            "title_label": "Name Your Article:",
            "cont_label": "Write a Description:"
        })

def editpage(request, entry):

    if request.method == 'POST':
        e_cont = request.POST.get('n_cont')
        
        util.save_entry(entry, bytes(e_cont, 'utf8'))
        return viewentry(request, entry)
    
    else:

        return render(request, "encyclopedia/modifyentry.html", {
            "label": "Edit Page",
            "title_label": "Rename Article:",
            "cont_label": "Modify Content:",
            "e_title": entry,
            "e_content": util.get_entry(entry)                 
        })

def randompage(request):
    
    entries = []
    for ent in util.list_entries():
        entries.append(ent.lower())
    
    return viewentry(request, random.choice(entries))


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
    
        

