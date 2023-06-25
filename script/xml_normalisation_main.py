from xml_normalisation import *
test_BM_file:str = "../tests/Mazarinades_tests/Bibliotheque_Mazarine/BM48896_MAZ.xml"
#normalise_xml(input_filepath=test_file1)
#normalise_xml(input_filepath=test_file2)
#normalise_xml(input_filepath=test_file3)
#normalise_xml(input_filepath=test_file4)
#normalise_xml(input_filepath=test_file5, output_filepath="temp.xml")
#normalise_xml(input_filepath=test_file6, output_filepath="temp_xml/temp.xml")
#normalise_xml(input_filepath=test_file7, output_filepath="temp_xml/temp.xml")
#tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
#normalise_names(input_filepath=test_file8, output_filepath="temp_xml/temp.xml", value_to_change="pièce de théâtre", replacement="texte de forme théâtrale")
#tei_to_json_file(filepath="temp_xml/temp.xml", main_output_dir="./temp")
#test_stats()

#change_attribute_name(input_filepath=test_BM_file, output_filepath="temp_xml/BM.xml", tag="pb", old_attribute="n", new_attribute="vue", namespace=namespace)
#change_attribute_name_dir(dir_path=maz_dir, tag="pb", old_attribute="n", new_attribute="vue", namespace=namespace)

normalise_xml_dir(dir_path=test_dir, value_to_change="pièce de théâtre", replacement="texte de forme théâtrale", change_name=True)