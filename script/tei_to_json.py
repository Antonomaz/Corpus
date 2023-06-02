from glob import glob
import json
from pathlib import Path

import texte

from tqdm.auto import tqdm

path = "../Mazarinades/*/*.xml"

files = glob(path)

collection_textes = [e for e in texte.corpora(files) if e.plain]
lst = [[files[i], e.header, e.texte, e.corrector] for i, e in enumerate(collection_textes)]

main_folder = Path("../Mazarinades_jsons_tests")
for e in tqdm(lst):
    file = e[0]
    file = Path(file).parts

    newpath = main_folder.joinpath(file[2])
    newpath.mkdir(parents=True, exist_ok=True)

    file = Path(file[-1]).with_suffix(".json")
    newpath = newpath.joinpath(file)

    tempdict = {
        "corrector": e[3],
        "entête": e[1],
        "texte": e[2]
    }
    with open(newpath, mode="w", encoding="utf-8") as f:
        json.dump(tempdict, f, indent=4, ensure_ascii=False)
