from typing import List

from pkb import PKB
pkb = PKB()

class Entity:
    def serialise(self, indent_level: int = 0) -> str:
        pass

class Operator(Entity):
    def __init__(self, symbol: str):
        self.symbol = symbol

    def serialise(self, indent_level: int = 0) -> str:
        return self.symbol

class Expression(Entity):
    def __init__(self, left_term: 'Term', operator: str, right_term: 'Term'):
        self.left_term = left_term
        self.operator = operator
        self.right_term = right_term

    def serialise(self, indent_level: int = 0) -> str:
        return f"{self.left_term.serialise()} {self.operator} {self.right_term.serialise()}"

class Term(Entity):
    def serialise(self, indent_level: int = 0) -> str:
        pass

class Variable(Term):
    def __init__(self, name: str):
        self.name = name

    def serialise(self, indent_level: int = 0) -> str:
        return self.name

class Constant(Term):
    def __init__(self, value: str):
        self.value = value

    def serialise(self, indent_level: int = 0) -> str:
        return self.value

class Procedure(Entity):
    def __init__(self, name: str, statements: 'StatementList') -> None:
        self.name = name
        self.statements = statements

    def serialise(self, indent_level: int = 0) -> str:
        statement_list = self.statements.serialise(indent_level + 1)
        indentation = " " * (indent_level * 4)
        return f"{indentation}procedure {self.name} {{\n{statement_list}\n{indentation}}}\n"

class StatementList(Entity):
    def __init__(self, statements: List['Statement']) -> None:
        self.statements = statements

    def serialise(self, indent_level: int = 0) -> str:
        serialized_statements = [statement.serialise(indent_level) for statement in self.statements]
        return "\n".join([f"{line}" for line in serialized_statements])

class Statement(Entity):
    def __init__(self) -> None:
        self.line_number = 0

    def serialise(self, indent_level: int = 0) -> str:
        pass

class CallStatement(Statement):
    def __init__(self, procedure_name: str) -> None:
        self.procedure_name = procedure_name

    def serialise(self, indent_level: int = 0) -> str:
        indentation = " " * (indent_level * 4)
        return f"{indentation}call {self.procedure_name};"

class PrintStatement(Statement):
    def __init__(self, variable_name: str) -> None:
        self.variable_name = variable_name

    def serialise(self, indent_level: int = 0) -> str:
        indentation = " " * (indent_level * 4)
        return f"{indentation}print {self.variable_name};"

class ReadStatement(Statement):
    def __init__(self, variable_name: str) -> None:
        self.variable_name = variable_name

    def serialise(self, indent_level: int = 0) -> str:
        indentation = " " * (indent_level * 4)
        return f"{indentation}read {self.variable_name};"

class IfStatement(Statement):
    def __init__(self, condition: Expression, if_statements: StatementList, else_statements: StatementList) -> None:
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

    def serialise(self, indent_level: int = 0) -> str:
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
    def __init__(self, condition: Expression, statements: StatementList):
        self.condition = condition
        self.statements = statements

    def serialise(self, indent_level: int = 0) -> str:
        indentation = " " * (indent_level * 4)
        code = (
            f"{indentation}while ({self.condition.serialise()}) {{\n"
            f"{self.statements.serialise(indent_level + 1)}\n"
            f"{indentation}}}"
        )
        return code

import random   
APPEND_CHANCE = 0.7
DECAY = 0.999
def roll():
    global APPEND_CHANCE
    APPEND_CHANCE *= DECAY
    return APPEND_CHANCE

class EntityFactory:
    def generate(self):
        pass

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
                    IfStatementFactory,
                    WhileStatementFactory
                 ],
                weights = (20, 20, 20, 10, 10))[0]
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
        variable_name = f"var_{random.randint(1, 100)}"
        return PrintStatement(variable_name)

class ReadStatementFactory(EntityFactory):
    def generate(self):
        variable_name = f"var_{random.randint(1, 100)}"
        return ReadStatement(variable_name)
    
class IfStatementFactory(EntityFactory):
    def generate(self):
        condition = ExpressionGenerator().generate()
        if_statements = StatementListFactory().generate()
        else_statements = StatementListFactory().generate()
        return IfStatement(condition, if_statements, else_statements)
    
class WhileStatementFactory(EntityFactory):
    def generate(self):
        condition = ExpressionGenerator().generate()
        statements = StatementListFactory().generate()
        return WhileStatement(condition, statements)

class ExpressionGenerator(EntityFactory):
    def generate(self):
        return Expression(Variable('x'), '==', Constant('1'))

if __name__ == "__main__":
    p = ProcedureFactory()
    buffer = ""
    for _ in range(10):
        buffer += p.generate().serialise()
        with open('generate.in', 'w') as f:
            f.write(buffer)
    
    with open('truths.out', 'w') as f:
        f.write(')\n('.join(str(list(pkb.relationships)).split('), (')))