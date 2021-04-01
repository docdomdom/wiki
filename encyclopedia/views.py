from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.http import HttpResponse
import random
import markdown2


from . import util

class CreateEntryForm(forms.Form):
        title = forms.CharField(label="", widget= forms.TextInput(attrs={'placeholder':'Title', 'class': 'form-control'}))
        content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Content', 'class': 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    content = util.get_entry(title)
    if content != None:
        content=markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        error = f"{title} not found."
        return render(request, "encyclopedia/error.html", {"error":error})

def search(request):
    # get url parameter
    q=request.GET.get("q")

    # get entries from storage
    entries = util.list_entries()

    # convert entries to lower string with list comprehension for comparison
    entries_lowercase = [entry.lower() for entry in entries]
    q_lowercase = q.lower()

    # look for exact match in list (checks for exact match, not substring when searchin in lists)
    # and redirect
    if q_lowercase in entries_lowercase:
        return redirect('entry', title=q)
    else:
        # empty list for hits
        matches = []
        
        # check for substring in string
        for entry in entries:
            if q_lowercase in entry.lower():
                matches.append(entry)

        if matches == []:
            error = f"{q} not found."
            return render(request, "encyclopedia/error.html", {"error":error})

        return render(request, "encyclopedia/index.html", {
            "entries": matches
        })

def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return redirect ('entry', title=title)
            else:
                error = f"{title} already exists."
                return render(request, "encyclopedia/error.html", {
                "error": error
                })

    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateEntryForm()
        })
    
def edit(request, title):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect ('entry', title=title)
        else:
            error = f"Error = {title}" 
            return render(request, "encyclopedia/error.html", {
                "error": error
            })
    else:
        content = util.get_entry(title) 
        initial_dict = {"content" : content, "title" : title}
        form = CreateEntryForm(initial_dict)
        form.fields['title'].widget.attrs['readonly'] = True
        print(form)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
        })

def random_entry(request):
    entries = util.list_entries()
    random_number = random.randint(0,len(entries)-1)
    return redirect('entry', title=entries[random_number])
