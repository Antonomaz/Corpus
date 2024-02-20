from glob import glob
import json
from pathlib import Path

import texte

from tqdm.auto import tqdm

input_dir_path: str = "../Mazarinades/*/*.xml"
# path = "../Mazarinades/Antonomaz/*.xml"
# input_dir_path = "../tests/Mazarinades_tests/*/*.xml"
# file_list:list = glob(path)
test_file5: str = "../tests/Mazarinades_tests/2001-2100/Moreau2022_GBOOKS.xml"
# main_output_dir:str = "../tests/Mazarinades_jsons"
main_output_dir: str = "../Mazarinades_jsons"


# print(len(files))

def tei_to_json_file(filepath: str, main_output_dir: str = main_output_dir):
    """creates json for single tei file.

    Args:
        filepath (str): [description]

    Returns:
        [type]: [description]
    """
    main_folder = Path(main_output_dir)
    curr_text = texte.Texte(filepath)
    json_att_list: list = [curr_text.header, curr_text.texte, curr_text.corrector, curr_text.imprimatur, curr_text.pages_number]
    # expected format: .../..../.../xxxx/xxxxx/{..}/1-100/myfile.xml
    file_path_parts = Path(filepath).parts
    # find new subdir path and create it if needed
    new_sub_dir_path = main_folder.joinpath(file_path_parts[-2])
    new_sub_dir_path.mkdir(parents=True, exist_ok=True)
    # find new full path for new file
    new_filepath = new_sub_dir_path.joinpath(Path(file_path_parts[-1]).with_suffix(".json"))
    # print(new_filepath)
    # finally write json file
    tempdict: dict = {
        "imprimatur": json_att_list[3],
        "corrector": json_att_list[2],
        "entête": json_att_list[0],
        "texte": json_att_list[1],
        "pages_number": json_att_list[4]
    }
    json.dump(obj=tempdict, fp=(f := open(file=new_filepath, mode="w", encoding="utf-8")), indent=4, ensure_ascii=False)
    f.close()
    return tempdict


# tei_to_json_file(filepath=test_file5)

def tei_to_json_dir(input_dir_path: str = input_dir_path, output_dir_path: str = main_output_dir):
    filepath_list: list = glob(input_dir_path)
    res_dict: dict = {}
    for filepath in tqdm(filepath_list):
        #        try:
        res_dict[filepath] = tei_to_json_file(filepath=filepath, main_output_dir=output_dir_path)
    #        except:
    #          print(filepath)
    #          continue
    return res_dict

# tei_to_json_dir()
