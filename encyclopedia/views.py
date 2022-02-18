from django.shortcuts import render

from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    # Check to see if the .md file exists
    print("inside wiki")
    mdfile = util.get_entry(name)
    # If not an md entry, return error page
    if(mdfile == None):
        return render(request, "encyclopedia/apology.html")
    # convert .md file to html
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    with open(f'encyclopedia/templates/html/{name}.html', 'w') as f:
        f.write(html)

    return render(request, f"html/{name}.html")

def search(request):
    print("inside search")
    q = request.GET['q']
    mdfile = util.get_entry(q)
    # If not an md entry, return error page
    if(mdfile == None):
        return render(request, "encyclopedia/apology.html")
    # convert .md file to html
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    with open(f'encyclopedia/templates/html/{q}.html', 'w') as f:
        f.write(html)

    return render(request, f"html/{q}.html")

def create(request):
    print("inside create")
    q = request.GET['q']
    print(q)

    

    
    

