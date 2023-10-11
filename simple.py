import random

from pkb import PKB
pkb = PKB()

class Entity:
    def serialise(self, indent_level=0):
        pass

class Operator(Entity):
    def __init__(self, symbol):
        self.symbol = symbol

    def serialise(self, indent_level=0):
        return self.symbol
    
class BooleanOperator(Operator):
    pass

class Expression(Entity):
    def __init__(self, left_term, operator=None, right_term=None):
        self.left_term = left_term
        self.operator = operator
        self.right_term = right_term

    def serialise(self, indent_level=0):
        if self.operator is not None:
            return f"{self.left_term.serialise()} {self.operator.serialise()} {self.right_term.serialise()}"
        
        return self.left_term.serialise()
    
class BooleanExpression(Expression):
    pass

class Term(Entity):
    def serialise(self, indent_level=0):
        pass

class Variable(Term):
    def __init__(self, name):
        self.name = name

    def serialise(self, indent_level=0):
        return self.name

class Constant(Term):
    def __init__(self, value):
        self.value = value

    def serialise(self, indent_level=0):
        return str(self.value)
    
class Bracket(Term):
    def __init__(self, expression):
        self.expression = expression

    def serialise(self, indent_level=0):
        return f"({self.expression.serialise()})"

class Procedure(Entity):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def serialise(self, indent_level=0):
        statement_list = self.statements.serialise(indent_level + 1)
        indentation = " " * (indent_level * 4)
        return f"{indentation}procedure {self.name} {{\n{statement_list}\n{indentation}}}\n"

class StatementList(Entity):
    def __init__(self, statements):
        self.statements = statements

    def serialise(self, indent_level=0):
        serialized_statements = [statement.serialise(indent_level) for statement in self.statements]
        return "\n".join([f"{line}" for line in serialized_statements])

class Statement(Entity):
    def __init__(self):
        self.line_number = 0

    def serialise(self, indent_level=0):
        pass

class CallStatement(Statement):
    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        return f"{indentation}call {self.procedure_name};"

class PrintStatement(Statement):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        return f"{indentation}print {self.variable_name};"

class ReadStatement(Statement):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        return f"{indentation}read {self.variable_name};"

class IfStatement(Statement):
    def __init__(self, condition, if_statements, else_statements):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        code = (
            f"{indentation}if ({self.condition.serialise()}) then {{\n"
            f"{self.if_statements.serialise(indent_level + 1)}\n"
            f"{indentation}}} else {{\n"
            f"{self.else_statements.serialise(indent_level + 1)}\n"
            f"{indentation}}}"
        )
        return code
    
class WhileStatement(Statement):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        code = (
            f"{indentation}while ({self.condition.serialise()}) {{\n"
            f"{self.statements.serialise(indent_level + 1)}\n"
            f"{indentation}}}"
        )
        return code
    
class AssignStatement(Statement):
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression

    def serialise(self, indent_level=0):
        indentation = " " * (indent_level * 4)
        return f"{indentation}{self.variable_name} = {self.expression.serialise()};"

class EntityFactory:
    def generate(self):
        pass

class VariableFactory(EntityFactory):
    def generate(self):
        if ReadStatementFactory.variable_count == 0:
            return Variable("var_1")
        else:
            variable_number = random.randint(1, ReadStatementFactory.variable_count)
            return Variable(f"var_{variable_number}")

class BracketFactory(EntityFactory):
    def generate(self):
        expression = ExpressionFactory().generate()
        return Bracket(expression)
    
class TermFactory(EntityFactory):
    def generate(self):
        term_type = random.choice([ConstantFactory, VariableFactory, BracketFactory])
        return term_type().generate()
    
class OperatorFactory(EntityFactory):
    def generate(self):
        operator = random.choice(['+', '-', '*'])
        return Operator(operator)
    
class BooleanOperatorFactory(EntityFactory):
    def generate(self):
        symbol = random.choice(['==', '>', '<', '!='])
        return BooleanOperator(symbol)

class ConstantFactory(EntityFactory):
    def generate(self):
        return Constant(random.randint(1, 100))

class ExpressionFactory(EntityFactory):
    def generate(self):
        if random.random() > TERM_CHANCE:
            left_term = TermFactory().generate()
            operator = OperatorFactory().generate()
            right_term = TermFactory().generate()
            return Expression(left_term, operator, right_term)
        else:
            return TermFactory().generate()
        
class BooleanExpressionFactory(EntityFactory):
    def generate(self):
        left_expr = ExpressionFactory().generate()
        boolean_operator = BooleanOperatorFactory().generate()
        right_expr = ExpressionFactory().generate()
        return BooleanExpression(left_expr, boolean_operator, right_expr)

class ProcedureFactory(EntityFactory):
    current_count = 0

    def generate(self):
        ProcedureFactory.current_count += 1
        procedure_name = f"proc_{self.current_count}"

        statement_list = StatementListFactory().generate()
        procedure = Procedure(procedure_name, statement_list)
        return procedure

class StatementListFactory(EntityFactory):
    def generate(self, statements=None):
        if statements is None:
            statements = [ReadStatementFactory().generate()]

        while random.random() < roll():
            statement_factory = random.choices(
                [
                    CallStatementFactory,
                    PrintStatementFactory,
                    ReadStatementFactory,
                    AssignStatementFactory,
                    IfStatementFactory,
                    WhileStatementFactory
                 ],
                weights = (20, 20, 20, 20, 7 * BRANCH_FACTOR, 7 * BRANCH_FACTOR))[0]
            statements.append(statement_factory().generate())

        return StatementList(statements)

from functools import wraps

class TrackCallsDecorator:
    def __init__(self, pkb):
        self.pkb = pkb

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            statement = func(*args, **kwargs)

            if isinstance(statement, CallStatement):
                current_procedure = "proc_" + str(ProcedureFactory.current_count)
                procedure_name = statement.procedure_name
                pkb.add_relationship(("calls", current_procedure, procedure_name))

            return statement
        return wrapper
    
def track_calls(pkb):
    return TrackCallsDecorator(pkb)

class CallStatementFactory(EntityFactory):
    @track_calls(pkb)
    def generate(self):
        if ProcedureFactory.current_count == 1:
            return ReadStatement('PASS')
        
        procedure_name = f"proc_{random.randint(1, ProcedureFactory.current_count - 1)}"
        return CallStatement(procedure_name)

class PrintStatementFactory(EntityFactory):
    def generate(self):
        if ReadStatementFactory.variable_count == 0:
            return ReadStatementFactory.generate()
        
        variable_name = f"var_{random.randint(1, ReadStatementFactory.variable_count)}"
        return PrintStatement(variable_name)

class ReadStatementFactory(EntityFactory):
    variable_count = 0

    def generate(self):
        ReadStatementFactory.variable_count += 1
        variable_name = f"var_{ReadStatementFactory.variable_count}"
        return ReadStatement(variable_name)

class IfStatementFactory(EntityFactory):
    def generate(self):
        condition = BooleanExpressionFactory().generate()
        if_statements = StatementListFactory().generate()
        else_statements = StatementListFactory().generate()
        return IfStatement(condition, if_statements, else_statements)
    
class WhileStatementFactory(EntityFactory):
    def generate(self):
        condition = BooleanExpressionFactory().generate()
        statements = StatementListFactory().generate()
        return WhileStatement(condition, statements)

class AssignStatementFactory(EntityFactory):
    def generate(self):
        if ReadStatementFactory.variable_count == 0:
            return ReadStatementFactory.generate()
        
        variable_name = f"var_{random.randint(1, ReadStatementFactory.variable_count)}"
        expression = ExpressionFactory().generate()
        return AssignStatement(variable_name, expression)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIMPLE generator", epilog='e.g.: python3 simple.py -l 1.0 -b 0.1 -e 0.9')
    
    
    parser.add_argument(
        "-n",
        type = int,
        default = 5,  
        help = "Number of procedures. Default 5."
    )
    parser.add_argument(
        "-l",
        type = float,
        default = 0.8,
        help = "Statement length factor. Higher value gives longer statement lists. Increasing this indirectly increases nesting depth. 0.0-1.0. Default 0.8."
    )
    parser.add_argument(
        "-b",
        type = float,
        default = 1.0,
        help = "Statement branch factor. 1x is the default probability for any statement to be a if/while. Anything beyond ~1.5 is ridiculous. Default 1.0."
    )
    parser.add_argument(
        "-e",
        type = float,
        default = 0.5,
        help = "Expression expansion probability. Higher value gives more branched expressions. 0.0-1.0. Default 0.5."
    )

    args = parser.parse_args()
    
    TERM_CHANCE = 1-args.e
    APPEND_CHANCE = args.l
    BRANCH_FACTOR = args.b
    DECAY = 0.9999
    def roll():
        global APPEND_CHANCE
        APPEND_CHANCE *= DECAY
        return APPEND_CHANCE


    p = ProcedureFactory()
    buffer = ""
    for _ in range(args.n):
        buffer += p.generate().serialise()
        with open('generate.in', 'w') as f:
            f.write(buffer)
    
    with open('truths.out', 'w') as f:
        f.write(')\n('.join(str(list(pkb.relationships)).split('), (')))