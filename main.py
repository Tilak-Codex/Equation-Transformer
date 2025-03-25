import re
#Edit made by tilak
equation = 'apple-4x^4+2x^4 = +2x^2+5y-y+4'
getting_input = "x"

print("Equation:", equation)
print("Getting_input:", getting_input)

def spliting_equation(equation):
    equation = equation.replace(" ", "")
    print("Splitting_Equation: ",equation)
 
    result = []
    term = ""
    print("Equation",equation)
    
    for char in equation:
        if char in "+-":  
            if term:  
                result.append(term)
            term = char  
        else:
            term += char  
    if term:
        result.append(term)
        
    print("Result: ",result)
    return result
    
def powering_term(element): 
    tokens = []
    temp = ""
    print("Powering_term: ",element)

    for char in element:
        if char.isalpha() or char == "^" or char == "_":  
            if temp and temp[-1].isdigit():  
                tokens.append(temp)
                temp = ""
            temp += char  
        elif char.isdigit():
            if temp and temp[-1].isalpha():
                temp += char 
                tokens.append(temp)
                temp = ""
            else:
                temp += char
        else:
            if temp:
                tokens.append(temp)
                temp = ""
    
    if temp:
        tokens.append(temp)
        
    print("Tokens:", tokens)

    if tokens[0] in ['+','-']:
        sign = tokens[0]
        tokens = tokens[1:]
        if tokens:
            tokens[0] = sign + tokens[0]
    
    if tokens[0] in ['+', '-']:
        tokens = tokens[1:]
    
    print("Processed Tokens:", tokens)

    numbers = []
    variables = []
    
    for token in tokens:
        if token.isdigit():
            numbers.append(int(token))  
        else:
            variables.append(token) 
    
    if variables and numbers:
        formatted_expression = f"{numbers[0]}{''.join(variables)}"
    else:
        formatted_expression = "".join(variables) if variables else str(numbers[0])

    print("Final Expression:", formatted_expression)
    return formatted_expression

    
def lhsRhs(lhs, rhs, variable):
    left_side = []
    right_side = []

    lhs_terms = spliting_equation(lhs)
    rhs_terms = spliting_equation(rhs)

    print("LHS terms:", lhs_terms)
    print("RHS terms:", rhs_terms)

    for term in lhs_terms:
        term = term.strip()
        term = powering_term(term)
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
        term = powering_term(term)
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
    coefficient = expression
    print("Coefficient",coefficient)
    coefficient = expression
    for char in expression:
        if char.isdigit() or char in "+-":
            num += char
        else:
            break  
    
    if num:
        coefficient = int(num)
    else:
        coefficient = 1

    return coefficient

if '=' not in equation:
    print("Invalid equation")
    
else:
    lhs, rhs = equation.split("=")

    lhs_terms = re.findall(r"[+-]?\w+\^?\d*|\w+", lhs)
    rhs_terms = re.findall(r"[+-]?\w+\^?\d*|\w+", rhs)
    tokens = lhs_terms + rhs_terms
    print("Extracted Terms:", tokens)
    
    elements = []
    
    for token in tokens:
        contains_letter = False
        operator = {'^','_'}
        for char in token:
            if char.isalnum() or char in operator:
                contains_letter = True
                break  
        if contains_letter:
            elements.append(token)
            
    print("Elements:", elements)

    found = False
    for element in elements:
        if getting_input in element and is_target_variable(element, getting_input):

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
                    print("Output:", getting_input, "=", right_side_str, dividing, int(coefficient))

                else:
                    print("2")
                    if left_side_str.startswith("-"):
                        right_side_str = right_side_str.replace(" ", "")
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
