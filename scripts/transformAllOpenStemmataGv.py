# Now with a local copy of https://github.com/OpenStemmata/database/tree/main/data
# Repo can be accessed via Github API and PyGithub https://pygithub.readthedocs.io/en/latest/examples.html


import os
import stemma_gv2ttl_funct as s

allGvFiles = []
for root, dirs, files in os.walk('../originalOpenStemmataData_20230422'):
    for file in files:
        if file.endswith(".gv"):
            allGvFiles.append(os.path.join(root, file))
# print(allGvFiles)
print(len(allGvFiles))

# apply stemma_gv2ttl.py to all files in the list
t = open('../openStemmataData.ttl', 'w')
# create the prefixes
prefixes = "@prefix stemma-onto: <http://example.com/stemma-onto#> . \n@prefix frbr: <http://purl.org/vocab/frbr/core#> . \n@prefix dct: <http://purl.org/dc/terms/> . \n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \n\n\n"
t.write(prefixes)
for file in allGvFiles:
    print(file)
    stemma_instance, nodes, edges = s.gv2ttl(file)
    t.write(stemma_instance)
    for node in nodes:
        if node != None:
            t.write(node)
    for edge in edges:
        t.write(edge)
    t.write("###################################################################### \n\n\n")
t.close()



