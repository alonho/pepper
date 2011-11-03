import re

def seperate_to_words(s):
    ss = [s]
    result = []
    def found(match):
        result.append(match.groups()[0])
        ss.append(ss.pop().replace(match.groups()[0], ''))
        
    # from FOOBar extract FOO
    re.sub("_?([A-Z]+)[A-Z][a-z]", found, ss[0])
    re.sub("_?([A-Z]+$)", found, ss[0])
    re.sub("_?([A-Z][a-z]+)", found, ss[0])
    re.sub("_?([^A-Z][a-z]+)", found, ss[0])
    return result

def to_camel_case(s):
    """
    foo -> Foo
    foo_bar -> FooBar
    """
    return ''.join(map(str.capitalize, s.split('_')))

def match_to_lower(match):
    return match.group().lower()

def decapitalize(s):
    return re.sub("(^[A-Z])", match_to_lower, s)

def match_to_under_and_lower(match):
    return '_' + match.group().lower()

def to_under_score(s):
    """
    Foo -> foo
    FooBar -> foo_bar
    """
    return re.sub("([A-Z])", match_to_under_and_lower, decapitalize(s))
