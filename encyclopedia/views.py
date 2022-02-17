from django.shortcuts import render

from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    # Check to see if the .md file exists
    mdfile = util.get_entry(name)
    # If so then we convert/write to HTML
    if(mdfile == None):
        return render(request, "encyclopedia/apology.html")

    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    with open(f'encyclopedia/templates/html/{name}.html', 'w') as f:
        f.write(html)

    return render(request, f"html/{name}.html")
    

    
    

