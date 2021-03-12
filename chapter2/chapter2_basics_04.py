def identify_case(s):
    if s == s.lower():
        return "Lowercase"
    elif s == s.upper():
        return "Uppercase"
    elif s == s.capitalize():
        return "Capitalized"
    else:
        return "Mixed"


assert identify_case("hello world") == "Lowercase"
assert identify_case("HELLO WORLD") == "Uppercase"
assert identify_case("Hello world") == "Capitalized"
assert identify_case("HELLO world") == "Mixed"
