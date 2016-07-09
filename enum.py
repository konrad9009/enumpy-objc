#!/usr/bin/python

import getopt
import re
import sys

USAGE = 'enum.py -i <input_file> -n <name>'

SCHEME_NS_ENUM = '''typedef NS_ENUM(NSUInteger, %s) {\n%s};'''
SCHEME_NS_DICTIONARY = '''@{\n%s};'''


class EnumElement:
    def __init__(self, original_name, processed_name, comment=None):
        self.original_name = original_name
        self.processed_name = processed_name
        self.comment = comment

    def string_value(self, int_value=''):
        comment = ' // ' + self.comment if self.comment else ''
        return '%s%s,%s' % (self.processed_name, int_value, comment)


class Enum:
    def __init__(self, name):
        self.name = name
        self.elements = list()

    def add_element(self, element):
        self.elements.append(element)

    def string_value(self):
        string_elements = ''
        for i, e in enumerate(self.elements):
            string_elements += '\t%s\n' % (e.string_value(' = 1') if i == 0 else e.string_value())
        return SCHEME_NS_ENUM % (self.name, string_elements)

    def value_transformer_string(self):
        items = ''.join('\t@"%s" : @(%s),\n' % (e.original_name, e.processed_name) for e in self.elements)
        return SCHEME_NS_DICTIONARY % items


def camelize(string):
    return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)


def process_file(input_file, name):
    enum = Enum(name)
    with open(input_file) as f:
        for line in f:
            elements = line.split(',')
            original = elements[0].strip()
            processed = name + camelize(original.lower())
            comment = elements[1].strip() if len(elements) > 0 else None
            enum.add_element(EnumElement(original, processed, comment))
    return enum


def main(argv):
    input_file = ''
    name = ''
    try:
        opts, args = getopt.getopt(argv, "hi:n:", ["input=", "name="])
    except getopt.GetoptError:
        print USAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print USAGE
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-n", "--name"):
            name = arg

    enum = process_file(input_file, name)
    print 'enum:\n', enum.string_value()
    print 'transformer dict:\n', enum.value_transformer_string()


if __name__ == "__main__":
    main(sys.argv[1:])
