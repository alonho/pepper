from ast import *
from contextlib import contextmanager

@contextmanager
def null_context():
    yield

def skip_first(func):
    notfirst = []
    def new_func(*a, **k):
        if notfirst:
            return func(*a, **k)
        else:
            notfirst.append(True)
    return new_func

BIN_SYMBOLS = {Add: '+',
               Sub: '-',
               Mult: '*',
               Div: '/',
               FloorDiv: '//',
               Mod: '%',
               LShift: '<<',
               RShift: '>>',
               BitOr: '|',
               BitAnd: '&',
               BitXor: '^'}

BOOL_SYMBOLS = {And: 'and',
                Or: 'or'}

CMP_SYMBOLS = {Eq: '==',
               Gt: '>',
               GtE: '>=',
               In: 'in',
               Is: 'is',
               IsNot: 'is not',
               Lt: '<',
               LtE: '<=',
               NotEq: '!=',
               NotIn: 'not in'}

UNARY_SYMBOLS = {Invert: '~',
                 Not: 'not',
                 UAdd: '+',
                 USub: '-'}

def GET_BIN_SYMBOL(node):
    return BIN_SYMBOLS[type(node)]

def GET_BOOL_SYMBOL(node):
    return BOOL_SYMBOLS[type(node)]

def GET_UNARY_SYMBOL(node):
    return UNARY_SYMBOLS[type(node)]

def GET_CMP_SYMBOL(node):
    return CMP_SYMBOLS[type(node)]

class Pepper(object):

    TAB = ' ' * 4
    
    def __init__(self, verbose=False):
        self._verbose = verbose
        self._flush()

    def _debug(self, node):
        if self._verbose:
            print node, vars(node)    

    def _flush(self):
        self._depth = 0
        self._stack = []
        self._result = []
            
    def tostring(self):
        return "".join(self._result)
        
    def _w(self, s):
        self._result.append(s)

    def convert(self, s):
        self.handle(parse(s))
        result = self.tostring()
        self._flush()
        return result
        
    def nl(self):
        self._w('\n' + self.TAB * self._depth)
        
    @contextmanager
    def indent(self):
        self._depth += 1
        try:
            self.nl()
            yield
        finally:
            self._depth -= 1

    def _get_parent(self):
        try:
            return type(self._stack[-2])
        except IndexError:
            return None
            
    def _parent_same_as_child(self):
        if len(self._stack) < 2:
            return False
        parent, current = self._stack[-2:]
        return type(parent) == type(current)

    def _parens_if_needed(self):
        if self._parent_same_as_child():
            return self._parens()
        return null_context()
        
    @contextmanager
    def _parens(self):
        self._w("(")
        yield
        self._w(")")
            
    @contextmanager
    def _stacked(self, node):
        self._stack.append(node)
        try:
            yield
        finally:
            self._stack.pop()            
            
    def handle(self, node):
        self._debug(node)
        with self._stacked(node):
            return getattr(self, "handle_" + node.__class__.__name__)(node)

    def handle_list(self, nodes):
        self.handle(nodes[0])
        for node in nodes[1:]:
            self.nl()
            self.handle(node)

    def handle_list_sep(self, nodes, sep):
        write_sep = skip_first(lambda: self._w(sep))
        for node in nodes:
            write_sep()
            self.handle(node)

    def handle_list_comma_sep(self, nodes):
        self.handle_list_sep(nodes, ", ")
            
    def indent_handle_list(self, nodes):
        with self.indent():
            self.handle_list(nodes)
            
    def handle_decorators(self, node):
        for dec in node.decorator_list:
            self._w("@")
            self.handle(dec)
            self.nl()

    def handle_Name(self, node):
        self._w(node.id)

    def handle_Str(self, node):
        if "\n" in node.s and node.s != "\n":
            self._w('"""{}"""'.format(node.s))
        else:
            self._w(repr(node.s))
    
    def handle_Num(self, node):
        self._w(repr(node.n))
    
    def handle_Print(self, node):
        self._w("print ")
        if node.dest is not None:
            self._w(">> ")
            self.handle(node.dest)
            self._w(", ")
        map(self.handle, node.values)
        if not node.nl:
            self._w(',')

    def handle_Module(self, module):
        self.handle_list(module.body)
        
    def handle_Expr(self, node):
        self.handle(node.value)

    def handle_Attribute(self, node):
        self.handle(node.value)
        self._w(".{}".format(node.attr))
        
    def handle_BinOp(self, node):
        with self._parens_if_needed():
            self.handle(node.left)
            self._w(" {} ".format(GET_BIN_SYMBOL(node.op)))
            self.handle(node.right)

    def handle_AugAssign(self, node):
        self.handle(node.target)
        self._w(" {}= ".format(GET_BIN_SYMBOL(node.op)))
        self.handle(node.value)

    def handle_Compare(self, node):
        with self._parens_if_needed():
            self.handle(node.left)
            for op, operand in zip(node.ops, node.comparators):
                self._w(" {} ".format(GET_CMP_SYMBOL(op)))
                self.handle(operand)
        
    def handle_If(self, node):
        self.nl()
        self._w("if ")
        while True:
            self.handle(node.test)
            self._w(":")
            self.indent_handle_list(node.body)
            
            orelse = node.orelse
            len_orelse = len(orelse)
            if len_orelse == 0:
                break
            elif len_orelse == 1 and isinstance(orelse[0], If):
                self.nl()
                self._w("elif ")
                node = orelse[0]
                continue
            else:
                self.nl()
                self._w("else:")
                self.indent_handle_list(orelse)
                break

    def handle_Pass(self, node):
        self._w("pass")

    def handle_Assign(self, node):
        self.handle_list_sep(node.targets, " = ")
        self._w(" = ")
        self.handle(node.value)
        
    def handle_For(self, node):
        self.nl()
        self._w("for ")
        self.handle(node.target)
        self._w(" in ")
        self.handle(node.iter)
        self._w(":")
        self.indent_handle_list(node.body)

    def handle_While(self, node):
        self.nl()
        self._w("while ")
        self.handle(node.test)
        self._w(":")
        self.indent_handle_list(node.body)
        if node.orelse != []:
            self._w("else:")
            self.indent_handle_list(node.orelse)

    def handle_arguments(self, node):
        comma = skip_first(lambda: self._w(", "))
        nondefaults = [None] * (len(node.args) - len(node.defaults))
        for arg, default in zip(node.args,
                                nondefaults + node.defaults):
            comma()
            self.handle(arg)
            if default is not None:
                self._w("=")
                self.handle(default)
        for value, prefix in ((node.vararg, "*"),
                              (node.kwarg, "**")):
            if value is not None:
                comma()
                self._w("{}{}".format(prefix, value))
            
    def handle_FunctionDef(self, node):
        self.nl()
        self.handle_decorators(node)
        self._w("def {}(".format(node.name))
        self.handle(node.args)
        self._w("):")
        self.indent_handle_list(node.body)

    def handle_NoneType(self, node):
        self._w("None")
        
    def handle_ClassDef(self, node):
        self.nl()
        self.handle_decorators(node)
        self._w("class {}(".format(node.name))
        self.handle_list_comma_sep(node.bases)
        self._w("):")
        self.indent_handle_list(node.body)

    def handle_Call(self, node):
        self.handle(node.func)
        self._w("(")
        comma = skip_first(lambda: self._w(", "))
        for arg in node.args:
            comma()
            self.handle(arg)
        for keyword in node.keywords:
            comma()
            self._w("{}=".format(keyword.arg))
            self.handle(keyword.value)
        if node.starargs is not None:
            comma()
            self._w("*")
            self.handle(node.starargs)
        if node.kwargs is not None:
            comma()
            self._w("**")
            self.handle(node.kwargs)
        self._w(")")
        
    def handle_Delete(self, node):
        self._w("del ")
        self.handle_list_comma_sep(node.targets)

    def handle_alias(self, node):
        self._w(node.name)
        if node.asname is not None:
            self._w(" as ")
            self._w(node.asname)
        
    def handle_Import(self, node):
        self._w("import ")
        self.handle_list_comma_sep(node.names)

    def handle_ImportFrom(self, node):
        self._w("from {} import ".format(node.module))
        self.handle_list_comma_sep(node.names)

    def make_comprehension(start, end):
        def handler(self, node):
            self._w(start)
            self.handle(node.elt)
            map(self.handle, node.generators)
            self._w(end)
        return handler
            
    handle_ListComp = make_comprehension("[", "]")
    handle_GeneratorExp = make_comprehension("(", ")")
    handle_SetComp = make_comprehension("{", "}")
    
    del make_comprehension
        
    def handle_comprehension(self, node):
        self._w(" for ")
        self.handle(node.target)
        self._w(" in ")
        self.handle(node.iter)
        for if_ in node.ifs:
            self._w(" if ")
            self.handle(if_)

    def handle_DictComp(self, node):
        self._w("{")
        self.handle(node.key)
        self._w(": ")
        self.handle(node.value)
        map(self.handle, node.generators)
        self._w("}")
        
    def handle_TryFinally(self, node):
        next = node.body[0]
        length = len(node.body)
        has_except = length == 1 and type(next) is TryExcept

        if has_except:
            self.handle(next)
            self.nl()
        else:
            self._w("try:")
            self.indent_handle_list(node.body)
            self.nl()
        self._w("finally:")
        self.indent_handle_list(node.finalbody)
            
    def handle_TryExcept(self, node):
        self._w("try:")
        self.indent_handle_list(node.body)
        self.nl()
        for handler in node.handlers:
            self._w("except")
            if handler.type is not None:
                self._w(" ")
                self.handle(handler.type)
                if handler.name is not None:
                    self._w(", ")
                    self.handle(handler.name)
            self._w(":")
            self.indent_handle_list(handler.body)
        if len(node.orelse) > 0:
            self.nl()
            self._w("else:")
            self.indent_handle_list(node.orelse)

    def handle_Tuple(self, node):
        self._w("(")
        self.handle_list_comma_sep(node.elts)
        if len(node.elts) == 1:
            self._w(",")
        self._w(")")

    def make_sequence(start, end):
        def handler(self, node):
            self._w(start)
            self.handle_list_comma_sep(node.elts)
            self._w(end)
        return handler

    handle_List = make_sequence("[", "]")
    handle_Set = make_sequence("{", "}")
    del make_sequence

    def handle_Dict(self, node):
        self._w("{")
        comma = skip_first(lambda: self._w(", "))
        for key, value in zip(node.keys, node.values):
            comma()
            self.handle(key)
            self._w(": ")
            self.handle(value)
        self._w("}")
        
    def handle_BoolOp(self, node):
        with self._parens_if_needed():
            self.handle_list_sep(node.values, " {} ".format(GET_BOOL_SYMBOL(node.op)))

    def handle_UnaryOp(self, node):
        with self._parens_if_needed():
            self._w(GET_UNARY_SYMBOL(node.op))
            if type(node.op) is Not:
                self._w(" ")
            self.handle(node.operand)
            
    def handle_Subscript(self, node):
        self.handle(node.value)
        self._w("[")
        self.handle(node.slice)
        self._w("]")

    def handle_Index(self, node):
        self.handle(node.value)

    def handle_Slice(self, node):
        if node.lower:
            self.handle(node.lower)
        self._w(":")
        if node.upper:
            self.handle(node.upper)
        if node.step:
            self._w(":")
            self.handle(node.step)

    def handle_ExtSlice(self, node):
        self.handle_list_comma_sep(node.dims)

    def handle_Yield(self, node):
        self._w("yield ")
        if node.value is not None:
            self.handle(node.value)

    def handle_Assert(self, node):
        self._w("assert ")
        self.handle(node.test)
        if node.msg is not None:
            self._w(", ")
            self.handle(node.msg)
        
    def handle_Lambda(self, node):
        self._w("lambda ")
        self.handle(node.args)
        self._w(": ")
        self.handle(node.body)

    def handle_Ellipsis(self, node):
        self._w("Ellipsis")

    def handle_Global(self, node):
        self._w("global {}".format(', '.join(node.names)))

    def handle_Nonlocal(self, node):
        self._w("nonlocal {}".format(', '.join(node.names)))
        
    def handle_Repr(self, node):
        self._w("`")
        self.handle(node.value)
        self._w("`")

    def handle_With(self, node):
        self._w("with ")
        self.handle(node.context_expr)
        if node.optional_vars is not None:
            self._w(" as ")
            self.handle(node.optional_vars)
        self._w(':')
        self.indent_handle_list(node.body)
        
    def handle_Return(self, node):
        self._w("return ")
        self.handle(node.value)

    def handle_Break(self, node):
        self._w("break")

    def handle_Continue(self, node):
        self._w("continue")

    def handle_Raise(self, node):
        self._w("raise ")
        self.handle_list_comma_sep((node.type, node.inst, node.tback))
        

if __name__ == '__main__':
    import sys
    print Pepper().convert(sys.stdin.read())
