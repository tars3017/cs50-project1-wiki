from django.shortcuts import render

from . import util

from markdown2 import markdown

from django import forms

class NewSearchForm(forms.Form):
    word = forms.CharField(label="search for")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_content(request, title):
    if (title in util.list_entries()):
        with open(f"entries/{title}.md") as f:
            s = f.read()   
            return render(request, "encyclopedia/show_page.html", {
                "page_title": title,
                "content": markdown(s)
            })
    return render(request, "encyclopedia/error.html")

def search(request):
    return render(request, "encyclopedia/search.html", {
        "form": NewSearchForm()
    })

