How to run:

//copy from hw1 submission
Self explanatory/follow the instructions on screen.


Some notes/assumptions:
1. In the input file, I am assuming there is a space between the word "doc" and document id" Eg: "Doc 1". Kindly input the files accordingly, or use the sample input file provided in the resources folder (/src/main/resources)

2. I am assuming the input will be in small letters. My parser will through an error if it sees "Drug" instead of "drug". I can fix it to take capital letters too, but then I thought this is not a compilers class and you probably wont care. Similarly it is assumed that the input document contains all words in small letters.

3. Proximity is defined to start from 1. i.e the proximity between the words drug and schizophrenia in "drug schizophrenia" is 1 and  "drug for schizophrenia" is 2.

4. The input : drug /78789876757867 hopes will fail, because that integer is beyond what Int in scala can understand. I tried on the maximum value of Int. So:
drug /2147483647 hopes : will work
drug /2147483648 hopes : will fail

5. Since the sample input file didnt have a full stop at the end of the sentences, I am assuming the input you provide wont have a full stop at the end of sentences. My code wont give correct results if there is a full stop. This is not because I overlooked the fact. But because, I thought it is too unnecessary a detail to implement for this course.



Test cases:

Below are a list of test cases I have tested this code on. Its highly possible that I might have missed out some edge test case. But the code works fine for all positive test cases, I think.


Other sample input tested:

Doc 1 a new hope
Doc 2 empire strikes back
Doc 3 return of the jedi
Doc 4 clone wars return of the jedi








