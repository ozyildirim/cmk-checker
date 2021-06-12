from utils import Utils
from logger import Logger
from lxml import etree as ET
from xml.dom import minidom


class Checker:

    def __init__(self):
        self.file_path = "cmk_xml_output.xml"
        self.total_empty_functions = 0
        self.total_file_destroy = 0
        self.total_file_instantiate = 0
        self.total_switch = 0
        self.total_hugeTargetFrameSize = 0
        self.total_case = 0
        self.total_getComponent = 0
        self.total_gameObjectFind = 0
        self.total_linq = 0
        self.inputTouch_found = False
        self.is_switch_found = False
        self.is_targetFrameRate_found = False

        self.loggerObj = Logger()

    def StartChecker(self):
        self.sEmptyFunctions()
        self.sInputTouch()
        self.sHugeTargetFrameSize()
        self.sSwitchCase()
        self.sGetComponent()
        self.sDestroyInstantiate()
        self.sGameObjectFind()
        self.sLinq()
        self.final_results()

    def sEmptyFunctions(self):

        # dom = minidom.parse(self.file_path)
        # functions = dom.getElementsByTagName('function')
        # for function in functions:
        #     print(function)
        context = ET.iterparse(self.file_path, events=("start", "end"))

        # turn it into an iterator
        context = iter(context)
        on_function_tag = False
        file_name = ""
        empty_func_counter = 0
        func_names = []
        on_name_tag = False

        for event, elem in context:
            tag = elem.tag
            value = elem.text
            if value:
                value = value.encode('utf-8').strip()

            if tag == '{http://www.srcML.org/srcML/src}unit':
                file_name = elem.get('filename')

            if event == 'start':

                if tag == "function":
                    on_function_tag = True

                if tag == "name" and on_function_tag == True:
                    func_name = value

                elif tag == 'block_content':
                    if on_function_tag:
                        # on_function_block_content_tag = True
                        if value == '':
                            func_names.append(func_name)
                            self.loggerObj.log_smell(
                                file_name + ": empty function detected.")
                            self.total_empty_functions = self.total_empty_functions + 1

            # if event == 'end' and tag == 'block_content':
            # on_function_block_content_tag = False

            if event == 'end' and tag == 'function':
                on_function_tag = False
                on_name_tag = False

            elem.clear()
        print(func_names)

    def sHugeTargetFrameSize(self):

        doc = minidom.parse(self.file_path)

        expr_stmt = doc.getElementsByTagName("expr_stmt")
        name_found = False
        file_name = ""

        for stmt in expr_stmt:
            names = stmt.getElementsByTagName("name")
            for name in names:
                if Utils.getNodeText(name) == "targetFrameRate":
                    name_found = True
                    self.is_targetFrameRate_found = True
                    break
            if name_found:
                try:
                    literal = stmt.getElementsByTagName("literal")[0]
                    if int(Utils.getNodeText(literal)) > 30:
                        self.loggerObj.log_smell(
                            "Application.targetFrameRate is bigger than 30, please consider using value lower than or equal to 30.")
                        self.total_hugeTargetFrameSize = self.total_hugeTargetFrameSize + 1
                except:
                    break

    def sInputTouch(self):

        context = ET.iterparse(self.file_path, events=("start", "end"))
        context = iter(context)
        getTouch_found = False
        touchCount_found = False
        file_name = ""

        for event, elem in context:
            tag = elem.tag
            value = elem.text
            attrib = elem.attrib

            if value:
                value = value.encode('utf-8').strip()

            if tag == '{http://www.srcML.org/srcML/src}unit':
                file_name = elem.get('filename')

            if event == 'start':

                if tag == 'name':
                    if value == b'GetTouch':
                        getTouch_found = True
                        self.loggerObj.log_smell("\n" +
                                                 file_name + ": Input.GetTouch detected.")

                    elif value == b'touchCount':
                        touchCount_found = True
                        self.loggerObj.log_smell("\n" +
                                                 file_name + ": Input.TouchCount detected.")
            elem.clear()

        if getTouch_found == False:
            Logger().log_warning("Ignore if this is not mobile app. Otherwise, you should consider using Input.GetTouch to set touch controllers, https://docs.unity3d.com/ScriptReference/Input.GetTouch.html")
        elif touchCount_found == False:
            Logger().log_warning("Ignore if this is not mobile app. Otherwise, you should consider using Input.TouchCount to set touch controllers, https://docs.unity3d.com/ScriptReference/Input.GetTouch.html")

        if getTouch_found == True or touchCount_found == True:
            self.inputTouch_found = True

    def sSwitchCase(self):

        doc = minidom.parse(self.file_path)
        units = doc.getElementsByTagName("unit")
        for unit in units:
            name = unit.getAttribute("filename")

            switch_count = 0
            case_count = 0

            switches = unit.getElementsByTagName("switch")
            cases = unit.getElementsByTagName("case")

            for switch in switches:
                switch_count += 1

            for case in cases:
                case_count += 1

            if switch_count > 0:
                self.is_switch_found = True
                self.loggerObj.log_smell(name + ": Total switch in document: " + str(switch_count) +
                                         " Total case in document: " + str(case_count))

    def sGetComponent(self):

        self.total_getComponent = 0
        doc = minidom.parse(self.file_path)
        log_array = []
        units = doc.getElementsByTagName("unit")
        for unit in units:
            file_name = unit.getAttribute("filename")
            functions = unit.getElementsByTagName("function")
            for func in functions:
                function_names = func.getElementsByTagName("name")
                for func_name in function_names:
                    if Utils.getNodeText(func_name) == "Update":
                        expr_stmts = func.getElementsByTagName("expr_stmt")
                        for stmt in expr_stmts:
                            expr_names = stmt.getElementsByTagName("name")
                            for exp_name in expr_names:
                                if(Utils.getNodeText(exp_name) == "GetComponent"):
                                    log_array.append(
                                        file_name + ": GetComponent found in Update function.")
                                    self.total_getComponent = self.total_getComponent + 1

                                    break
                        decl_stmts = func.getElementsByTagName("decl_stmt")
                        for stmt in decl_stmts:
                            decl_names = stmt.getElementsByTagName("name")
                            for decl_name in decl_names:
                                if(Utils.getNodeText(decl_name) == "GetComponent"):
                                    log_array.append(
                                        file_name + ": GetComponent found in Update function.")
                                    self.total_getComponent = self.total_getComponent + 1
                                    break
        for i in range(int(len(log_array)/2), int(len(log_array))):
            self.loggerObj.log_smell(log_array[i])
        self.total_getComponent = self.total_getComponent / 2

    def sDestroyInstantiate(self):

        doc = minidom.parse(self.file_path)
        destroy_found = False
        insantiate_found = False

        units = doc.getElementsByTagName("unit")

        for unit in units:
            file_name = unit.getAttribute("filename")
            total_instantiate = 0
            total_destroy = 0

            expr_stmts = unit.getElementsByTagName("expr_stmt")
            decl_stmts = unit.getElementsByTagName("decl_stmt")

            for expr_stmt in expr_stmts:
                expr_names = expr_stmt.getElementsByTagName("name")
                for exp_name in expr_names:
                    if((Utils.getNodeText(exp_name)) == "Instantiate"):
                        insantiate_found = True
                        total_instantiate = total_instantiate + 1
                    elif((Utils.getNodeText(exp_name)) == "Destroy"):
                        destroy_found = True
                        total_destroy = total_destroy + 1

            for decl_stmt in decl_stmts:
                decl_names = decl_stmt.getElementsByTagName("name")
                for decl_name in decl_names:
                    if((Utils.getNodeText(decl_name)) == "Instantiate"):
                        insantiate_found = True
                        total_instantiate = total_instantiate + 1
                    elif((Utils.getNodeText(decl_name)) == "Destroy"):
                        destroy_found = True
                        total_destroy = total_destroy + 1

            if destroy_found and total_destroy >= 2:
                self.loggerObj.log_smell("Total Destroy in " + str(file_name) +
                                         ":" + str(total_destroy))

            if insantiate_found and total_instantiate >= 2:
                self.loggerObj.log_smell("Total Instantiate in " + file_name +
                                         ":" + str(total_instantiate))

            self.total_file_destroy = self.total_file_destroy + total_destroy
            self.total_file_instantiate = self.total_file_instantiate + total_instantiate

    def sGameObjectFind(self):

        doc = minidom.parse(self.file_path)
        log_array = []
        units = doc.getElementsByTagName("unit")
        for unit in units:
            file_name = unit.getAttribute("filename")
            decl_stmt = unit.getElementsByTagName("decl_stmt")
            expr_stmt = unit.getElementsByTagName("expr_stmt")

            if file_name != None:
                for stmt in decl_stmt:
                    dot_operator_found = False
                    gameObject_found = False
                    findFunc_found = False
                    names = stmt.getElementsByTagName("name")
                    operators = stmt.getElementsByTagName("operator")
                    for oper in operators:
                        if Utils.getNodeText(oper) == ".":
                            dot_operator_found = True
                            break
                    for name in names:
                        if Utils.getNodeText(name) == "GameObject":
                            gameObject_found = True
                        elif Utils.getNodeText(name) == "Find":
                            findFunc_found = True
                    if dot_operator_found and gameObject_found and findFunc_found:
                        log_array.append(
                            file_name + ": GameObject.Find detected.")
                        self.total_gameObjectFind = self.total_gameObjectFind + 1

                for stmt in expr_stmt:
                    dot_operator_found = False
                    gameObject_found = False
                    findFunc_found = False
                    names = stmt.getElementsByTagName("name")
                    operators = stmt.getElementsByTagName("operator")
                    for oper in operators:
                        if Utils.getNodeText(oper) == ".":
                            dot_operator_found = True
                            break
                    for name in names:
                        if Utils.getNodeText(name) == "GameObject":
                            gameObject_found = True
                        elif Utils.getNodeText(name) == "Find":
                            findFunc_found = True
                    if dot_operator_found and gameObject_found and findFunc_found:
                        log_array.append(
                            file_name + ": GameObject.Find detected.")
                        self.total_gameObjectFind = self.total_gameObjectFind + 1
        for i in range(int(len(log_array)/2), int(len(log_array))):
            self.loggerObj.log_smell(log_array[i])
        self.total_gameObjectFind = self.total_gameObjectFind / 2

    def sLinq(self):
        doc = minidom.parse('cmk_xml_output.xml')
        log_array = []
        units = doc.getElementsByTagName("unit")
        for unit in units:
            file_name = unit.getAttribute("filename")
            usings = unit.getElementsByTagName("using")
            for using in usings:
                names = using.getElementsByTagName("name")
                for name in names:
                    if Utils.getNodeText(name) == "Linq":
                        # self.loggerObj.log_smell(file_name + ": Linq found.")
                        log_array.append(file_name + ": Linq found.")
                        self.total_linq = self.total_linq + 1

        for i in range(int(len(log_array)/2), int(len(log_array))):
            self.loggerObj.log_smell(log_array[i])
        self.total_linq = self.total_linq / 2

    def final_results(self):
        print("\n\n")
        print("*************ANALYZE RESULTS*************")
        print("\nProject analyze stats are given below.\n")
        if self.is_switch_found:
            self.loggerObj.log_results(
                "Switch-case smells detected in project.")
            self.loggerObj.log_warning(
                "Using switch-case statements cause to smell in applications. Consider not to use them.")
        else:
            self.loggerObj.log_results(
                "There is not Switch-Case Smells in Project")
        if self.total_getComponent == 0:
            self.loggerObj.log_results(
                "There isn't any getComponent, which is located in Update function, found in project.")
        else:
            self.loggerObj.log_results("Total number of GetComponent statement in Update function: " +
                                       str(int(self.total_getComponent)))
        if self.total_empty_functions == 0:
            self.loggerObj.log_results(
                "There isn't any empty function in project.")
        else:
            self.loggerObj.log_results("Total number of empty functions: " +
                                       str(self.total_empty_functions))

        if self.total_hugeTargetFrameSize > 0:
            self.loggerObj.log_results(
                "TargetFrameRate is higher than expected. Please check log file and consider fixing it.")
        elif self.total_hugeTargetFrameSize == 0 and self.is_targetFrameRate_found:
            self.loggerObj.log_results(
                "TargetFrameRate is used as recommended.")
        else:
            self.loggerObj.log_results(
                "There isn't any HugeTargetFrameSize in that project.")

        if self.total_gameObjectFind == 0:
            self.loggerObj.log_results(
                "There isn't any GameObject.Find() found in project.")
        else:
            self.loggerObj.log_results(
                "Total number of GameObject.Find functions: " + str(int(self.total_gameObjectFind)))
        if self.total_file_destroy == 0:
            self.loggerObj.log_results(
                "There isn't any Destroy function in project.")
        else:
            self.loggerObj.log_results(
                "Total number of Destroy function: " + str(self.total_file_destroy))
        if self.total_file_instantiate == 0:
            self.loggerObj.log_results(
                "There isn't any Instantiate function in project.")
        else:
            self.loggerObj.log_results("Total number of Instantiate function: " +
                                       str(self.total_file_instantiate))
        if self.total_linq == 0:
            self.loggerObj.log_results(
                "There isn't any LinQ library found in project.")
        else:
            self.loggerObj.log_results(
                "Linq library is used in that project. Consider not to used it.")

        if self.inputTouch_found == True:
            self.loggerObj.log_results(
                " Input Touch Smell dedected in that project."
            )
        elif self.inputTouch_found == False:
            self.loggerObj.log_results(
                "There is not Input Touch Smell in that project."
            )
        # recommendations
        self.loggerObj.log_warning(
            "Using switch-case statements cause to smell in applications. Consider not to use them.")
        log_file_location = "./log_txt_file.txt"
        print("\n Detailed analyze result is exported as " + log_file_location)
