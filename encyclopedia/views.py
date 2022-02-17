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
    print("inside wiki")
    # If so then we convert/write to HTML
    if(mdfile == None):
        render("encyclopedia/apology.html")

    print("Passed")
    markdowner = Markdown()
    markdowner.convert(mdfile)
    with open(f'{name}.html', 'w') as f:
        f.write(markdowner)
    

    
    

