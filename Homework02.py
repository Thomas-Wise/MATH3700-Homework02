# Homework02.py
# Thomas Wise
# MATH 3700, Homework 02
# 09 Mar 2020



# Let x_poly be the set of powers of x and their coefficients.
# So [[2,3], [4,5]] = (2x^3) + (4x^5)



# A function for multiplying polynomials together
def multPolys(p1, p2):
    # First find the maximum exponent value and build an empty polynomial
    # of that size
    maxTerm = 0;
    for term1 in p1:
        for term2 in p2:
            if term1[1] + term2[1] > maxTerm:
                maxTerm = term1[1] + term2[1]
    p3 = [];
    for i in range(0, maxTerm + 1):
        p3.append([0,i])
        
    # Multiply all the terms in term1 by all the terms in term2 and add them
    # to p3
    for term1 in p1:
        for term2 in p2:
            p3[term1[1] + term2[1]][0] += term1[0] * term2[0];
    
    # Remove any terms with a coeff of 0
    term = 0;
    while(term < len(p3)):
        if p3[term][0] == 0:
            p3.pop(term);
        else:
            term += 1;
    return p3;

##############################################################################

# This finds all the possible f_1s and f_2s, including duplicates and ones
# that can't be used. It is a recursive function.
def findFs(polys, exponents, f1s, f2s, polyNum, expVars):
    # polyNum is the current polynomial whose exponent we're iterating through.
    # exponents[polyNum] is the max exponent.
    for exp in range(0, exponents[polyNum] + 1):
        # If we're iterating through the last polynomial, multiply f1 and f2
        # by each polynomial to the power of their current exponent and add
        # it to the list.
        if polyNum == len(polys) - 1:
            f1 = [[1, 0]];
            f2 = [[1, 0]];
            f1[0][0] = 1;
            f2[0][0] = 1;
            for poly in range(0, len(polys)):
                for x0 in range(0, expVars[poly]):
                    f1 = multPolys(f1, polys[poly]);
                for x0 in range(0, exponents[poly]-expVars[poly]):
                    f2 = multPolys(f2, polys[poly]);
            f1s.append(f1);
            f2s.append(f2);
        
        # If this is not the last polynomial, iterate through all the later
        # polynomials
        else:
            findFs(polys, exponents, f1s, f2s, polyNum + 1, expVars);
        # Keep track of the current exponents.
        expVars[polyNum] += 1;
    expVars[polyNum] = 0;
    
##############################################################################

# Takes sets of f1 and f2 and return only the f1s and f2s that have no negative
# coeffs and where all the coeffs add up to the number of sides.
def findGoodFs(f1s, f2s, goodF1s, goodF2s, sides):
    total1 = 0;
    total2 = 0;
    for function in range(0, len(f1s)):
        total1 = 0;
        total2 = 0;
        neg1 = False;
        neg2 = False;
        for term in f1s[function]:
            if term[0] < 0:
                neg1 = True;
                break;
            total1 += term[0];
        for term in f2s[function]:
            if term[0] < 0:
                neg2 = True;
                break;
            total2 += term[0];
        
        if total1 == sides and total2 == sides and (not neg1) and (not neg2):
            goodF1s.append(f1s[function]);
            goodF2s.append(f2s[function]);
            
##############################################################################

# Takes a poly data structure and prints it in a more readable form.
def strPoly(poly):
    string = "";
    for term in range(0, len(poly) - 1):
        string += str(poly[term][0]) + "x^" + str(poly[term][1]) + " + ";
    string += str(poly[-1][0]) + "x^" + str(poly[-1][1]);
    return string;

##############################################################################

# Removes duplicate sets of f1 and f2. i.e. f1 and f2 are switched or you just
# added something to all the sides of f1 and subtracted it from f2
def remDups(f1s, f2s):
    p1 = 0;
    while p1 < len(f1s):
        p2 = p1 + 1;
        # For every pair of f1 and f2, compare it to every later pair of f1 and
        # f2. Then if they're the same, remove the second pair.
        while(p2 < len(f2s)):
            same = True;
            # Check if f1 and f2 in the first pair both have a function in the 
            # second pair that is the same size
            sameSize = len(f1s[p1]) == len(f1s[p2]) and (
                       len(f2s[p1]) == len(f2s[p2]));
            sameSize = sameSize or len(f1s[p1]) == len(f2s[p2]) and (
                                   len(f2s[p1]) == len(f1s[p2]));
            if not sameSize:
                same = False;
            # If they are the same size, make sure that f1 and f2 from the
            # first pair each have a function in the second pair such that
            # the coefficients are the same and the exponents are the same.
            # (The exponents are still considered the same if they're just
            # added by a certain amount in f1 and subtracted by that amount
            # in f2)
            
            else:
                same1 = False;
                same2 = False;
                if(len(f1s[p1]) == len(f1s[p2])):
                    sameCoeffs = True;
                    for term in range(0, len(f1s[p1])):
                        if(f1s[p1][term][0] != f1s[p2][term][0]):
                            sameCoeffs = False;
                            break;
                    if sameCoeffs and (not same1):
                        same1 = True;
                        diff = f1s[p1][0][1] - f1s[p2][0][1];
                        for term in range(0, len(f1s[p1])):
                            if not (
                            (f1s[p1][term][1] - f1s[p2][term][1]) == diff):
                                same1 = False;
                        
                        
                if(len(f2s[p1]) == len(f2s[p2])):
                    sameCoeffs = True;
                    for term in range(0, len(f2s[p1])):
                        if(f2s[p1][term][0] != f2s[p2][term][0]):
                            sameCoeffs = False;
                            break;
                    if sameCoeffs and (not same2):
                        same2 = True;
                        diff = f2s[p1][0][1] - f2s[p2][0][1];
                        for term in range(0, len(f2s[p1])):
                            if not (
                            (f2s[p1][term][1] - f2s[p2][term][1]) == diff):
                                same2 = False;
                        
                        
                if(len(f1s[p1]) == len(f2s[p2])):
                    sameCoeffs = True;
                    for term in range(0, len(f1s[p1])):
                        if(f1s[p1][term][0] != f2s[p2][term][0]):
                            sameCoeffs = False;
                            break;
                    if sameCoeffs and (not same1):
                        same1 = True;
                        diff = f1s[p1][0][1] - f2s[p2][0][1];
                        for term in range(0, len(f1s[p1])):
                            if not (
                            (f1s[p1][term][1] - f2s[p2][term][1]) == diff):
                                same1 = False;
                    
                if(len(f2s[p1]) == len(f1s[p2])):
                    sameCoeffs = True;
                    for term in range(0, len(f2s[p1])):
                        if(f2s[p1][term][0] != f1s[p2][term][0]):
                            sameCoeffs = False;
                            break;
                    if sameCoeffs and (not same2):
                        same2 = True;
                        diff = f2s[p1][0][1] - f1s[p2][0][1];
                        for term in range(0, len(f2s[p1])):
                            if not (
                            (f2s[p1][term][1] - f1s[p2][term][1]) == diff):
                                same2 = False;
                        
                if (not same1) or (not same2):
                    same = False;
            # If the two pairs are the same, remove the second pair.
            if same:
                f1s.pop(p2);
                f2s.pop(p2);
            else:
                p2 += 1;
        p1 += 1;
##############################################################################

# The main function. Takes as input the polynomials, their exponents, and the
# number of sides and prints all unique pairs of f1 and f2 such that you can
# make the desired dice out of them.
def findDice(polys, exponents, sides):
    f1s = [];
    f2s = [];
    expVars = [0]*len(polys);
    findFs(polys, exponents, f1s, f2s, 0, expVars);
    goodF1s = [];
    goodF2s = [];
    findGoodFs(f1s, f2s, goodF1s, goodF2s, sides);
    remDups(goodF1s, goodF2s);
    for i in range(0, len(goodF1s)):
        print("f_1: " + strPoly(goodF1s[i]));
        print("f_2: " + strPoly(goodF2s[i]));
        print();
##############################################################################
    

# I've been changing this part for each size of die. This is for size 8.
        
# Let x_poly be the set of powers of x and their coefficients.
# So [[2,3], [4,5]] = (2x^3) + (4x^5)
a_poly = [[1,1]];
b_poly = [[1,1],[1,0]];
c_poly = [[1,2],[1,0]];
d_poly = [[1,4],[1,0]];
polys = [a_poly, b_poly, c_poly, d_poly];
findDice(polys, [2,2,2,2], 8);