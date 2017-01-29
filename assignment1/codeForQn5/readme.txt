How to run:

Type “sbt run” and follow the prompts.



To test for Qns5.1 and qn5.2: i.e simple two word queries separated by an operator.
Eg:schizophrenia AND drug

1. type sbt run
2. choose option 1
3. type in your query

Note: parenthesis is not supported. This is a simple LR parser now.


To test for Qn 5.3:

1. type sbt run
2. choose option 2
3. type in your query


Note: A long set of ************************************************* denotes that the entire application has restarted.


Features:

Currently below are the functionalities supported by this code.

1. supports boolean AND queries
Eg: schizophrenia AND drug

2. supports boolean OR queries.
Eg: breakthrough OR new


Qn) What it does not support?

Ans: currently it doesn’t support multiple concatenated queries.

Eg: (schizophrenia AND drug) OR (breakthrough OR new)

Qn) What are the error/null checks?
Ans: I have tried to cover all possible error checks. 