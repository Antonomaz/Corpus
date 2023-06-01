import json
import glob

test_file: str = "../tests/Mazarinades_jsons_tests/1-100/Moreau100_GALL.json"
test_dir: str = "../tests/Mazarinades_jsons_tests/1-100/*.json"


def corrected_file_stats(dir_path: str):
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
        nbPages = data_dict["entête"]["nbPages"]
        if nbPages in result_dict:
            result_dict[nbPages] += 1
        else:
            result_dict[nbPages] = 1
     # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}

# put dubious/alleged authors in known authors


def author_stats(dir_path: str):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {}
    file_count: int = len(file_list)
    for filepath in file_list:
        data_dict: dict = json.load(open(filepath))
        author_dict: dict = data_dict["entête"]["author"]
        if author_dict is None:
            if "unnamed" in result_dict:
                result_dict["unnamed"] += 1
            else:
                result_dict["unnamed"] = 1
        else:
            # dubious author
            if "@role" in author_dict:
                if "dubious" in result_dict:
                    result_dict["dubious"] += 1
                else:
                    result_dict["dubious"] = 1
            # pseudonyms
            elif "addName" in author_dict:
                if "@type" in author_dict["addName"] and author_dict["addName"]["@type"] == "pseudonyme":
                    if result_dict["pseudonym"] in result_dict:
                        result_dict["pseudonym"] += 1
                    else:
                        result_dict["pseudonym"] = 1
            # full names
            else:
                if "known_author" in result_dict:
                    result_dict["known_author"] += 1
                else:
                    result_dict["known_author"] = 1
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}


def publisher_helper(result_dict: dict, publisher_dict: dict):
    # inconsistent formatting handling
    if "persName" not in publisher_dict and "surname" in publisher_dict:
        if "known_publisher" in result_dict:
            result_dict["known_publisher"] += 1
        else:
            result_dict["known_publisher"] = 1
    else:
        persName = publisher_dict["persName"]
        if isinstance(persName, str) and persName == "Sans Nom":
            if "unnamed" in result_dict:
                result_dict["unnamed"] += 1
            else:
                result_dict["unnamed"] = 1
        elif isinstance(persName, dict) and "surname" in persName:
            if "known_publisher" in result_dict:
                result_dict["known_publisher"] += 1
            else:
                result_dict["known_publisher"] = 1

    return result_dict


def publisher_stats(dir_path: str):
    file_list: list = glob.glob(dir_path)
    result_dict: dict = {}
    file_count: int = len(file_list)
    for filepath in file_list:
        # print(filepath)
        data_dict: dict = json.load(open(filepath))
        publisher = data_dict["entête"]["publisher"]
        print(publisher)
        # handling lists of publishers
        if isinstance(publisher, list):
            for p in publisher:
                result_dict = publisher_helper(result_dict=result_dict, publisher_dict=p)
        else:
            result_dict = publisher_helper(result_dict=result_dict, publisher_dict=publisher)

     # {<page count>: (<number of docs for page count>, <percent compared to total file count>)}
    return {key: (val, val/file_count * 100) for key, val in result_dict.items()}


def test_stats():
    print(corrected_file_stats(dir_path=test_dir))
    print(nb_page_stats(dir_path=test_dir))
    print(author_stats(dir_path=test_dir))
    print(publisher_stats(dir_path=test_dir))
    return
