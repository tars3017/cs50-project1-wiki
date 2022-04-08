from django.shortcuts import render

from . import util

from markdown2 import markdown

from django import forms

from django.http import HttpResponseRedirect

class NewSearchForm(forms.Form):
    word = forms.CharField(label="Search for", widget=forms.TextInput(attrs={'class': 'search'}))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def load_content(request, title):
    if (title in util.list_entries()):
        with open(f"entries/{title}.md") as f:
            s = f.read()   
            return render(request, "encyclopedia/show_page.html", {
                "page_title": title,
                "content": markdown(s),
                "form": NewSearchForm()
            })
    return render(request, "encyclopedia/error.html", {"form": NewSearchForm})

def search(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["word"]
            print(keyword)

            if (keyword in util.list_entries()):
                with open(f"entries/{keyword}.md") as f:
                    s = f.read()
                    return render(request, "encyclopedia/show_page.html", {
                        "page_title": keyword,
                        "content": markdown(s),
                        "form": NewSearchForm()
                    })
            else:
                candidate_list = []
                for entry in util.list_entries():
                    if keyword in entry:
                        candidate_list.append(entry)
                if len(candidate_list):
                    return render(request, "encyclopedia/fuzzy_result.html", {
                        "page_title": "Search" + keyword,
                        "candidates": candidate_list,
                        "form": NewSearchForm()
                    })
    return render(request, "encyclopedia/search.html", {
        "form": NewSearchForm()
    })

