def generate_types_cardinality(g,prop):
    
    list_types=list()
    cardianliy="ONE"
    
    if "type" in prop.keys():
        if "format" in prop.keys():
            list_types.append(prop["format"])
        else :
            list_types.append(prop["type"])
    
    if "anyOf" in prop.keys():
        for e in prop["anyOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else :
                for t in e.keys():
                    list_types.append(e[t])
    
    if "oneOf" in prop.keys():
        for e in prop["oneOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else :
                for t in e.keys():
                    list_types.append(e[t])

    i=1
    j=1
    while i==1:
        i=0
        j=j+1
        for t in list_types:
            if isinstance(t,dict):
                i=1
                e=t
                list_types.remove(t)
                if "format" in e.keys():
                    list_types.append(e["format"])
                else:
                    for sous_type in e.keys():
                        list_types.append(e[sous_type])
                   
    if len(list_types)==0:
        cardianliy=""
        
    #Some cleaning up
    expected_types =[]
    
    for t in list_types:
        if len(t.split('/'))>1 :
            expected_types.append(t.split('/')[-1].capitalize())
            ##If we ever needed it
            #external_type= g['$validation']["definitions"][t.split('/')[-1]]
            #print(Fore.YELLOW + f'Def of the External Type : {external_type}' + Style.RESET_ALL)            

        else :
            expected_types.append(t.capitalize())    

    ##Remove duplicates
    clean_expected_types = list(set(expected_types))

    #Replace 'String' with 'Text'
    for i in clean_expected_types:
        if i == "String":
            clean_expected_types.remove(i)
            clean_expected_types.append("Text")
    #print(Fore.MAGENTA + f'Expected Types : {clean_expected_types}' + Style.RESET_ALL)

    #print(Fore.RED + f'Cardinality = {cardianliy}' + Style.RESET_ALL)

    return cardianliy, clean_expected_types