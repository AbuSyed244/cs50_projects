from django.shortcuts import render
from django import forms
from . import util
import markdown2
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import URLPattern
import random

def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')        
        search_entries = []
        entries = []
        for ent in util.list_entries():
            entries.append(ent.lower())
        if query.lower() in entries:
            return entry_display(request, query)
        for entry in entries:
            if query.lower() in entry:
                search_entries.append(entry.capitalize())
                entry =+ 1
            elif query.lower() not in entry:            
                entry =+ 1
        if len(search_entries) == 0:
            return render(request, 'encyclopedia/error.html', {
            'content':'Sorry, your search returned no entries.',
            'title':'No entries found'})
        else:
            return render(request, 'encyclopedia/search.html', {
            'content':search_entries,
            'title':'Search Results'})


def index(request):
    return render(request, 'encyclopedia/index.html', {'entries': util.list_entries()})


def entry_display(request, title):
    entries = []
    for ent in util.list_entries():
        entries.append(ent.lower())
    if title.lower() in entries:
        html_content = markdown2.markdown_path(f"entries/{title}.md")
        return render(request, 'encyclopedia/entry.html', {'title':title,
        'html_content':html_content})
    else:
        return render(request, "encyclopedia/error.html",{
            "title":"Page Not Found",
            "content": "Sorry, the requested URL cannot be found!"
        })


def newpage(request):
    entries = []
    for ent in util.list_entries():
        entries.append(ent.lower())
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        new_content = request.POST.get('new_content')
        
        if new_title.lower() not in entries:
            util.save_entry(new_title.title(), new_content)
            return entry_display(request, new_title)            
        else:
            return render(request, "encyclopedia/error.html", {
                "title": "Page not saved",
                "content": "Sorry, another page with the same name already exists!"                
            })        
    else:
        return render(request, 'encyclopedia/newpage.html', {'title': 'Create New Page'})

def edit(request, title):    
    ex_content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/editpage.html", {
            "title": title.title(),          
            "ex_content": ex_content
        })
    else:       
        edit_content = request.POST.get("edit_content")
        util.save_entry(title, edit_content.replace("\r", ""))
        return entry_display(request, title)

def random_page(request):    
    entries = []
    for ent in util.list_entries():
        entries.append(ent.lower())
    return entry_display(request, random.choice(entries))


