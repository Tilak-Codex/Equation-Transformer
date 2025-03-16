import re

equation = 'apple = e+4orange+5a+4'
getting_input = "orange"

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
                right_side.append(f"+{term[1:]}")
            elif term.startswith("+"):
                right_side.append(f"-{term[1:]}")
            else:
                right_side.append(f"-{term}")

    for term in rhs_terms:
        term = term.strip()
        if term and is_target_variable(term, variable):
            if term.startswith("-"):
                left_side.append(f"+{term[1:]}")
            elif term.startswith("+"):
                left_side.append(f"-{term[1:]}")
            else:
                left_side.append(f"-{term}")
        else:
            if term.startswith("-") or term.startswith("+"):
                right_side.append(term)
            else:
                right_side.append(f"+{term}")
                
    print("1LHS terms:", left_side) 
    print("1RHS terms:", right_side)
    
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

def left_side_constant(expression):
    expression = expression.replace(" ", "")
    total = 0
    num = ""
    
    for i in expression:
        if i.isdigit() or i in '-+':
            num += i
    
    try:
        total = eval(num)  
    except:
        total = 0  

    return total  


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
                left_side_str = "".join(left_side)
                right_side_str = "".join(right_side)  
                
                print("Left side str:", left_side_str)
                print("Right side str:", right_side_str)

                coefficient = left_side_constant(left_side_str)
                print("Coefficient of variable:", coefficient)
                dividing = '/'
                
                try:
                    
                    if coefficient and coefficient != 0:
                        print("1")
                        print("Output:", getting_input, "=", (right_side_str),dividing, int(coefficient) )
                    else:
                        print("2")
                        if left_side_str.startswith("-"):
                            right_side_str = right_side_str.replace(" ","")
                            right_side_str = right_side_str.replace("-","+")
                            right_side_str = right_side_str.replace("+","-")
                            left_side_str = left_side_str[1:]
                        if left_side_str.startswith("+"):
                            left_side_str = left_side_str[1:]
                        print("Output:", left_side_str, "=", right_side_str)

                except Exception as e:
                    print("Error evaluating right side:", e)

                found = True
                break  

        if not found:
            print("Variable is not found in the equation")
