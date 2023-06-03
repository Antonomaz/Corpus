import json
import glob
import dateutil.parser as duparser
import flatdict #external dependancy but hopefully just for the temporary fixes anyway until the xml files are normalised/no need for special handling for anything
 
test_file: str = "../tests/Mazarinades_jsons_tests/1-100/Moreau100_GALL.json"
test_dir: str = "../tests/Mazarinades_jsons_tests/*/*.json"

unknown_pub_place: str = "Sans Lieu"
unknown_pub_name: str = "Sans Nom"
unknown_pub_date:str = "Sans Date"


def corrected_file_stats(dir_path: str) -> dict:
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
    return {"file_count": file_count, "corrected_file_count": corrected_file_count, "corrected_file_percentage": corrected_file_count/file_count * 100}


def nb_page_stats(dir_path: str):
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
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}

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

def author_stats(dir_path: str) -> dict:
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
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}


def publisher_helper(result_dict: dict, publisher_dict: dict):
    # inconsistent formatting handling
    # note: persName/orgName
    if "persName" not in publisher_dict and ("surname" or "orgName" in publisher_dict):
        result_dict["named_publisher"] += 1
    else:
        # regular case
        flat_publisher_dict = flatdict.FlatDict(value=publisher_dict)
        #print(flat_publisher_dict)
        #pseudonyms
        if "pseudonyme" in flat_publisher_dict.values():
            result_dict["pseudonym"] +=1
        else:
            persName = publisher_dict["persName"]
            if isinstance(persName, dict):
               if "surname" in persName:
                result_dict["named_publisher"] += 1
               elif unknown_pub_name in persName.values():
                   result_dict["unnamed_publisher"] +=1
            elif isinstance(persName, str):
                if persName == unknown_pub_name:
                    result_dict["unnamed_publisher"] += 1
                else:
                    result_dict["named_publisher"] +=1
            else:
                print(publisher_dict)
    return result_dict

# assumption: no case where one publisher is clearly known and the other has a pseudonym or is unnamed


def publisher_stats(dir_path: str) -> dict:
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {"named_publisher": 0, "unnamed_publisher": 0, "pseudonym": 0}
    file_count: int = len(file_list)
    for filepath in file_list:
        #print(filepath)
        data_dict: dict = json.load(open(filepath))
        publisher = data_dict["entête"]["publisher"]
        # handling lists of publishers
        if isinstance(publisher, list):
            #print(publisher)
            for p in publisher:
                old_named_publisher_count: int = result_dict["named_publisher"]
                result_dict = publisher_helper(result_dict=result_dict, publisher_dict=p)
                if result_dict["named_publisher"] > old_named_publisher_count:
                    break
        else:
            result_dict = publisher_helper(result_dict=result_dict, publisher_dict=publisher)
    print(sum(result_dict.values()))
     # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}


def pub_place_helper(result_dict: dict, pub_place_dict: dict):
    pub_place: str = pub_place_dict["#text"]
    if pub_place == unknown_pub_place:
        result_dict[unknown_pub_place] +=1
    else:
        if pub_place in result_dict:
            result_dict[pub_place] += 1
        else:
            result_dict[pub_place] = 1
    return result_dict


def pub_place_stats(dir_path: str):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {unknown_pub_place:0}
    file_count: int = len(file_list)
    # to check if the file count is correct once you take into account lists
    dup_count:int = 0 
    for filepath in file_list:
        old_sum:int = sum(result_dict.values())
        # print(filepath)
        data_dict: dict = json.load(open(filepath))
        #print(data_dict["entête"]["pubPlace"])
        pub_place = data_dict["entête"]["pubPlace"]
        #handling inconsistent formatting
        if isinstance(pub_place, str):
            #print(pub_place)
            if pub_place == unknown_pub_place:
                result_dict[unknown_pub_place] +=1
            else:
                if pub_place in result_dict:
                 result_dict[pub_place] += 1
                else:
                    result_dict[pub_place] = 1
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
    return {key: (val, val/file_count * 100) for key, val in result_dict.items() if val > 10}

def pub_date_helper(result_dict:dict, pub_date_dict:dict)->dict:
    when_key:str = "@when"
    if when_key not in pub_date_dict:
        if unknown_pub_date in pub_date_dict.values():
            result_dict[unknown_pub_date]+=1
    else:        
        #using the year by default
        pub_date = duparser.parse(timestr=pub_date_dict["@when"]).year
        if pub_date in result_dict:
            result_dict[pub_date] += 1
        else:
            result_dict[pub_date] = 1
    return result_dict

def pub_date_stats(dir_path: str):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {unknown_pub_date: 0}
    file_count: int = len(file_list)
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        pub_date = data_dict["entête"]["pubDate"]
        #print(pub_date)
        
        #handling inconsistent formatting
        if isinstance(pub_date, str):
            #print(pub_date)
            if pub_date == unknown_pub_date:
                result_dict[pub_date] += 1
            else:
                #using the year by default
                pub_date = duparser.parse(timestr=pub_date).year
                if pub_date in result_dict:
                 result_dict[pub_date] += 1
                else:
                    result_dict[pub_date] = 1
        # regular case
        else:
            # handling lists
            if isinstance(pub_date, list):
                for p_d in pub_date:
                    if "@when" in p_d:
                        result_dict = pub_date_helper(result_dict=result_dict, pub_date_dict=p_d)
                        break               
            else:
                result_dict = pub_date_helper(result_dict=result_dict, pub_date_dict=pub_date)
    print(sum(result_dict.values()))
    # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}

def imprimatur_stats(dir_path:str):
    return

def test_stats():
    #print(corrected_file_stats(dir_path=test_dir)) #ok count
    #print(nb_page_stats(dir_path=test_dir)) #ok count
    #print(author_stats(dir_path=test_dir)) #ok count
    print(publisher_stats(dir_path=test_dir))
    #print(pub_place_stats(dir_path=test_dir)) #ok count
    #print(pub_date_stats(dir_path=test_dir))
    return


test_stats()
