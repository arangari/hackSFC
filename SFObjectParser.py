
# Simple xml parser for salesforce object file .object

import xml.etree.ElementTree as ET

tree = ET.parse('Loan_Account__c.object')
root = tree.getroot()

#for child in root:
#    print "tag = " , child.tag
#    print "attrib = ", child.attrib

ns = {'customObject' : 'http://soap.sforce.com/2006/04/metadata',

     }

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

        return ""
        #if(type == 'Lookup') :
        #    print 'lookup not supported yet'
        #    return ""

        #if(type == 'Picklist') :
        #    print 'Picklist not supported yet'
        #    return ""





class SFObject:
    Name = 'some-name'
    fields = []
    def __init__(self, name):
        self.Name = name

    def addField(self, cfield):
        self.fields.append(cfield)

    def display(self):
        print "Object name : ", self.Name
        for cf in self.fields :
            cf.display()

    #print the object class
    def dumpJavaClass(self) :
        ocName = self.Name + '.cls'
        oc = open(ocName, "w")

        oc.write("//This is automated geneerated file!! \n\n")

        classString = "public class " + self.Name + "\t extends SalesForceObject {"



        oc.write(classString)
        oc.write("\n\t//")
        oc.write("\n\t//this is body of class")
        oc.write("\n\t//")
        oc.write("\n\n")
        for cf in self.fields :
            memberString = cf.dumpJavaMember()
            print 'memberstring = :',memberString,':'
            oc.write(memberString)
            oc.write("\n\n")

        oc.write("}")
        oc.close()

loanAccount = SFObject('Loan_Account__c')


for fields in root.findall('customObject:fields', ns):
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

    loanAccount.addField(cfield)


#print 'loanAccount = '
#loanAccount.display()
loanAccount.dumpJavaClass()






