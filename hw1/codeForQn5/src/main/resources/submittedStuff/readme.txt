Files attached herewith:

1. the file containing written answers:v1.5_hw1_mithunpaul.pdf
2. build.sbt
3. rest is all classic SCALA/JAVA file structure. 
5. actual codes can be found in /src/main/scala/
6. the input file which contains the documents can be found in:/src/main/resources/inputfile.txt

How to run:
1. unzip and cd to this folder
2. Type “sbt run” and follow the prompts.



To test for Qns5.1 and Qn5.2: i.e simple two word queries separated by an operator.
Eg:schizophrenia AND drug

1. type sbt run
2. choose option 1
3. type in your query

Notes: 

1. parenthesis is not supported. This is a simple LR parser now.
2. supports AND queries
3. supports OR queries.


To test for Qn 5.3:
i.e simple two word queries separated by an operator.
Eg:(drug OR treatment) AND schizophrenia


1. type sbt run
2. choose option 2
3. type in your query




Notes
1. Parenthesis is supported.

2. The operator priority is determined by the parenthesis. Hence a query where the operator priority is not specified explicitly with parenthesis will throw an error.
Eg: drug OR treatment AND schizophrenia


3. A query without parenthesis won’t work.

4. Please refer to the pdf attached herewith for details about test cases covered by this parser.


5. A long set of ************************************************* denotes that the entire application has restarted.

