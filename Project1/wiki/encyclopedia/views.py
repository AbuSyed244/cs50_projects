from django.shortcuts import render
from django import forms
from . import util
import markdown2
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import URLPattern

def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        entries = []
        search_entries = []
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
            return render(request, 'encyclopedia/notfound.html', {
            'content':'Sorry, your search returned no entries.',
            'title':'No entries found'})
        else:
            return render(request, 'encyclopedia/search.html', {
            'content':search_entries,
            'title':'Search Results'})


def index(request):
    return render(request, 'encyclopedia/index.html', {'entries': util.list_entries()})


def entry_display(request, title):
    html_content = markdown2.markdown_path(f"entries/{title}.md")
    return render(request, 'encyclopedia/entry.html', {'title':title,
     'html_content':html_content})


def newpage(request):
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        new_content = request.POST.get('new_content')
        util.save_entry(new_title.title(), new_content)
        return entry_display(request, new_title)
    return render(request, 'encyclopedia/newpage.html', {'title': 'Create New Page'})