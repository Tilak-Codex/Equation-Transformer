import re

# Given equation and variable to solve for
equation = "-apple = -4e - orange+5a-y+3"
getting_input = "e"

print("Equation:", equation)
print("Getting_input:", getting_input)

def spliting_equation(equation):
    equation = equation.replace(" ", "")  
    result = []
    term = ""
    
    for char in equation:
        if char in "+-":  
            if term:  
                result.append(term)
            term = char  
        else:
            term += char  
    if term:
        result.append(term)
        
    return result


def lhsRhs(lhs, rhs, variable):
    left_side = []
    right_side = []

    lhs_terms = spliting_equation(lhs)
    rhs_terms = spliting_equation(rhs)

    print("LHS terms:", lhs_terms)
    print("RHS terms:", rhs_terms)

    for term in lhs_terms:
        term = term.strip()
        if term and is_target_variable(term, variable):
            left_side.append(term) 
        else:
           
            if term.startswith("-"):
                right_side.append(term[1:])  
            else:
                right_side.append(f"-{term}") 

    for term in rhs_terms:
        term = term.strip()
        if term and is_target_variable(term, variable):
            if term.startswith("-"):
                left_side.append(term[1:]) 
            else:
                left_side.append(f"-{term}") 
        else:
            if term.startswith("-") or term.startswith("+"):
                right_side.append(term) 
            else:
                right_side.append(f"+{term}")  

    return left_side, right_side


def is_num_without_signs(coefficient_part):
    if not coefficient_part:
        return False

    if coefficient_part[0] in "+-":
        coefficient_part = coefficient_part[1:]

    for char in coefficient_part:
        if not ('0' <= char <= '9'):
            return False

    return True


def is_target_variable(term, variable):
    if term.endswith(variable):
        coefficient_part = term[:-len(variable)] 
        if coefficient_part == "" or coefficient_part in ["+", "-"] or is_num_without_signs(coefficient_part):
            return True

    return False


if '=' not in equation:
    print("Invalid equation")
else:
    lhs, rhs = equation.split("=")
    if not getting_input.isalpha():
        print("Variable is invalid")
    else:       
        tokens = re.findall(r"-?\d*[a-zA-Z]+|[a-zA-Z]+|\d+|[+\-*/=]", equation)

        elements = []
        for token in tokens:
            contains_letter = False
            for char in token:
                if char.isalpha():
                    contains_letter = True
                    break  
            if contains_letter:
                elements.append(token)

        selected_list = []
        for item in elements:
            variable_part = ""
            for char in item:
                if char.isalpha():  
                    variable_part += char
            selected_list.append(variable_part)


        print("Elements:", elements)
        print("Selected_list:", selected_list)

        found = False
        for element in selected_list:
            if element == getting_input:
                left_side, right_side = lhsRhs(lhs, rhs, getting_input)
                left_side_str = " + ".join(left_side)
                right_side_str = " ".join(right_side)  

                print("Output:", left_side_str, "=", right_side_str)
                found = True
                break  

        if not found:
            print("Variable is not found in the equation")
