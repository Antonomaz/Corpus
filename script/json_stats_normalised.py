import json
import glob
import csv
import dateutil.parser as duparser
import flatdict #external dependancy but hopefully just for the temporary fixes anyway until the xml files are normalised/no need for special handling for anything
test_file: str = "../Mazarinades_jsons/1-100/Moreau100_GALL.json"
#test_dir: str = "../tests/Mazarinades_jsons/*/*.json"
test_dir: str = "../Mazarinades_jsons/*/*.json"
csv_dir:str="../output/stats"
# old names
#unknown_pub_place: str = "Sans Lieu"
#unknown_pub_name: str = "Sans Nom"
#unknown_pub_date:str = "Sans Date"
unknown_pub_place: str = "Sans lieu"
unknown_pub_name: str = "Sans nom"
unknown_pub_date:str = "Sans date"
inconsistent_format_list_path:str = "../output/"
no_when_file:str = "../output/inconsistent_format/no_when.txt"
str_when_file:str = "../output/inconsistent_format/str_when.txt"
no_date_dict_file:str = "../output/inconsistent_format/no_date_dict.txt"
no_persName_file:str = "../output/inconsistent_format/no_persName.txt"

def write_to_csv(data_dict:dict, csv_dir:str = csv_dir, filename:str="", mode:str = "w", fieldnames:list = ["status", "count"], iterable_values:bool = True):
    csv_file = open(file=f"{csv_dir}/{filename}.csv", mode=mode)
    res = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
    res.writeheader()
    if not iterable_values:
        res.writerow(data_dict)
        return
    for key,val in data_dict.items():
        rowdict:dict = {fieldnames[0]:key}
        for i in range(1,len(fieldnames)):
            rowdict[fieldnames[i]] = val[i-1]
        res.writerow(rowdict=rowdict)      
    return

def corrected_file_stats(dir_path: str, save_to_csv:bool = True) -> dict:
    """returns stats on the proportion of files in the corpus that has been manually reviewed and corrected by humans.

    Args:
        dir_path (str): path to the corpus' directory

    Returns:
        dict{str: int, str: int, str: float}: {'file_count': <file count>, 'corrected_file_count': <corrected file count>, 'corrected_file_percentage': <corrected file percentage>}
    """
    file_list: list = glob.glob(dir_path)
    file_count: int = len(file_list)
    corrected_file_count: int = 0
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        if data_dict["corrector"]:
            corrected_file_count += 1
    stat_dict:dict = {"file_count": file_count, "corrected_file_count": corrected_file_count, "corrected_file_percentage": corrected_file_count/file_count * 100}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="corrected_file_stats", fieldnames=[k for k in stat_dict.keys()], iterable_values=False)   
    return stat_dict
    

def nb_page_stats(dir_path: str, save_to_csv:bool = True):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {}
    file_count: int = len(file_list)
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        nbPages:int = data_dict["entête"]["nbPages"]
        if nbPages in result_dict:
            result_dict[nbPages] += 1
        else:
            result_dict[nbPages] = 1
    # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    print(sum(result_dict.values()))
    stat_dict:dict= {key: (val, val/file_count * 100) for key, val in result_dict.items()}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="nb_page_stat", fieldnames=["nb_page", "count", "percentage"])   
    return stat_dict

# WASDONE: put dubious/alleged authors in known authors
# for pseudonyms: tests/Mazarinades_jsons_tests/1-100/Moreau50_GALL.json
def author_helper(result_dict: dict, author_dict: dict, in_list:bool = False)->dict:
    """helper function for author_stats.

    Args:
        result_dict (dict): the result dictionary to update.
        author_dict (dict): the dictionary with the authorship info to parse.
        in_list (bool, optional):when used to parse authors in a list. Defaults to False. Ignores pseudonyms (doesn't add them to the result dict) if set to True.

    Returns:
        dict: the updated result dict.
    """
    #unnamed/unknown authors
    if author_dict is None:
        result_dict["unnamed_author"] += 1
    else:
        # pseudonyms
        #print(author_dict)
        flat_author_dict = flatdict.FlatDict(value=author_dict)
        #print(flat_author_dict)
        if "pseudonyme" in flat_author_dict.values():
            if not in_list:
                result_dict["pseudonym"] += 1
        # confirmed OR alleged/dubious author
        else:
            result_dict["named_author"] += 1
    return result_dict

def author_stats(dir_path: str, save_to_csv:bool = True) -> dict:
    """returns stats on the authorship status of the texts in the corpus. There are three possible statuses: "unnamed_author", "pseudonym", and "named_author". Documents specified to have "dubious/alleged authorship" in the json metadata are counted under "named_author".
    Args:
        dir_path (str): path to the corpus' directory
    Returns:
        dict{<str>: tuple(<int>, <float>)}: {<authorship status>: (<number of docs with that authorship status>, <percentage compared to total file count>)}
    """
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {"named_author": 0, "unnamed_author":0, "pseudonym": 0}
    file_count: int = len(file_list)
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        author = data_dict["entête"]["author"]
        # list handling
        if isinstance(author, list):
            #print(author)
            i:int = 0
            for i in range(len(author)-1):
                old_named_author_count:int = result_dict["named_author"]
                result_dict = author_helper(result_dict=result_dict, author_dict=author[i], in_list=True) 
                #TODO: case where one author is dubious and the other not
                if result_dict["named_author"] > old_named_author_count:
                    break
            # to handle cases of lists with only pseudonyms so that at least one can be counted
            else:
                result_dict = author_helper(result_dict=result_dict, author_dict=author[i], in_list=False)
        else:                
            result_dict = author_helper(result_dict=result_dict, author_dict=author)
    print(sum(result_dict.values()))
    stat_dict:dict = {key: (val, val/file_count * 100) for key, val in result_dict.items()}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="author_stats", fieldnames=["authorship status", "count", "percentage"])   
    return stat_dict


def publisher_helper(result_dict: dict, publisher_dict: dict, filepath = "", in_list:bool = False):
    persName_keys:list = ["surname", "forename", "orgName"]
    keys: list = ["named_publisher", "pseudonym", "unnamed_publisher"]
    updated_key:str = ""
    flat_publisher_dict = flatdict.FlatDict(value=publisher_dict)
    #print(flat_publisher_dict)
    #pseudonyms
    if "pseudonyme" in flat_publisher_dict.values():
            result_dict["pseudonym"] +=1
            updated_key = keys[1]
    else:
        persName = publisher_dict["persName"]
        if isinstance(persName, dict):
            if "surname" or "orgName" in persName:
                result_dict["named_publisher"] += 1
                updated_key = keys[0]
            # not normal for this one
            elif unknown_pub_name in persName.values():
                result_dict["unnamed_publisher"] +=1
                print(publisher_dict, filepath)
        elif isinstance(persName, str):
            #print(publisher_dict, filepath, file=open("temp.txt", "a"))
            if persName == unknown_pub_name:
                result_dict["unnamed_publisher"] += 1
                updated_key = keys[2]
                #print(publisher_dict)
            else:
                result_dict["named_publisher"] +=1
                updated_key = keys[0]
    return result_dict, updated_key

# assumption: no case where one publisher is clearly known and the other has a pseudonym or is unnamed
# NB: false assumption: one case was found (../tests/Mazarinades_jsons_tests/101-200/Moreau169_MAZ.json)

def publisher_stats(dir_path: str, save_to_csv:bool = True) -> dict:
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {"named_publisher": 0, "unnamed_publisher": 0, "pseudonym": 0}
    file_count: int = len(file_list)
    for filepath in file_list:
        #print(filepath)
        data_dict: dict = json.load(open(filepath))
        publisher = data_dict["entête"]["publisher"]
        # handling lists of publishers
        if isinstance(publisher, list):
            temp_dict:dict = dict.fromkeys(result_dict, 0)
            #print(temp_dict)
            #print(publisher)
            all_it:bool = True
            for p in publisher:
                temp_dict, updated_key = publisher_helper(result_dict=temp_dict, publisher_dict=p, filepath=filepath)
                if updated_key == "named_publisher":
                    result_dict["named_publisher"] +=1
                    all_it = False
                    break
                #if all_it:
                #    print(publisher, filepath)
            else:
                if temp_dict["pseudonym"] > 0:
                    result_dict["pseudonym"] +=1
                else:
                    result_dict["unnamed_author"] +=1
        else:
            result_dict, _ = publisher_helper(result_dict=result_dict, publisher_dict=publisher, filepath=filepath)
    print(sum(result_dict.values()))
     # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    stat_dict: dict = {key: (val, val/file_count * 100) for key, val in result_dict.items()}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="publisher_stats", fieldnames=["publisher status", "count", "percentage"])   
    return stat_dict


def pub_place_helper(result_dict: dict, pub_place_dict: dict):
    pub_place: str = pub_place_dict["#text"]
    if pub_place == unknown_pub_place:
        #print(pub_place_dict)
        result_dict[unknown_pub_place] +=1
    else:
        if pub_place in result_dict:
            result_dict[pub_place] += 1
        else:
            result_dict[pub_place] = 1
    return result_dict


def pub_place_stats(dir_path: str, save_to_csv:bool = True, filepath:str=""):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {unknown_pub_place:0}
    file_count: int = len(file_list)
    # to check if the file count is correct once you take into account lists
    dup_count:int = 0 
    for filepath in file_list:
        old_sum:int = sum(result_dict.values())
        data_dict: dict = json.load(open(filepath))
        pub_place = data_dict["entête"]["pubPlace"]
        #handling inconsistent formatting
        if isinstance(pub_place, str):
            print(f"ERROR!!!!!!!!! {pub_place}, {filepath}")            
        else:            
            # handling lists
            if isinstance(pub_place, list):
                for p in pub_place:
                    result_dict = pub_place_helper(result_dict=result_dict, pub_place_dict=p)
                    if pub_place.index(p) != 0:
                        dup_count +=1
            else:
               result_dict = pub_place_helper(result_dict=result_dict, pub_place_dict=pub_place)
        if sum(result_dict.values()) == old_sum:
            print(pub_place)
     # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    #print(file_count)
    print(sum(result_dict.values())- dup_count)
    stat_dict:dict = {key: (val, val/file_count * 100) for key, val in result_dict.items() if val > 10}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="pub_place_stat", fieldnames=["place", "count", "percentage"])   
    return stat_dict

def pub_date_helper(result_dict:dict, pub_date_dict:dict, filepath:str= ""):
    updated_key: str|int = ""
    when_key:str = "@when"
    if when_key not in pub_date_dict:
        if unknown_pub_date in pub_date_dict.values():
            result_dict[unknown_pub_date]+=1
            updated_key = unknown_pub_date
        else:
            print(f"ERROR!!!!!!!!! {pub_date_dict}, {filepath}")            
    else: 
        if unknown_pub_date in pub_date_dict.values():
            result_dict[unknown_pub_date]+=1
        else:               
            #using the year by default
            pub_date = duparser.parse(timestr=pub_date_dict["@when"]).year
            updated_key = pub_date
            if pub_date in result_dict:
                result_dict[pub_date] += 1
            else:
                result_dict[pub_date] = 1
    return result_dict, updated_key

def pub_date_stats(dir_path: str, save_to_csv:bool=True):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {unknown_pub_date: 0}
    file_count: int = len(file_list)
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        pub_date = data_dict["entête"]["pubDate"]
        # handling lists
        if isinstance(pub_date, list):
            temp_dict:dict = dict.fromkeys(result_dict, 0)
            for p_d in pub_date:
                    temp_dict, updated_key = pub_date_helper(result_dict=temp_dict, pub_date_dict=p_d, filepath=filepath)
                    if updated_key != unknown_pub_date:
                        if updated_key in result_dict:
                            result_dict[updated_key] +=1
                        else:
                            result_dict[updated_key] = 1
                        break
            else:
                result_dict[unknown_pub_date] +=1  
                print(pub_date)  
        else:
            result_dict, _ = pub_date_helper(result_dict=result_dict, pub_date_dict=pub_date,filepath=filepath)
    print(sum(result_dict.values()))
    # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    stat_dict:dict = {key: (val, val/file_count * 100) for key, val in result_dict.items()}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="pub_date_stat", fieldnames=["year", "count", "percentage"])
    return stat_dict   

def imprimatur_stats(dir_path:str, save_to_csv:bool=True):
    file_list: list = glob.glob(dir_path)
    file_count: int = len(file_list)
    imprimatur_count: int = 0
    for filepath in file_list:
        print(filepath)
        data_dict: dict = json.load(open(filepath))
        print(data_dict.keys())
        if (impr:= data_dict["imprimatur"]) is not None:
            imprimatur_count += 1
    stat_dict:dict = {"file_count": file_count, "imprimatur-ed_file_count": imprimatur_count, "imprimatur-ed_file_percentage": imprimatur_count/file_count * 100}
    if save_to_csv:
        write_to_csv(data_dict=stat_dict, csv_dir=csv_dir, filename="imprimatur_stat", fieldnames=[k for k in stat_dict.keys()], iterable_values=False)    
    return stat_dict

def test_stats():
    #print(corrected_file_stats(dir_path=test_dir, save_to_csv=False)) #ok count
    #print(nb_page_stats(dir_path=test_dir, save_to_csv=False)) #ok count
    #print(author_stats(dir_path=test_dir, save_to_csv=False )) #ok count
    print(publisher_stats(dir_path=test_dir, save_to_csv=False)) #ok count
    print(pub_place_stats(dir_path=test_dir, save_to_csv=False)) #ok count
    print(pub_date_stats(dir_path=test_dir, save_to_csv=False)) #ok_count
    #imprimatur_dict: dict = imprimatur_stats(dir_path=test_dir)
    #write_to_csv(data_dict=imprimatur_dict, csv_dir=csv_dir, filename="imprimatur_stats")
    return
