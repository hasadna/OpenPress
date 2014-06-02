__author__ = 'asafvaladarsky'
from lxml import etree
from os import walk, sep, path
from logging import info, warning

def main(mainFolderName,schemaFileName, shouldRecursiveSearch):
    with open(schemaFileName) as schemaFile:
        schemaText = schemaFile.read()

    xmlschema = etree.XMLSchema(etree.parse(schemaFileName))

    filesList = []

    recursiveSearch = True if shouldRecursiveSearch != "0" else False

    for root, dirs, files in walk(mainFolderName):
        for file_name in files:
            if file_name.lower().endswith(".xml"):
                #with open(file_name) as xmlFile:
               filesList.append(path.join(root, file_name))
        if not recursiveSearch:
            print "breaking"
            break

    for fileName in filesList:
        doc = etree.parse(fileName)
        xmlschema.assertValid(doc)
        if not xmlschema.validate(doc):
            warning('File %s does not pass validation %s' % (file_name,schemaFileName))
        else:
            info("File %s passed validation: %s" % (file_name,schemaFileName))


if __name__ == "__main__":
    from sys import argv
    main(argv[1], argv[2], argv[3])