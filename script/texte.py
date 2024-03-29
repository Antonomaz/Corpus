import contextlib
import glob
import json
import re
from collections import Counter

import xmltodict
from bs4 import BeautifulSoup
from numpy import mean
from tqdm.auto import tqdm


def eval_sub_type(str_):
    if str_ == "no":
        return False
    elif str_ == "yes":
        return True
    else:
        return str_


with open("LGERM.json", encoding="utf-8") as f:
    LGERM = json.load(f)
mots_LGERM = set(LGERM)


def corpora(path: str | list):
    if isinstance(path, str):
        path = glob.glob(path)

    for file in tqdm(path):
        yield Texte(file)


class Texte:
    lexique = mots_LGERM

    pages_regex = re.compile(r"(?:<pb\s*.*?\s*>)")
    line_breaks_and_figures = re.compile(r'\n|(?:<\s*(?:lb?|figure)\s*(?:\w*=".*?"\s*)*/?>)')
    tabs_and_tags = re.compile(r'<.*?/?>|\t')
    double_spaces_and_beyond = re.compile(r'(\s){2,}')

    def __init__(self, path):
        # added in
        self.pages_number = None
        self.corrector: bool = None
        self.imprimatur: str = None
        self.elts = None

        self.ttrs = None
        self.ttr = None

        self.hapaxes = None
        self.hapax = None
        self.hapax_ratio = None

        self.texte = None
        self.plain = None
        self.pages = None

        self.lexicalites = None
        self.lexicalite = None
        self.lignes_non_lexicalisees = 0

        self.n_words: int = None
        self.n_lines: int = None
        self.n_pages: int = None
        self.n_chars: int = None

        self.path = path

        with open(path, encoding="utf-8") as f:
            self.txt = f.read()

            self.header = self.process_header()

            self.process_body()

    def get_txt(self):
        return self.txt

    def __repr__(self):
        return f"{self.__class__.__name__}({self.txt!r})"

    def __str__(self):
        return self.txt

    def __len__(self):
        return len(self.txt)

    def process_header(self) -> dict:
        dict_ = xmltodict.parse(self.txt)
        dict_ = dict_["TEI"]["teiHeader"]

        header = dict_["profileDesc"]["textClass"]["keywords"]["term"]
        header = [{header["@type"]: header["#text"] if "#text" in header else eval_sub_type(
            header["@subtype"]) if "@subtype" in header else None} for header in header]

        dict_header: dict = {}
        for dicts in header:
            for k, v in dicts.items():
                if k not in dict_header:
                    dict_header[k] = []
                dict_header[k].append(v)

        dict_header = {k: v if len(v) > 1 else v[0] for k, v in dict_header.items()}

        with contextlib.suppress(KeyError):
            creation = dict_["profileDesc"]["settingDesc"]["setting"]["date"]
            if creation is None:
                dict_header["creation"] = "00-00-0000"
            else:
                dict_header["creation"] = creation["@when"] if "@when" in creation else creation["#text"]

        dict_header["change"] = dict_["revisionDesc"]["change"]

        titre = dict_["fileDesc"]["titleStmt"]["title"]
        titre = [e["#text"] for e in titre if e["@type"] == "main" and "#text" in e]

        dict_header["titre"] = titre if isinstance(titre, str) else " ".join(titre)

        dict_header["dates"] = dict_["fileDesc"]["publicationStmt"]["date"]

        # added in: 2023-06-01
        # checking author
        dict_header["author"] = dict_["fileDesc"]["sourceDesc"]["bibl"]["author"]
        # print(dict_header["author"])

        # publication date
        dict_header["pubDate"] = dict_["fileDesc"]["sourceDesc"]["bibl"]["date"]
        # print(dict_header["pubDate"])

        # publication place
        dict_header["pubPlace"] = dict_["fileDesc"]["sourceDesc"]["bibl"]["pubPlace"]
        # print(dict_header["pubPlace"])

        # publisher
        dict_header["publisher"] = dict_["fileDesc"]["sourceDesc"]["bibl"]["publisher"]
        # print(dict_header["publisher"])

        # checking if the file has been reviewed or not
        persName_dict: dict = {}
        persName_list: list = dict_["fileDesc"]["titleStmt"]["respStmt"]["persName"]
        self.corrector = False
        for pers_dict in persName_list:
            if pers_dict["@role"] == "Corrector":
                self.corrector = True
                break
        # page count
        dict_header["nbPages"] = dict_["fileDesc"]["sourceDesc"]["bibl"]["extent"]["measure"]["@quantity"]
        # print(dict_header["nbPages"])
        return dict_header

    def get_header(self):
        return self.header

    def get_nb_pages(self):
        return (self.header)["nbPages"]

    def process_body(self):
        tei_head = re.search(r"<teiHeader.*?>.*?</teiHeader>", self.txt, re.DOTALL).group()
        # print(tei_head)

        soup = BeautifulSoup(tei_head, "html.parser")

        # 2023-06-05
        # elts = {e.tag: e.text for e in soup.find_all()} not sure what it was supposed to do: doesn't return anything
        elts = {tag.name: tag.text for tag in soup.find_all()}

        # 2024-02-03
        pages_number = BeautifulSoup(self.txt, "xml")
        pages_number = pages_number.find_all("pb")

        txt = self.pages_regex.split(self.txt)[1:]

        if not txt:
            print(f"Empty file: {self.path = }")
            return

        if len(pages_number) < len(txt):
            print(
                f"Number of pages and number of texts don't match: {self.path = }"
                f", {len(pages_number) = }, {len(txt) = }"
            )

        combined = zip(pages_number, txt)
        combined = [(e[0], self.line_breaks_and_figures.split(e[1])) for e in combined]
        # |<figure\s*type"\w*"\s*/> in the following regex (should be covered by <.*?/?>)
        combined = [(e[0], [self.tabs_and_tags.sub("", line) for line in e[1]]) for e in combined]
        # removing double spaces but keeping the right space
        combined = [(e[0], [self.double_spaces_and_beyond.sub(r'\1', line) for line in e[1]]) for e in combined]
        combined = [(e[0], [line.strip() for line in e[1] if line.strip()]) for e in combined]
        combined = [e for e in combined if e[1]]

        pages_number, txt = zip(*combined)

        pages_number = [e.get("n") if e.get("n") else e.get("vue") for e in pages_number]

        pages = [' '.join(line for line in page) for page in txt]

        plain = ' '.join(mot for page in txt for line in page for mot in line)

        if not plain:
            print(f"Empty file: {self.path = }")
            return

        self.pages_number = pages_number

        self.texte = txt

        self.elts = elts

        self.n_pages = len(self.txt)
        self.n_lines = sum(len(page) for page in txt)
        self.n_words = len(plain.split())
        self.n_chars = sum(len(line) for page in txt for line in page)

        self.ttrs = [self.mesurer_ttr(page) for page in pages]
        self.ttr = mean(self.ttrs)

        self.lexicalites = [self.mesurer_lexicalite(page) for page in pages]
        self.lexicalite = mean(self.lexicalites)

        self.hapaxes = [self.mesurer_hapax(page) for page in pages]
        self.hapax = sum(self.hapaxes)
        self.hapax_ratio = self.hapax / self.n_words

        self.pages = pages
        self.plain = plain

        # added in: 2023-06-04
        text_soup: BeautifulSoup = BeautifulSoup(self.txt, features="xml")
        imprimatur_text: str = text_soup.find("imprimatur")
        self.imprimatur = imprimatur_text.text if imprimatur_text is not None else None
        # print(self.imprimatur)

        return

    def mesurer_ttr(self, text):
        mots = text.split()
        vocabulaire = set(mots)
        if not mots:
            raise ValueError(f"Empty string, {self.path = }")
        return len(vocabulaire) / len(mots)

    def mesurer_lexicalite(self, text):
        tokens = text.split()
        mots_LGERM = self.lexique

        mots = [mot for mot in tokens if mot in mots_LGERM]

        if not mots:
            self.lignes_non_lexicalisees += 1
            return 0  # -1  a retester

        return len(mots) / len(tokens)

    @staticmethod
    def mesurer_hapax(text):
        mots = text.split()
        count = Counter(mots)
        return sum(1 for mot, occurrences in count.items() if occurrences == 1)


if __name__ == "__main__":
    test = "soft"

    path = "Corpus/Mazarinades/*/*.xml"

    testfile = "Corpus/Mazarinades/1-100/Moreau3_MAZ.xml"
    #    try:
    #      texte = Texte(testfile)
    #      print(texte.__dict__)
    #    except:
    #      continue

    if test != "soft":
        liste = list(corpora(path))
