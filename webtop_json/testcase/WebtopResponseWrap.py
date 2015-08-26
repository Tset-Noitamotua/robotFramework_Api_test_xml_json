import re
import xml.etree.ElementTree as ET

class WebtopResponseWrap:

	# XPath Format
	# Element Self: .
	# Children Element: mail/folder/list
	# Children Element Attribute: mail/folder/list/msg/@uid
	elmntPattern = "^(\./)?\w+(/\w+)*$"
	attrPattern = "^(\./)?(\w+/)*@\w+$"
	attrPattern_getElement = "^(\./)?(\w+/)*\w+(\[@\w+=\w*\])*$"

	def __init__(self, responseText, treeElement=None):
		try:
			if treeElement == None:
				self.tree = ET.fromstring(responseText)
			else:
				self.tree = treeElement
		except ET.ParseError, e:
			self.tree = None
			raise Exception("not well-formed xml response.")

	# get text value or attribute value of element by xPath
	def getTextValue(self, xPath, index=0):
		#response xml parse unsuccessfully.
		if self.tree == None:
			return None
		if index < 0:
			raise Exception("index must greater than 0.")
			return None
		#xPath is in element type. e.g. ./mail
		if xPath == "." or re.match(WebtopResponseWrap.elmntPattern,xPath) != None:
			isAttr = False
		#xPath is in attribute type. e.g. ./mail/@action
		elif re.match(WebtopResponseWrap.attrPattern,xPath) != None:
			isAttr = True
		#xPath is not well-formed.
		else:
			raise Exception("not well-formed xPath.")
			return None
		#attribute type xPath
		if isAttr:
			tmpIndex = xPath.index("/@")
			elmnt = self.tree.findall(xPath[0:tmpIndex])[index]
			if elmnt != None:
				return elmnt.attrib[xPath[tmpIndex+2:len(xPath)]]
			else:
				return None
		#element type xPath
		else:
			elmntList = self.tree.findall(xPath)
			if len(elmntList) == 0:
				return None
			elmnt = elmntList[index]
			if elmnt != None:
				return elmnt.text
			else:
				return None

	# get size of subelement by xPath
	def getElementSize(self, xPath):
		#response xml parse unsuccessfully.
		if self.tree == None:
			return -1
		#xPath must be element type. e.g. ./mail
		if xPath == "." or re.match(WebtopResponseWrap.elmntPattern,xPath) != None:
			return len(self.tree.findall(xPath))
		else:
			raise Exception("not an element-type xPath.")
			return -1

	# get list of subelement by xPath
	def getElementList(self, xPath):
		#response xml parse unsuccessfully.
		if self.tree == None:
			return None
		#xPath must be element type. e.g. ./mail
		if re.match(WebtopResponseWrap.elmntPattern,xPath) != None:
			l = list()
			for elmnt in self.tree.findall(xPath):
				l.append(WebtopResponseWrap("",elmnt))
			return l
		else:
			raise Exception("not an element-type xPath.")
			return None

	# get element by xPath
	def getElement(self, xPath, index=0):
		#response xml parse unsuccessfully.
		if self.tree == None:
			return None
		if index < 0:
			raise Exception("index must greater than 0.")
			return None
		#xPath is in element type. e.g. ./mail
		if xPath == "." or re.match(WebtopResponseWrap.attrPattern_getElement,xPath) != None:
			if xPath.find("[@") == -1:
				elmnts = self.tree.findall(xPath)
				if len(elmnts) > index:
					return elmnts[index]
				else:
					return None
			else:
				tmpIndex = xPath.index("[@")
				elmnts = self.tree.findall(xPath[0:tmpIndex])
				attriList = re.findall("@\w+=\w*",xPath[tmpIndex:len(xPath)])
				count = 0
				while(count < len(elmnts)):
					isRemoved = False
					for tmpStr in attriList:
						tmpStr = tmpStr[1:len(tmpStr)]
						tmpArr = tmpStr.split("=")
						tmpVal = elmnts[count].attrib.get(tmpArr[0])
						if tmpVal == None or tmpVal != tmpArr[1]:
							elmnts.remove(elmnts[count])
							isRemoved = True
							break
					if not isRemoved:
						count = count + 1
				if len(elmnts) > index:
					return elmnts[index]
				else:
					return None
		#xPath is not well-formed.
		else:
			raise Exception("not well-formed xPath.")
			return None
		

	# set value for the element by xPath
	def setElementValue(self, xPath, valueText, attrib={}, index=0):
		elmnt = self.getElement(xPath, index)
		if elmnt != None:
			elmnt.text = valueText
			if attrib != None:
				for attribute in attrib:
					if attrib[attribute] != None:
						elmnt.set(attribute, attrib[attribute])
					elif elmnt.attrib.has_key(attribute):
						del elmnt.attrib[attribute]
		else:
			raise Exception("the element to set is None.")

	# add Element by xPath
	def addElement(self, xPath, tag, valueText="", attrib={}, index=0):
		#response xml parse unsuccessfully.
		if self.tree == None:
			raise Exception("the tree is None, please initiate the tree before adding element.")
		if index < 0:
			raise Exception("index must greater than 0.")
		#xPath is in element type. e.g. ./mail
		if xPath == "." or re.match(WebtopResponseWrap.elmntPattern,xPath) != None:
			elmnts = self.tree.findall(xPath)
			if len(elmnts) > index:
				elmnt = elmnts[index]
				newElmnt = ET.SubElement(elmnt, tag, attrib)
				newElmnt.text = valueText
			else:
				raise Exception("index must greater than length of the target elements.")
		else:
			raise Exception("not an element-type xPath.")

	# delete Element by xPath
	def removeElement(self, xPath, index=0):
		#response xml parse unsuccessfully.
		if self.tree == None:
			raise Exception("the tree is None, please initiate the tree before adding element.")
		elmnt = self.getElement(xPath, index)
		if elmnt != None:
			tmpIndex = xPath.rfind("/")
			if tmpIndex == -1:
				parentElmnt = self.tree.getroot()
				parentElmnt.remove(elmnt)
			else:
				parentElmnts = self.tree.findall(xPath[0:tmpIndex])
				if xPath.find("@") == -1:
					tagName = xPath[tmpIndex+1:len(xPath)]
				else:
					tagName = xPath[tmpIndex+1:xPath.find("[")]
				for parentElmnt in parentElmnts:
					for tmpElmnt in parentElmnt.iter(tagName):
						if tmpElmnt == elmnt:
							parentElmnt.remove(elmnt)
							return
		else:
			raise Exception("the element to delete is None.")

	# get Xml text of the tree
	def toXML(self):
		return ET.tostring(self.tree)
