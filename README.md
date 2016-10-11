# Python-Based-Compiler

Basic compiler, written in python.
Submitted as an assignment for Formal Languages and Compilers.

The compiler will accept programs with the following syntax:

Program = Statements
Statements = Statement (; Statement)*
Statement = If | While | Assignment

If = if Comparison then Statements end
While = while Comparison do Statements end
Assignment = identifier := Expression

Comparison = Expression Relation Expression
Relation = = | != | < | <= | > | >=

Expression = Term ((+ | -) Term)*
Term = Factor ((* | /) Factor)*
Factor = (Expression) | number | identifier
