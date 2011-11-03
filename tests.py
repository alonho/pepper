from pepper import Pepper, BIN_SYMBOLS

c = Pepper().convert

def assert_unchanged(s):
    if c(s) != s:
        print "original:"
        print s
        print
        print "new: "
        print c(s)
        assert False

u = assert_unchanged
    
def test_print():
    u("print 1")
    u("print >> f, 'a'")
    u("print 'a',")

def test_math():
    assert c("1 + 3 + 2") == "(1 + 3) + 2"
    assert c("1 + 3 * 2") == "1 + (3 * 2)"
    assert c("(1 + 2) * 3") == "(1 + 2) * 3"
    
    for op in BIN_SYMBOLS.values():
        u("1 {} 2".format(op))

def test_if():
    u("""
if True:
    pass
elif False:
    1
else:
    2""")

def test_for():
    u("""
for i in l:
    pass""")

def test_while():
    u("""
while True:
    pass""")

def test_func():
    u("""
@dec
def f(a, b=3, *c, **d):
    pass""")

def test_attribute():
    u("a.b")
    
def test_class():
    u("""
@dec
class a(p1, p2):
    
    def f():
        pass""")

def test_assign():
    u("a = b = 1")

def test_augassign():
    u("a += 1")
    
def test_delete():
    u("del a, b")

def test_import():
    u("import a")

def test_import_from():
    u("from x import y, z")

def test_alias():
    u("import a as b")

def test_try():
    u("""try:
    a
except Exception, e:
    b
else:
    c""")

    u("""try:
    a
except Exception:
    b""")

    u("""try:
    a
except:
    b""")

    u("""try:
    a
finally:
    b""")
    
    u("""try:
    a
except E:
    b
finally:
    c""")

def test_list_comp():
    u("[a for b in c for d in k if j]")
    
def test_gen_comp():
    u("(a for b in c for d in k if j)")

def test_set_comp():
    u("{a for b in c for d in k if j}")

def test_call():
    u("f(a, b=0, *c, **d)")
    
def test_unpack():
    u("f(*a)")

def test_tuple():
    u("(1, 2, 3)")

def test_list():
    u("[1, 2]")

def test_set():
    u("{1, 2}")

def test_dict():
    u("{a: 1, b: 2}")

def test_bool():
    u("(a and b and c) or d")

def test_unary():
    u("not a")
    u("~a")

def test_getitem():
    u("a[b]")

def test_slice():
    u("a[:]")
    u("a[1:]")
    u("a[:1]")
    u("a[::1]")
    u("a[0:10:2]")

def test_extslice():
    u("l[1, 2:3, 4:5, 6]")
    
def test_compare():
    u("a == b and b == c")

def test_yield():
    u("yield a")
    
def test_lambda():
    u("lambda x, y=1, *a, **k: x * 2")

def test_ellipsis():
    u("Ellipsis")

def test_dictcomp():
    u("{a: b for (a, b) in d}")

def test_repr():
    u("`a`")

def test_with():
    u("""with a as b:
    pass""")

def test_global():
    u("global x, y")

def test_return():
    u("return x")

def test_break():
    u("break")

def test_continue():
    u("continue")

def test_raise():
    u("raise x, y, z")
