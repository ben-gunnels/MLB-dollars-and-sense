from collections import defaultdict
"""
Utility functions for web scraper functionality
"will smithp": "players/s/smithwi04.shtml",
"""
# Replace unidentifiable chars with their common replacement
character_replacement = { "\u00e9": "e", 
                    "\u00f1": "n", 
                    "\u00fa": "u",
                    "\u00f3": "o" ,
                    "\u00d3": "O",
                    "\u00e1": "a",
                    "\u00c1": "A",
                    "\u00ed": "i",
                    } 

problem_names = [
    ["jackie", "bradley", "jr."],
    ["vladimir", "guerrero", "jr."],
    ["victor", "mesa", "jr."]
]

def replace_text(text):
    """
        Replaces unidentified characters with common identifiers. Not recommended to use. 
    """
    for old, new in character_replacement.items():
        text = text.replace(old, new)
    return text


def capitalize_correct(text, sep=" "):
    text = text.split(sep)
    text = [x.capitalize() for x in text]
    return text

def format_name(text, sep=" "):
    """
    Convoluted text processing to create keys. Handles edge cases.
    """
    text = text.replace(",", "")       
    text = text.split(sep)
    text = [name.lower() for name in text]

    if (len(text) == 3): # Name contains three parts
        if any(suffix in set(text) for suffix in ["jr.", "ii", "iii", "iv"]):
            if any(set(problem_name) == set(text) for problem_name in problem_names):
                for problem_name in problem_names:
                    if set(text) == set(problem_name):
                        text = " ".join(problem_name)
            else:
                text = f"{text[-1]} {text[-3]} {text[-2]}" # Name contains a jr., etc. first_name last_name jr
        elif any(middle in set(text) for middle in ["de", "la"]):
            text = f"{text[-1]} {text[-3]} {text[-2]}" 
        else:
            text = f"{text[-2]} {text[-1]} {text[-3]}" # Name contains a middle name first_name middle_initial last_name
    elif (len(text) == 4):
        text = f"{text[-1]} {text[-4]} {text[-3]} {text[-2]}"
    else:
        text = f"{text[1]} {text[0]}"
        # text = replace_text(text) # Don't replace characters
    return text