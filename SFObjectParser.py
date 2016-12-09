
# Simple xml parser for salesforce object file .object

import xml.etree.ElementTree as ET
import sys
import os
from os.path import isfile, join

class CustomField:
    def __init__(self, name):
        self.FieldName = name
        self.details = {}

    def setDescription(self, descr):
        self.Description = descr

    def addDetail(self, key, value):
        self.details.update({key:value})

    def display(self):

        myType = self.details.get('type')
        print "display:\t", myType,  " " , self.FieldName
        #print "Description = ", self.Description
        #for key, value in self.details.iteritems() :
        #    print "Key = " , key , "\tValue ", value

    def dumpJavaMember(self):
        type = self.details.get('type', 'not-present')
        label = self.details.get('label', 'not-present')
        #memberString = "\t// " + self.Description
        memberString = "\t// " + label
        memberString += "\n\t"
        if(type == 'not-present') :
            print 'type is not present for ', self.FieldName
            return ""

        if(type == 'Text') :
            memberString += "String " + self.FieldName + ";"
            return memberString

        if(type == 'Date') :
            memberString  += "Date " + self.FieldName + ";"
            return memberString

        if(type == 'DateTime') :
            memberString  += "Date " + self.FieldName + ";"
            return memberString

        if(type == 'Checkbox') :
            memberString  += "boolean " + self.FieldName + ";"
            return memberString

        if(type == 'Number') :
            memberString  += "double " + self.FieldName + ";"
            return memberString;

        if(type == 'ID') :
            memberString  += "ID " + self.FieldName + ";"
            return memberString;

        return ""
        #if(type == 'Lookup') :
        #    print 'lookup not supported yet'
        #    return ""

        #if(type == 'Picklist') :
        #    print 'Picklist not supported yet'
        #    return ""

class SFObject:

    StandardFields = ["Id",
                       "IsDeleted",
                       "CreatedById",
                       "CreateDate",
                       "LastModifiedById",
                       "LastModifiedDate",
                       "SystemModstamp",
                       "Name"
                     ]

    StandardDateFields = ["CreateDate",
                          "LastModifiedDate",
                          "SystemModstamp"
                         ]
    count = 0

    def __init__(self, name):
        self.Name = name
        self.fields = []
        SFObject.count  += 1
        self.addIdField()
        self.addNameField()
        self.addVariousDateFields()
        #self.addVariousReferenceFields()

    def addIdField(self) :
        idField = CustomField('Id');
        idField.addDetail('label', 'Salesforce Identifier')
        idField.addDetail('type', 'ID')
        self.addField(idField)

    def addNameField(self) :
        nameField = CustomField('Name');
        nameField.addDetail('label', 'Name')
        nameField.addDetail('type', 'Text')
        self.addField(nameField)

    def addVariousDateFields(self) :
        for df in SFObject.StandardDateFields :
            dateField = CustomField(df)
            dateField.addDetail('label', df)
            dateField.addDetail('type', 'Date')
            self.addField(dateField)

    def addField(self, cfield):
        self.fields.append(cfield)

    def display(self):
        print "Object name : ", self.Name
        for cf in self.fields :
            cf.display()


    #print the object class
    def dumpJavaClass(self, dir) :
        ocName = self.Name + '.cls'
        ocPath = os.path.join(dir, ocName)
        print 'ocPath = ', ocPath
        oc = open(ocPath, "w")

        oc.write("//This is automated geneerated file!! \n\n")

        classString = "\npublic class " + self.Name + "\t extends SalesForceObject {"

        oc.write(classString)
        oc.write("\n\t//")
        oc.write("\n\t//this is body of class")
        oc.write("\n\t//")
        oc.write("\n\n")

        oc.write("\n\t// Custom fields")
        oc.write("\n\t//")
        oc.write("\n\n")

        for cf in self.fields :
            memberString = cf.dumpJavaMember()
            #print 'memberstring = :',memberString,':'
            oc.write(memberString)
            oc.write("\n\n")

        oc.write("}")
        oc.close()


def getParsedObject(oroot, objectName) :

    object = SFObject(objectName)

    ns = {'customObject' : 'http://soap.sforce.com/2006/04/metadata',

         }



    for fields in oroot.findall('customObject:fields', ns):
        #get the full name
        fullName = fields.find('customObject:fullName', ns).text
        cfield = CustomField(fullName)

        #get the description
        #description = fields.find('customObject:description', ns).text
        #cfield.setDescription(description)

        #get the externalId flag
        externalId = fields.find('customObject:externalId', ns).text

        #get the label
        label = fields.find('customObject:label', ns).text

        mytype = fields.find('customObject:type', ns).text

        cfield.addDetail('label', label)
        cfield.addDetail('type', mytype)
        cfield.addDetail('externalId', externalId)

        #print 'custom field is :'
        #cfield.display()

        object.addField(cfield)

    return object



def createPoJoForSFObject(objDir, targetDir):

    print 'Target directory is: ', targetDir
    print 'Object directory is: ', objDir

    files = os.listdir(objDir)

    for ff in files :
        print 'ff = ', ff
        objectName = ff.replace('.object', '')
        print 'objectName = ', objectName
        fullff =  os.path.join(objDir, ff)
        print 'fullff = ', fullff
        tree = ET.parse(fullff)
        root = tree.getroot()
        object =  getParsedObject(root, objectName)
        #object.display()
        object.dumpJavaClass(targetDir)


objDir = sys.argv[1]
targetDir = sys.argv[2]
#ffname = os.path.join(objDir, 'fname.cls')
#print 'ffname = ', ffname

createPoJoForSFObject(objDir, targetDir)










