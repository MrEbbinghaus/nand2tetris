import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from sys import exit

class CompilationEngine:

    def __init__(self, inputXML, show=False, autoSim=True):
        self.list = inputXML.iter()
        self.root = ET.Element("class")
        self.token = next(self.list)
        self.show = show
        self.autoSim = autoSim
        self.outStr = self.compileClass()

    def __str__(self):
        return self.outStr

    def compileClass(self):
        self.token = next(self.list)
        if self.token.tag == "keyword" and self.token.text == "class":
            self.addElement(self.root, "keyword", self.token.text)

        if self.token.tag == "identifier":
            self.addElement(self.root, "identifier", self.token.text)
        else:
            print("ERROR: missing Class-Name")

        if self.token.tag == "symbol" and self.token.text == "{":
            #self.addElement(self.root, "symbol", self.token.text)
            self.token = next(self.list)

        self._compileClassVarDecs(self.root)

        while self.token.text != "}":
            if self.token.text in ("function", "method", "constructor"):
                self._compileSubroutine(self.root)

        # }
        #self.addElement(self.root, self.token.tag, self.token.text)
        self.token = next(self.list)

        out = prettify(self.root)
        if self.show:
            print(out)
        return out

    def _compileClassVarDecs(self, root):
        while self.token.text in ("field", "static"):
            self._compileClassVarDec(root)

    def _compileClassVarDec(self, oldRoot):
        root = self.addElement(oldRoot, "classVarDec")
        self.addElement(root, self.token.tag, self.token.text)

        if self.token.tag in ("identifier", "keyword"):
            self.addElement(root, self.token.tag, self.token.text)
        else:
            print("Error: type of one or more class variables wrong!")
            exit(-1)

        if self.token.tag == "identifier":
            self.addElement(root, self.token.tag, self.token.text)

            while self.token.tag == "symbol" and not self.token.text == ";":
                #,
                self.addElement(root, self.token.tag, self.token.text)
                #identifier
                self.addElement(root, self.token.tag, self.token.text)

            if self.token.text == ";":
                self.addElement(root, self.token.tag, self.token.text)
            elif self.autoSim:
                print("missing ';' , but... who cares?")
                ET.SubElement(root, "symbol").text = ";"
        else:
            print("Error: missing identifier of a class variable")
            exit(-1)

    def _compileSubroutine(self, oldRoot):
        root = self.addElement(oldRoot, "subroutineDec")

        self.addElement(root, self.token.tag, self.token.text)

        if self.token.tag in ("identifier") or self.token.text in ("void", "int", "char", "boolean"):
            self.addElement(root, self.token.tag, self.token.text)

        if self.token.tag in ("identifier"):
            self.addElement(root, self.token.tag, self.token.text)

        #self.addElement(root, self.token.tag, self.token.text)
        self.token = next(self.list)
        self._compileParameterList(root)
        #self.addElement(root, self.token.tag, self.token.text)
        self.token = next(self.list)

        if self.token.text == "{":
            newRoot = self.addElement(root, "subroutineBody")
            #self.addElement(newRoot, self.token.tag, self.token.text)
            self.token = next(self.list)

            self._compileVarDec(newRoot)
            self._compileStatements(newRoot)

            #self.addElement(newRoot, self.token.tag, self.token.text)
            self.token = next(self.list)

    def _compileParameterList(self, oldRoot):
        root = self.addElement(oldRoot, "parameterList")

        if self.token.tag in ("identifier", "keyword"):
            #type
            self.addElement(root, self.token.tag, self.token.text)
            #ident
            self.addElement(root, self.token.tag, self.token.text)

            while self.token.tag == "symbol" and not self.token.text == ")":
                #,
                self.addElement(root, self.token.tag, self.token.text)
                #type
                self.addElement(root, self.token.tag, self.token.text)
                #identifier
                self.addElement(root, self.token.tag, self.token.text)

    def _compileStatements(self, oldRoot):
        root = self.addElement(oldRoot, "statements")
        while self.token.text != "}":
            #print("compile Statement")

            if self.token.text == "let":
                self._compileLet(root)

            elif self.token.text == "do":
                self._compileDo(root)

            elif self.token.text == "return":
                self._compileReturn(root)

            elif self.token.text == "if":
                self._compileIf(root)

            elif self.token.text == "while":
                self._compileWhile(root)

            else:
                print("Error: Unknown Statement:\n"+self.token.text)
                exit(-1)

    def _compileLet(self, oldRoot):
        root = self.addElement(oldRoot, "letStatement")
        self.addElement(root, self.token.tag, self.token.text)
        if self.token.tag == "identifier":
            self.addElement(root, self.token.tag, self.token.text)
            if self.token.text == "[":
                #[
                self.addElement(root, self.token.tag, self.token.text)
                self._compileExpression(root)
                #]
                self.addElement(root, self.token.tag, self.token.text)

            if self.token.text == "=":
                self.addElement(root, self.token.tag, self.token.text)
                self._compileExpression(root)

            if self.token.text == ";":
                self.addElement(root, self.token.tag, self.token.text)
            elif self.autoSim:
                print("missing ';' , but... who cares?")
                ET.SubElement(root, "symbol").text = ";"

    def _compileDo(self, oldRoot):
        root = self.addElement(oldRoot, "doStatement")

        self.addElement(root, self.token.tag, self.token.text)
        self.addElement(root, self.token.tag, self.token.text)
        if self.token.text == ".":
            self.addElement(root, self.token.tag, self.token.text)
            if self.token.tag == "identifier":
                self.addElement(root, self.token.tag, self.token.text)

            else:
                print("identifier in do-Statement expected!")
                exit(-1)
        if self.token.text == "(":
            #(
            self.addElement(root, self.token.tag, self.token.text)
            self._compileExpressionList(root)
            #)
            self.addElement(root, self.token.tag, self.token.text)
        else:
            print("( missing in do-Statement ")
            exit(-1)

        if self.token.text == ";":
            self.addElement(root, self.token.tag, self.token.text)
        elif self.autoSim:
            print("missing ';' , but... who cares?")
            ET.SubElement(root, "symbol").text = ";"

    def _compileIf(self, oldRoot):
        root = self.addElement(oldRoot, "ifStatement")

        self.addElement(root, self.token.tag, self.token.text)
        self.addElement(root, self.token.tag, self.token.text)
        self._compileExpression(root)
        self.addElement(root, self.token.tag, self.token.text)
        self.addElement(root, self.token.tag, self.token.text)
        self._compileStatements(root)
        self.addElement(root, self.token.tag, self.token.text)

        if self.token.text =="else":
            self.addElement(root, self.token.tag, self.token.text)
            self.addElement(root, self.token.tag, self.token.text)
            self._compileStatements(root)
            self.addElement(root, self.token.tag, self.token.text)

    def _compileReturn(self, oldRoot):
        root = self.addElement(oldRoot, "returnStatement")

        self.addElement(root, self.token.tag, self.token.text)

        if self.token.text != ";":
            self._compileExpression(root)


        if self.token.text == ";":
            self.addElement(root, self.token.tag, self.token.text)
        elif self.autoSim:
            print("missing ';' , but... who cares?")
            ET.SubElement(root, "symbol").text = ";"

    def _compileWhile(self, oldRoot):
        root = self.addElement(oldRoot, "whileStatement")

        if self.token.text == "while":
            self.addElement(root, self.token.tag, self.token.text)
            self.addElement(root, self.token.tag, self.token.text)
            self._compileExpression(root)
            self.addElement(root, self.token.tag, self.token.text)
            self.addElement(root, self.token.tag, self.token.text)
            self._compileStatements(root)
            self.addElement(root, self.token.tag, self.token.text)
        else:
            print("Error in while-Statement")
            exit(-1)

    def _compileExpression(self, oldRoot):
        root = self.addElement(oldRoot, "expression")
        self._compileTerm(root)
        while self.token.text in {"+", "-", "*", "/", "&", "|", "<", ">", "="}:
            self.addElement(root, self.token.tag, self.token.text)
            self._compileTerm(root)

    def _compileTerm(self, oldRoot):
        root = self.addElement(oldRoot, "term")

        # ( expression )
        if self.token.text == "(":
            self.addElement(root, self.token.tag, self.token.text)
            self._compileExpression(root)
            self.addElement(root, self.token.tag, self.token.text)

        elif self.token.tag in ("integerConstant", "StringConstant"):
            self.addElement(root, self.token.tag, self.token.text)

        elif self.token.text in ("-", "~"):
            self.addElement(root, self.token.tag, self.token.text)
            self._compileTerm(root)

        elif self.token.text in {"true", "false", "null", "this"}:
            self.addElement(root, self.token.tag, self.token.text)

        # varName [ expression ]?
        elif self.token.tag == "identifier":
            self.addElement(root, "identifier", self.token.text)
            if self.token.text == "[":
                #[
                self.addElement(root, self.token.tag, self.token.text)
                self._compileExpression(root)
                #]
                self.addElement(root, self.token.tag, self.token.text)
            elif self.token.text in {"(", "."}:
                if self.token.text == ".":
                    self.addElement(root, self.token.tag, self.token.text)
                    if self.token.tag == "identifier":
                        self.addElement(root, self.token.tag, self.token.text)

                    else:
                        print("identifier expected!")
                        exit(-1)
                if self.token.text == "(":
                    #(
                    self.addElement(root, self.token.tag, self.token.text)
                    self._compileExpressionList(root)
                    #)
                    self.addElement(root, self.token.tag, self.token.text)

    def _compileExpressionList(self, oldRoot):
        root = self.addElement(oldRoot, "expressionList")

        while self.token.text != ")":
            self._compileExpression(root)
            while self.token.text != ")":
                self.addElement(root, self.token.tag, self.token.text)
                self._compileExpression(root)

    def _compileVarDec(self, oldRoot):
        while self.token.text == "var":
            root = self.addElement(oldRoot, "varDec")
            #var
            self.addElement(root, self.token.tag, self.token.text)
            if self.token.tag in ("identifier", "keyword"):
                #type
                self.addElement(root, self.token.tag, self.token.text)
                #ident
                self.addElement(root, self.token.tag, self.token.text)

                while self.token.tag == "symbol" and not self.token.text == ";":
                    #,
                    self.addElement(root, self.token.tag, self.token.text)
                    #identifier
                    self.addElement(root, self.token.tag, self.token.text)

                if self.token.text == ";":
                    self.addElement(root, self.token.tag, self.token.text)
                elif self.autoSim:
                    print("missing ';' , but... who cares?")
                    ET.SubElement(root, "symbol").text = ";"

    def addElement(self, root, tag, text=None):
        #print("added: Tag: {0}, Text: {1}".format(tag, text))
        lastToken = ET.SubElement(root, tag)
        if text is not None:
            lastToken.text = text
            try:
                self.token = next(self.list)
            except StopIteration:
                print("Done")
        return lastToken

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")