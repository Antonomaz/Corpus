#! /usr/bin/env bash
python3 xml_normalisation.py;
 python3 tei_to_json_main.py;
 python3 json_stats_normalised_main.py;
