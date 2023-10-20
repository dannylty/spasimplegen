import simple

class Extractor:
    pass

class NextExtractor(Extractor):
    def __init__(self, pkb):
        self.pkb = pkb
        self.m_prev = list()

    def visit_procedure(self, p):
        self.visit_stmt_lst(p.statements)
        self.m_prev = list()

    def visit_if_stmt(self, if_stmt):
        self.register_next(if_stmt)
        self.m_prev = list()

        then_extractor = NextExtractor(self.pkb)
        else_extractor = NextExtractor(self.pkb)
        then_extractor.m_prev.append(if_stmt)
        else_extractor.m_prev.append(if_stmt)

        then_extractor.visit_stmt_lst(if_stmt.if_statements)
        else_extractor.visit_stmt_lst(if_stmt.else_statements)

        self.m_prev += then_extractor.m_prev
        self.m_prev += else_extractor.m_prev

    def visit_while_stmt(self, while_stmt):
        self.register_next(while_stmt)

        inner_extractor = NextExtractor(self.pkb)
        inner_extractor.m_prev.append(while_stmt)

        inner_extractor.visit_stmt_lst(while_stmt.statements)
        inner_extractor.register_next(while_stmt)

    def visit_stmt_lst(self, statements):
        for stmt in statements:
            if type(stmt) == simple.WhileStatement:
                self.visit_while_stmt(stmt)
            elif type(stmt) == simple.IfStatement:
                self.visit_if_stmt(stmt)
            else:
                self.visit_normal_stmt(stmt)

    def register_next(self, s):
        for stmt in self.m_prev:
            self.pkb.add_relationship(("next", stmt.line_number, s.line_number))

        self.m_prev.clear()
        self.m_prev.append(s)

    def visit_binary_expr(self, _):
        pass

    def visit_literal_expr(self, _):
        pass

    def visit_unary_expr(self, _):
        pass

    def visit_normal_stmt(self, s):
        self.register_next(s)
