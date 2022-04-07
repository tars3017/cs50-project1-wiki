from django.shortcuts import render

from . import util

from markdown2 import markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_content(request, title):
    with open(f"entries/{title}.md") as f:
        s = f.read()   
        return render(request, "encyclopedia/show_result.html", {
            "page_title": title,
            "content": markdown(s)
        })

