import re
import json
import sys
import getopt
import os


def main(argv):
    input_file, entity_dictionary, entity_type_file = '', dict(), ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:e:", ["ifile=", "dfile=", "efile="])
    except getopt.GetoptError:
        print('correctOutput.py -i <inputTEXTfile> -d <inputFolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('correctOutput.py -i <inputTEXTfile> -d <inputFolder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-d", "--dfile"):
            if arg[-1] != "/": arg += '/'
            entity_dictionary = json.load(open(arg + "dict.json", encoding="utf-8"))
            entity_type_file = [abc.rstrip() + "[\d]+" for abc in open(arg + "entityTypes.txt", encoding="utf-8")]
    if len(opts) < 2:
        print("Number of arguments should be 2. Type '-h' for help")
        sys.exit(2)

    output_folder = "/".join(input_file.split("/")[:-1]) + "/"
    input_file_name = input_file.split("/")[-1][2:]
    pattern_string = "|".join(entity_type_file)

    pattern = re.compile(pattern_string)
    f1 = open(input_file, encoding="utf-8")
    f2 = open(output_folder + input_file_name, 'w', encoding="utf-8")
    for l in f1:
        matches = re.findall(pattern, l)
        allMatchesFound = True
        for match in matches:
            key_word = re.sub(r'([A-Z]+[\d]+)', r'\1', match)
            if key_word in entity_dictionary:
                l = l.replace(match, entity_dictionary[key_word])
            else:
                allMatchesFound = False
                break
        if allMatchesFound:
            f2.write(l)
    f2.close()
    f1.close()
   # os.remove(input_file)


if __name__ == "__main__":
    main(sys.argv[1:])

