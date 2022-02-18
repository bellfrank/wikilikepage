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
    q = request.GET['q']
    mdfile = util.get_entry(q)

    # If not an md entry, provide search results page with substring entries
    if(mdfile == None):
        similar_entries = []
        listmd = util.list_entries()

        # Adding similar entries to a list
        for i in listmd:
            if q in i:
                similar_entries.append(i)
        
        if (len(similar_entries) == 0):
            return render(request, "encyclopedia/apology.html")

        return render(request, "encyclopedia/results.html",{
            "similar_entries" : similar_entries
        })

    # else section: convert .md file to html
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    with open(f'encyclopedia/templates/html/{q}.html', 'w') as f:
        f.write(html)

    return render(request, f"html/{q}.html")


def create(request):
    if request.method == "POST":
        
        # store title in a variable 
        title = request.POST['title']
        content = request.POST['content']
        
        # Check to see if title is already an entry
        mdfile = util.get_entry(title)

        # If entry is already created, alert user
        if(mdfile != None):
            # somehow alert the user here
            pass
            
        #else we want to create the form 
        util.save_entry(title, content)
        
        
    else:
        return render(request, "encyclopedia/create.html")