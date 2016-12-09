
# Simple xml parser for salesforce object file .object

import xml.etree.ElementTree as ET
import sys
import os
import pprint
from os.path import isfile, join

class CustomField:
    def __init__(self, name):
        self.FieldName = name
        self.details = {}

    def isLookupField(self):
        myType = self.details.get('type')
        if(myType == 'Lookup') :
            return True;
        return False;

    def isMasterDetailField(self):
        myType = self.details.get('type')
        if(myType == 'MasterDetail') :
            return True;
        return False;

    def lookupParent(self) :
        if(self.isLookupField()) :
            parentClass = self.details.get('referenceTo')
            relationShipName = self.details.get('relationshipName')
            return {"parent": parentClass, "relation" : relationShipName}

    def masterDetailParent(self) :
        if(self.isMasterDetailField()) :
            parentClass = self.details.get('referenceTo')
            relationShipName = self.details.get('relationshipName')
            return {"parent": parentClass, "relation" : relationShipName}





    def setDescription(self, descr):
        self.Description = descr

    def addDetail(self, key, value):
        self.details.update({key:value})

    def display(self):
        isRelationShip = self.details.get('isRelationShip', 'not-present')
        myType = self.details.get('type')
        #print "display:\t", myType,  " " , self.FieldName , " isRelationShip:" , isRelationShip
        #print "Description = ", self.Description
        #for key, value in self.details.iteritems() :
        #    print "Key = " , key , "\tValue ", value

    def dumpSimpleMember(self):
        #print 'dumpSimpleMember(): ', self.FieldName
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

        if(type == 'LongTextArea') :
            memberString += "String " + self.FieldName + ";"
            return memberString

        if(type == 'Picklist') :
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
            return memberString

        if(type == 'ID') :
            memberString  += "ID " + self.FieldName + ";"
            return memberString

        if(type == 'Lookup') :
            referenceClass =  self.details.get('referenceTo', 'not-present')
            memberString += referenceClass + " " + self.FieldName + ";"
            return memberString

        if(type == 'MasterDetail') :
            referenceClass =  self.details.get('referenceTo', 'not-present')
            memberString += referenceClass + " " + self.FieldName + ";"
            return memberString

        return ""

    def dumpRelationShipMember(self) :
        #print 'dumpRelationShipMember(): ', self.FieldName
        type = self.details.get('type', 'not-present')
        label = self.details.get('label', 'not-present')
        #memberString = "\t// " + self.Description
        memberString = "\t// " + label
        memberString += "\n\t"

        listStr = 'List<' + type + '>'
        memberString += listStr + " " + self.FieldName + ";"
        return memberString

    def dumpJavaMember(self) :
        isRelationShip = self.details.get('isRelationShip', 'not-present')
        if(isRelationShip == 'true') :
            return self.dumpRelationShipMember()
        else :
            return self.dumpSimpleMember()

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
        self.lookupFields = []
        self.masterDetailFields = []
        SFObject.count  += 1
        self.addIdField()
        self.addNameField()
        self.addVariousDateFields()
        #self.addVariousReferenceFields()

    def objectName(self) :
        return self.Name

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

    def addRelationListField(self, childType, relationShipName) :
        #print 'adding relationship to ', self.Name, ' relationshipname = ', relationShipName , ' childtype = ', childType

        fName = relationShipName + '__r'
        relationField = CustomField(fName);
        relationField.addDetail('label', fName)
        relationField.addDetail('type', childType)
        relationField.addDetail('isRelationShip', 'true')
        self.addField(relationField)


    def addVariousDateFields(self) :
        for df in SFObject.StandardDateFields :
            dateField = CustomField(df)
            dateField.addDetail('label', df)
            dateField.addDetail('type', 'Date')
            self.addField(dateField)

    def addField(self, cfield):
        self.fields.append(cfield)
        if(cfield.isLookupField()) :
            self.lookupFields.append(cfield)
        if(cfield.isMasterDetailField()) :
            self.masterDetailFields.append(cfield)

    def getLookupFields(self):
        return self.lookupFields

    def getMasterDetailFields(self):
        return self.masterDetailFields

    def display(self):
        print "Object name : ", self.Name
        for cf in self.fields :
            cf.display()


    #print the object class
    def dumpJavaClass(self, dir) :
        ocName = self.Name + '.cls'
        ocPath = os.path.join(dir, ocName)
        #print 'ocPath = ', ocPath
        oc = open(ocPath, "w")

        oc.write("//This is automated geneerated file!! \n\n")

        classString = "\npublic class " + self.Name + "\t extends sObject {"

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
        cfield.addDetail('externalId', externalId)

        #get the label
        label = fields.find('customObject:label', ns).text
        cfield.addDetail('label', label)

        mytype = fields.find('customObject:type', ns).text
        cfield.addDetail('type', mytype)

        if(mytype == 'Lookup' or mytype == 'MasterDetail') :
            referenceClass = fields.find('customObject:referenceTo', ns).text
            relationshipName = fields.find('customObject:relationshipName', ns).text
            #relationshipLabel = fields.find('customObject:relationshipLabel', ns).text
            cfield.addDetail('referenceTo', referenceClass)
            cfield.addDetail('relationshipName', relationshipName)
            #cfield.addDetail('relationshipLabel', relationshipLabel)


        #print 'custom field is :'
        #cfield.display()

        object.addField(cfield)

    return object

def updateRelationShip(parentmap, objectName, parentChildObjectMap) :
    parentC = parentmap.get("parent")
    relationShipName = parentmap.get("relation")

    #print 'populateParentChildObjectMap():  objectName= ',objectName , 'parentC= ', parentC, 'relationShipName= ', relationShipName

    if(parentChildObjectMap.has_key(parentC)) :
        relationShipMap = parentChildObjectMap.get(parentC)

        if(relationShipMap.has_key(objectName)) :
            relationShipList = relationShipMap.get(objectName)
            relationShipList.append(relationShipName)
        else :
            relationShipList = [relationShipName]
            relationShipMap.update({objectName : relationShipList})
    else :
        relationShipList = [relationShipName]

        relationShipMap = {objectName : relationShipList}
        parentChildObjectMap.update({parentC:relationShipMap})


def populateParentChildObjectMap(objectList) :

    parentChildObjectMap = {}

    for object in objectList :
        objectName = object.objectName()

        lookupFields = object.getLookupFields()
        for lField in lookupFields :
            map = lField.lookupParent()
            updateRelationShip(map, objectName, parentChildObjectMap)

        masterDetailFields = object.getMasterDetailFields()
        for lField in masterDetailFields :
            map = lField.masterDetailParent()
            updateRelationShip(map, objectName, parentChildObjectMap)


    #pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(parentChildObjectMap)

    return parentChildObjectMap




def createPoJoForSFObject(objDir, targetDir):

    objectList = []


    print 'Target directory is: ', targetDir
    print 'Object directory is: ', objDir

    files = os.listdir(objDir)

    for ff in files :
        #print 'ff = ', ff
        objectName = ff.replace('.object', '')
        #print 'objectName = ', objectName
        fullff =  os.path.join(objDir, ff)
        #print 'fullff = ', fullff
        tree = ET.parse(fullff)
        root = tree.getroot()
        object =  getParsedObject(root, objectName)
        objectList.append(object)
        #object.display()
        #object.dumpJavaClass(targetDir)

    #find all the objects which refer to each other

    parentChildObjectMap1 = populateParentChildObjectMap(objectList)
    pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(parentChildObjectMap1)

    objectNameMap = {}
    for obj in objectList :
        objectNameMap.update({obj.objectName():obj})

    for objName in parentChildObjectMap1.keys() :
        if(objectNameMap.has_key(objName) == False) :
            object1 = SFObject(objName)
            objectNameMap.update({objName:object1})

    #pp.pprint(objectNameMap)

    for parentName in parentChildObjectMap1.keys() :
        relations = parentChildObjectMap1.get(parentName)
        parentObj = objectNameMap.get(parentName)

        numRelationShips = 0
        for childType in relations.keys() :
            numRelationShips += 1
            relationShipList = relations.get(childType)
            for relationShipName in relationShipList :
                parentObj.addRelationListField(childType, relationShipName)


    print "creating java classes..."
    for objName in objectNameMap.keys() :
        object = objectNameMap.get(objName)
        #object.display()
        object.dumpJavaClass(targetDir)





#objDir = sys.argv[1]
#targetDir = sys.argv[2]
#createPoJoForSFObject(objDir, targetDir)
















