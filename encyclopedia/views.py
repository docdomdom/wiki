from django.shortcuts import render
from django.shortcuts import redirect

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    content = util.get_entry(title)
    if content != None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {"title":title})

def search(request):
    q=request.GET.get("q")
    entries = util.list_entries()
    entries_to_lower = [entry.lower() for entry in entries]

    if q in entries_to_lower:
        pass
    else:
        pass
    return redirect('entry', title=q)

    




