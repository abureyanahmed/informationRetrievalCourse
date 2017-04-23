Files attached herewith:

1. build.sbt
3. rest is all classic SCALA/JAVA file structure. 
5. actual codes can be found in /src/main/scala/
6. the input file which contains the documents can be found in:/src/main/resources/inputfile.txt

How to run:
1. unzip and cd to this folder
2. Type “sbt run” and follow the prompts.



To test for Qns7.1: non directional queries
Eg:new /1 schizophrenia

1. type sbt run
2. choose option 1
3. type in your query


To test for Qns7.1: directional queries
Eg:new /1 schizophrenia

1. type sbt run
2. choose option 2
3. type in your query



Some notes/assumptions:
1. In the input file, I am assuming there is a space between the word "doc" and document id" Eg: "Doc 1". Kindly input the files accordingly, or use the sample input file provided in the resources folder (/src/main/resources/inputfile.txt)

2. I am assuming the query input will be in small letters. My parser will through an error if it sees "Drug" instead of "drug". I can fix it to take capital letters too, but then I thought this is not a compilers class and you probably wont matter. Similarly it is assumed that the input document contains all words in small letters.

3. Proximity is defined to start from 1. i.e the proximity between the words drug and schizophrenia in "drug schizophrenia" is 1 and  "drug for schizophrenia" is 2.

4. The input : "drug /78789876757867 hopes" will fail, because that integer is beyond what Int in scala can understand. I tried on the maximum value of Int. So:
drug /2147483647 hopes : will work
drug /2147483648 hopes : will fail

5. Since the sample input file didnt have a full stop at the end of the sentences, I am assuming the input you provide wont have a full stop at the end of sentences. My code wont give correct results if there is a full stop. This is not because I overlooked the fact. But because, I thought it is too unnecessary a detail to implement for this course.

6. Negative values for proximity indicator is considered and error.


Other sample input tested: I have tested my code against these sentences.

Doc 1 a new hope
Doc 2 empire strikes back
Doc 3 return of the jedi
Doc 4 clone wars return of the jedi



Test cases: These are a list of test cases i have tested my code against. You can choose to ignore if irrelevant.

Positive test cases
breakthrough /1 drug
for /2 of
new /1 schizophrenia
new /2 schizophrenia
new /3 schizophrenia

Multiple occurences of same combination
drug /1 for

Test cases given in the question
schizophrenia /2 drug

Reverse test cases.
drug /1 for
for /1 drug
new /2 for
for /2 new
schizophrenia /2 drug
Eg: breakthrough /3 new

Test for non integer values as proximity
*** instead of /2
Space space space instead of /2
/****
/space space space

Parser testing
Capital letters
;lasjdflk /2 asdfasdf
**** /2 ************

Test for negative integer values as proximity
drug /-1 hopes

Test for decimals
drug /0.2 /hopes

Test for very high integer values
Code shouldnt bomb- it should reply that no proximity is found

Test for random parsing strings Eg: 988098345 /2 w34234

Check if two terms exist in the same document
Drug /2 drug
new /3 breakthrough

Tests for directional queries

Positive test cases
breakthrough /1 drug
drug /1 breakthrough  
for /2 of
new /1 schizophrenia
Should give result
schizophrenia /1 new 
Should throw error
new /2 schizophrenia
Not found
new /3 schizophrenia
found

Multiple occurences of same combination
drug /1 for
drug /2 for
for /1 drug
for /2 drug

Test cases given in the question
schizophrenia /2 drug
Not found
schizophrenia /1 drug
Found only in doc 2, 
Found in doc1 but Error for doc 1
Found in doc3 but Error for doc 3
breakthrough /3 new
schizophrenia /4 drug
schizophrenia /2 drug
schizophrenia /1 drug
drug /1 for
for /1 drug
new /2 for
for /2 new
schizophrenia /2 drug
Eg: breakthrough /3 new

