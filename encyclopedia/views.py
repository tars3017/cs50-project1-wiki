from django.shortcuts import render

from . import util

from markdown2 import markdown

from django import forms

from django.http import HttpResponseRedirect

from django.utils.safestring import mark_safe

from django.urls import reverse

import random

class NewSearchForm(forms.Form):
    word = forms.CharField(label="Search for", widget=forms.TextInput(attrs={'class': 'search'}))

class AddPageForm(forms.Form):
    page_title = forms.CharField(label=mark_safe("Title"))
    content = forms.CharField(label="Page content", widget=forms.Textarea() )
    

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
    return render(request, "encyclopedia/error.html", {
        "form": NewSearchForm, 
        "error_msg": "Error! Page not found"
    })

def search(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["word"]
            # print(keyword)

            if keyword in util.list_entries():
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

def new_page(request):
    print(request)
    if request.method == 'POST':
        form = AddPageForm(request.POST)
        if form.is_valid():
            ct = form.cleaned_data["content"]
            tt = form.cleaned_data["page_title"]
            # check title exist or not
            for tmp in util.list_entries():
                if tt.lower() == tmp:
                    print(tmp)
                    return render(request, "encyclopedia/error.html", {
                        "form": NewSearchForm(),
                        "error_msg": "Page already existed!"
                    })
            
            # save content
            new_file = open(f'./entries/{tt}.md', 'w')
            new_file.write(ct)
            new_file.close()
            print("save fiel")
            return HttpResponseRedirect(reverse("index"))
            # return render(request, "encyclopedia/index.html", {
            #     "form": NewSearchForm(),
            #     "entries": util.list_entries()
            # })
        else:
            return render(request, 'encyclopedia/add_page.html', {
                "form": NewSearchForm(),
                "new_forms": form
            })
    return render(request, "encyclopedia/add_page.html", {
        "form": NewSearchForm(),
        "new_forms": AddPageForm()
    })

def random_page(request):
    l = util.list_entries()
    random.shuffle(l)
    target = l[0]
    print(target)
    return load_content(request, target)
    