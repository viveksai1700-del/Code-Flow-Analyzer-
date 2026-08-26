import ast


class CodeAnalyzer:

    def __init__(self):
        self.functions = []
        self.loops = []
        self.conditions = []
        self.variables = []
        self.returns = []
        self.prints = []
        self.flow = []

    def analyze_body(self, body):

        for node in body:
            self.analyze_node(node)

    def analyze_node(self, node):

        # FUNCTION
        if isinstance(node, ast.FunctionDef):

            self.functions.append(node.name)

            function_body = []

            previous_flow = self.flow
            self.flow = function_body

            self.analyze_body(node.body)

            self.flow = previous_flow

            self.flow.append({
                "type": "function",
                "label": f"FUNCTION: {node.name}()",
                "children": function_body
            })

            return

        # VARIABLE
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    name = target.id

                    if name not in self.variables:
                        self.variables.append(name)

                    self.flow.append({
                        "type": "variable",
                        "label": f"SET {name}"
                    })

            return

        # IF
        if isinstance(node, ast.If):

            condition = ast.unparse(node.test)

            self.conditions.append(condition)

            yes_flow = []
            no_flow = []

            previous_flow = self.flow

            self.flow = yes_flow
            self.analyze_body(node.body)

            self.flow = no_flow
            self.analyze_body(node.orelse)

            self.flow = previous_flow

            self.flow.append({
                "type": "condition",
                "label": f"IF {condition}",
                "yes": yes_flow,
                "no": no_flow
            })

            return

        # FOR
        if isinstance(node, ast.For):

            target = ast.unparse(node.target)

            self.loops.append(
                f"for {target}"
            )

            loop_body = []

            previous_flow = self.flow
            self.flow = loop_body

            self.analyze_body(node.body)

            self.flow = previous_flow

            self.flow.append({
                "type": "loop",
                "label": f"FOR {target}",
                "children": loop_body
            })

            return

        # WHILE
        if isinstance(node, ast.While):

            condition = ast.unparse(node.test)

            self.loops.append(
                f"while {condition}"
            )

            loop_body = []

            previous_flow = self.flow
            self.flow = loop_body

            self.analyze_body(node.body)

            self.flow = previous_flow

            self.flow.append({
                "type": "loop",
                "label": f"WHILE {condition}",
                "children": loop_body
            })

            return

        # RETURN
        if isinstance(node, ast.Return):

            self.returns.append(
                "return statement"
            )

            self.flow.append({
                "type": "return",
                "label": "RETURN"
            })

            return

        # PRINT / FUNCTION CALL
        if isinstance(node, ast.Expr):

            value = node.value

            if isinstance(value, ast.Call):

                if isinstance(value.func, ast.Name):

                    function_name = value.func.id

                    if function_name == "print":

                        self.prints.append(
                            "print statement"
                        )

                        self.flow.append({
                            "type": "output",
                            "label": "OUTPUT"
                        })

                    else:

                        self.flow.append({
                            "type": "call",
                            "label": f"CALL {function_name}()"
                        })

            return


def analyze_code(code):

    try:

        tree = ast.parse(code)

        analyzer = CodeAnalyzer()

        analyzer.analyze_body(tree.body)

        return {
            "success": True,
            "functions": analyzer.functions,
            "loops": analyzer.loops,
            "conditions": analyzer.conditions,
            "variables": analyzer.variables,
            "returns": analyzer.returns,
            "prints": analyzer.prints,
            "flow": analyzer.flow
        }

    except SyntaxError as error:

        return {
            "success": False,
            "error": f"Syntax error: {error}"
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }