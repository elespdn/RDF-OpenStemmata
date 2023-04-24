
## transform the node lines
def transformNodeLines(line, gvFileName):    
    '''
    This function takes a node line from a .gv file as input and returns one or more triples as output.
    '''
    witnessName = line.split('[')[0].strip()
    if 'color="grey"' in line:
        if 'label' in line:
            witnessLabel = line.split('label="')[1].split('"')[0]
            return "<" + gvFileName + "_node_" + witnessName + "> a stemma-onto:HypotheticalWitness ;" + '\n\t\t\t rdfs:label "' + witnessLabel + '" ;\n\t\t\t stemma-onto:isWitnessIn <' + gvFileName + "_stemma> . \n\n\n"
        else :
            witnessLabel = witnessName
            return "<" + gvFileName + "_node_" + witnessName + "> a stemma-onto:HypotheticalWitness ;" + '\n\t\t\t rdfs:label "' + witnessLabel + '" ;\n\t\t\t stemma-onto:isWitnessIn <' + gvFileName + "_stemma> . \n\n\n"
    elif 'label' in line:        
        witnessLabel = line.split('label="')[1].split('"')[0]
        return "<" + gvFileName + "_node_" + witnessName + "> a stemma-onto:ExistingWitness , frbr:Expression ;" + '\n\t\t\t rdfs:label "' + witnessLabel + '" ;\n\t\t\t stemma-onto:isWitnessIn <' + gvFileName + "_stemma> . \n\n\n"




def createSourceIfNotInWitnessList(source, witnessList, gvFileName):
        if source not in witnessList:
            witnessList.append(source)
            return "<" + gvFileName + "_node_" + source + "> a stemma-onto:ExistingWitness , frbr:Expression ;" + '\n\t\t\t rdfs:label "' + source + '" ;\n\t\t\t stemma-onto:isWitnessIn <' + gvFileName + "_stemma> . \n\n\n"
        else:
            return ""

def createTargetIfNotInWitnessList(target, witnessList, gvFileName):
        if target not in witnessList:
            witnessList.append(target)
            return "<" + gvFileName + "_node_" + target + "> a stemma-onto:ExistingWitness , frbr:Expression ;" + '\n\t\t\t rdfs:label "' + target + '" ;\n\t\t\t stemma-onto:isWitnessIn <' + gvFileName + "_stemma> . \n\n\n"
        else:
            return ""
     

## transform the edge lines
def transformEdgeLines(line, gvFileName, witnessList):
    '''
    This function takes an edge line from a .gv file as input and returns one or more triples as output.
    '''
    # define source and target (if the node does not exist already, create it)
    source = line.split('->')[0].split("#")[0].strip()
    target = line.split('->')[1].split('[')[0].split(';')[0].split("#")[0].strip()
    addedSource = createSourceIfNotInWitnessList(source, witnessList, gvFileName)
    addedTarget = createTargetIfNotInWitnessList(target, witnessList, gvFileName)
    addedNodes = addedSource + addedTarget    
    
    # write the relation
    if 'style="dashed"' in line:
        if 'dir=none' in line:
            return addedNodes + "<" + gvFileName + "_node_" + target + "> stemma-onto:isHypotheticalContaminatingExemplarOf <" + gvFileName + "_node_" + source + "> . \n <" + gvFileName + "_node_" + source + "> stemma-onto:isHypotheticalContaminatingExemplarOf <" + gvFileName + "_node_" + target + "> . \n\n\n"
        else:
            return addedNodes + "<" + gvFileName + "_node_" + source + "> stemma-onto:isContaminatingExemplarOf <" + gvFileName + "_node_" + target + "> . \n\n\n"
    elif 'color="grey"' in line:
        return addedNodes + "<" + gvFileName + "_node_" + source + "> stemma-onto:isHypotheticallyAncestorOf <" + gvFileName + "_node_" + target + "> . \n\n\n"
    else:
        return addedNodes + "<" + gvFileName + "_node_" + source + "> stemma-onto:isExemplarOf <" + gvFileName + "_node_" + target + "> . \n\n\n"
    


def gv2ttl(gvSourceFile):
    """
    This function takes a .gv file as input and creates a .ttl file as output.
    The .gv file is a graphviz file that describes a stemma.
    The .ttl file is a turtle file that describes the same stemma in the stemma ontology.
    """
    
    f = open(gvSourceFile, 'r')

    # create the instance of the stemma
    #gvFileName = gvSourceFile.split('.')[0]
    gvFileName = gvSourceFile.split('/')[-2]
    sourceLanguage = gvSourceFile.split('/')[-3]
    stemma_instance = "<" + gvFileName + '_stemma> a stemma-onto:Stemma ; \n\t\t\t <stemma-onto:hasOpenStemmataEntry> "https://github.com/OpenStemmata/database/tree/main/data/' + sourceLanguage + '/' + gvFileName + '" ; \n\t\t\t <dct:language> "' + sourceLanguage + '" . \n\n\n'

    # create the list of witnesses, the list of nodeLines and the list of edgeLines (in order to first process nodeLines)
    witnessList = []
    nodeLines = []
    edgeLines = []
    for line in f:
        if '->' not in line and '{' not in line and '}' not in line and len(line.strip()) != 0 and (line.strip().startswith('#') is False)  and (line.strip().startswith('//') is False):
            witnessName = line.split('[')[0].strip()
            witnessList.append(witnessName)
            nodeLines.append(line)
        elif  '->' in line and (line.strip().startswith('#') is False) and (line.strip().startswith('//') is False):
            edgeLines.append(line)

    # print(witnessList)

    # create the nodes and the edges
    nodes = []
    for line in nodeLines:
        node = transformNodeLines(line, gvFileName)
        if node != "":
            nodes.append(node)
    
    edges = []
    for line in edgeLines:
        edge = transformEdgeLines(line, gvFileName, witnessList)
        if edge != "":
            edges += edge
    f.close()
    return stemma_instance, nodes, edges

