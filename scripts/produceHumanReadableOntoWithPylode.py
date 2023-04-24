## PRODUCING THE HUMAN-READABLE VERSION OF THE ONTOLOGY WITH PYLODE

from pylode import OntDoc

# initialise
od = OntDoc(ontology="../stemma-onto.ttl")

# produce HTML
# html = od.make_html()

# or save HTML to a file
od.make_html(destination="../stemma-onto.html")
