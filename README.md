#Kanjidicparser

**Kanjidicparser** is a script for parsing data from the KANJIDIC project: 
http://www.edrdg.org/wiki/index.php/KANJIDIC_Project

The script exports a pickle file ("kanji_dict.pickle") containing a nested dictionary 
with data for all kanji entries in the KANJIDIC database.

##Usage

Make sure kanjidic2.xml is downloaded from the KANJIDIC project site into the same directory as the script and 
run the script file. 

##How to use kanji_dict.pickle

kanji_dict.pickle is a nested dictionary where each key is an individual kanji.
Each kanji key links to another dictionary where kanji-specific information.

Example entry: 増

    meanings: 'increase', 'add', 'augment', 'gain', 'promote'
    onyomi: 'ゾウ'
    kunyomi: 'ま.す', 'ま.し', 'ふ.える', 'ふ.やす'
    nanori: 'まし', 'ます'
    freq: '231'
    jlpt: '2'

Accessing information: kanji_dict.pickle loaded into variable _dict_

_dict_["増"]["meanings"] returns the list ['increase', 'add', 'augment', 'gain', 'promote']

##Notes regarding data fields

**meanings** - definitions in English
**onyomi** - readings closer to original Chinese readings, usually used for noun and compounds
**kunyomi** - Japanese readings
**freq** - frequency of occurrence 
**jlpt** - JLPT level 

##License informtion

**kanjidicparser.py** is free to use and modify. Data from the KANJIDIC projects is subject to conditions 
found at http://www.edrdg.org/edrdg/licence.html.

 