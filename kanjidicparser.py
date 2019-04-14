
""" This is a script for parsing data from the KANJIDIC project (http://www.edrdg.org/wiki/index.php/KANJIDIC_Project)

Script opens kanjidic2.xml and reads the data into the variable "all_lines".
Data is then filtered for relevant information for each kanji character. "Relevant information" refers to the elements
of the "wanted_data" variable. These data points have been selected out of the greater data set in kanjidic2.xml
because of their importance to reading and understanding kanji for intermediate/advanced Japanese learners.
(See README for more details about what is parsed from kanjidic2.xml)
After parsing, a nested Python dictionary is built with keys for each individual kanji character. Each key refers
to another dictionary containing all information about that specific kanji key.
Functionality is included to export the built dictionary as a json file for use in other projects.
"""

import json
import re
import time

wanted_data = ["<!-- Entry for Kanji:", "<character>", "<literal>", "<freq>", "<jlpt>",
               '<reading r_type="ja_on">', '<reading r_type="ja_kun">', "<meaning>", "<nanori>",
               "</character>"]


def trim_data():
    """ Parses the all_lines list and returns only those lines that contains wanted data"""

    ret_lines = []
    for line in all_lines:
        for text in wanted_data:
            match = re.match(text, line)
            if match:
                if text == "</character>":
                    ret_lines.append(line)
                    ret_lines.append("\n")
                else:
                    ret_lines.append(line)
    return ret_lines  # returned list is a list of all lines needed to build dictionary


def create_entries(data):
    """ Creates a list of strings where each string contains all information about a specific kanji"""

    ret_list = []
    entry = ""
    for line in data:
        if line != "\n":
            entry += line
        else:
            ret_list.append(entry)
            entry = ""
    return ret_list


def create_dict_keys(entries):
    """ Creates the keys and sub-keys for the dictionary """

    keys = {}
    for i in entries:
        for j in i:
            if (ord(j) >= ord('\u4e00')) and (ord(j) <= ord('\u9faf')):  # all kanji are in this range
                keys[j] = {}
                keys[j]["onyomi"] = []
                keys[j]["kunyomi"] = []
                keys[j]["nanori"] = []
                keys[j]["meaning"] = []
                keys[j]["freq"] = []
                keys[j]["jlpt"] = []
                break
    return keys


def create_dict_vals(keys, entries):
    """ Parses each string in the entries parameter and matches information to their proper places in the dictionary"""
    for i in keys:
        for j in entries:
            if i in j:
                meanings = re.findall(r'<meaning>(.*?)</meaning>', j)
                jlpt = re.findall(r'<jlpt>(.*?)</jlpt>', j)
                freq = re.findall(r'<freq>(.*?)</freq>', j)
                onyomi = re.findall(r'<reading r_type="ja_on">(.*?)</reading>', j)
                kunyomi = re.findall(r'<reading r_type="ja_kun">(.*?)</reading>', j)
                nanori = re.findall(r'<nanori>(.*?)</nanori>', j)
                keys[i]["onyomi"] = onyomi
                keys[i]["kunyomi"] = kunyomi
                keys[i]["nanori"] = nanori
                keys[i]["meaning"] = meanings
                keys[i]["freq"] = freq
                keys[i]["jlpt"] = jlpt
                if not keys[i]["nanori"]:
                    keys[i]["nanori"] = " N/A "
                if not keys[i]["jlpt"]:
                    keys[i]["jlpt"] = " N/A "
                if not keys[i]["onyomi"]:
                    keys[i]["onyomi"] = " N/A "
                if not keys[i]["kunyomi"]:
                    keys[i]["kunyomi"] = " N/A "
                if not keys[i]["meaning"]:
                    keys[i]["meaning"] = " N/A "
                if not keys[i]["freq"]:
                    keys[i]["freq"] = " N/A "
                break


def create_kanji_dict():
    """ Creates the kanji dictionary using the functions above"""

    print("creating kanji_dict...")
    trimmed_data = trim_data()
    print("kanjidic2.xml data trimmed...")
    print("creating kanji_dict keys and values...")
    entries = create_entries(trimmed_data)
    kanji_dict = create_dict_keys(entries)
    create_dict_vals(kanji_dict, entries)
    return kanji_dict


def export_to_json(kanji_dict):
    """ Exports parameter as a json file to be used later"""

    output_dest = open("kanji_dict.json", "w")
    json.dump(kanji_dict, output_dest)
    output_dest.close()


def get_kanji_dict():
    """ Retrieves the kanji dictionary json file if it exists"""

    try:
        ff = open("kanji_dict.json", "rb")
        kanji_dict = json.load(ff)
        ff.close()
        return kanji_dict
    except FileNotFoundError:
        print("kanji_dict.json not found in current directory")
        print("Make sure kanji_dict.json has been created")
        raise FileNotFoundError


# script to build out and export kanji  dictionary
t = time.time()
try:
    f = open("kanjidic2.xml", 'r')
    print("kanjidic2.xml found in directoy")
except FileNotFoundError:
    print("No kanjidic2.xml file in directory.")
    print("Download kanjidic2.xml at http://www.edrdg.org/wiki/index.php/KANJIDIC_Project")
    raise FileNotFoundError

print("reading kanjidic2.xml...")
all_lines = f.readlines()
f.close()
print()

kanji_data = create_kanji_dict()
print("kanji_dict created")
print()

print("exporting to json file...")
export_to_json(kanji_data)
print("data exported to kanji_dict.json")
d = time.time()
print("process completed in " + str(round(d - t, 2)) + " seconds.")
