(*
* Matthew "Matt" Gee
* Pomona College
* CS52 FA16
* Sept 8, 2016
*)


(*
* Test a function with 1-3 arguments
* @problem : string with problem number, i.e. "1. Cube"
* @num : string with test number i.e. "1"
* @total: string with the total number of tests for this problem (or in
* general), i.e. "3"
* with num=1 and total=3, prints as "1. Cube 1/3"
* @str: string to print out if test fails, i.e. "Checks base cases for lists"
* @function: function name to test
* @argN: argument for function (must be in order)
*
*
* Sample block:
*
* 
* val _ = test1 "1. CUBE " "1" "3" "Check basic functionality" cube 5 125;
* val _ = test1 "1. CUBE " "2" "3" "Check basic functionality" cube 3 27;
* val _ = test1 "1. CUBE " "3" "3" "Check basic functionality" cube 0 0;
*
* If all are correct, runs as
* 
* 1. CUBE 1/3 : PASS
* 1. CUBE 2/3 : PASS
* 1. CUBE 3/3 : PASS
*
* Use val _ to silence printing of every name
*
*
*) 
fun test1 problem num total str function arg1 retval = 
  if (function arg1 = retval)
    then print(problem ^ num ^ "/" ^ total ^ " : PASS\n")
  else
    print(problem ^ num ^ "/" ^ total ^ " : FAIL\n" ^ str ^ "\n");

fun test1_rf problem num total str function arg1 retval = 
  if (Real.==((function arg1), retval) = true)
    then print(problem ^ num ^ "/" ^ total ^ " : PASS\n")
  else
    print(problem ^ num ^ "/" ^ total ^ " : FAIL\n" ^ str ^ "\n");
    
fun test2 problem num total str function arg1 arg2 retval = 
  if (function arg1 arg2 = retval)
    then print(problem ^ num ^ "/" ^ total ^ " : PASS\n")
  else
    print(problem ^ num ^ "/" ^ total ^ " : FAIL\n" ^ str ^ "\n");

fun test3 problem num total str function arg1 arg2 arg3 retval = 
  if (function arg1 arg2 arg3 = retval)
    then print(problem ^ num ^ "/" ^ total ^ " : PASS\n")
  else
    print(problem ^ num ^ "/" ^ total ^ " : FAIL\n" ^ str ^ "\n");
