from django.shortcuts import render

from . import util

from markdown2 import Markdown
markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def css(request):
    with open("entries/CSS.md") as f:
        s = f.read()   
        print(markdowner.convert(s))
        return render(request, "encyclopedia/show_result.html", {
            "page_title": "CSS",
            "content": markdowner.convert(s)
        })

def django(request):
    return render(request, "encyclopedia/show_result.html")

def git(request):
    return render(request, "encyclopedia/show_result.html")

def html(request):
    return render(request, "encyclopedia/show_result.html")

def python(request):
    return render(request, "encyclopedia/show_result.html")

