from converters import to_camel_case, to_under_score, seperate_to_words

def test_seperate():
    assert seperate_to_words("FooBar") == ["Foo", "Bar"]
    assert seperate_to_words("_FooBar") == ["Foo", "Bar"]
    assert seperate_to_words("foo_bar") == ["foo", "bar"]
    assert seperate_to_words("_foo_bar") == ["foo", "bar"]
    assert seperate_to_words("FOOBar") == ["FOO", "Bar"]
    assert seperate_to_words("_FOOBar") == ["FOO", "Bar"]
    assert seperate_to_words("_YaBADaBaDoo") == ["Ya", "BA", "DA", "Ba", "Doo"]

def _test_to_camel_case():
    assert to_camel_case("foo") == "Foo"
    assert to_camel_case("foo_bar") == "FooBar"
    assert to_camel_case("FooBar") == "FooBar"

def _test_to_under_score():
    assert to_under_score("Foo") == "foo"
    assert to_under_score("FooBar") == "foo_bar"
    assert to_under_score("_foo_bar") == "_foo_bar"
    
