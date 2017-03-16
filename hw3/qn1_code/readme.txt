The versions of various tools used in this code are as follows:

Tool: Java
java version "1.8.0_77"
Java(TM) SE Runtime Environment (build 1.8.0_77-b03)
Java HotSpot(TM) 64-Bit Server VM (build 25.77-b03, mixed mode)

Tool: Lucene
<version>6.4.2</version>

Tool: Maven
Apache Maven 3.3.9 



Steps to Export Path:
1.Add the following to ~/.profile and ~/.bash_profile
2. export JAVA_HOME= `/usr/libexec/java_home -v 1.8`
3. export PATH=/Users/mithun/Desktop/apache-maven-3.3.9/bin:$PATH

Note: this will change depending on the location of java and maven in your machine.


Steps to Compile/Run:
1. change directory to the directory which has pom.xml
Eg: cd /hw3/qn1_code/mithun-hw3/
2. type “mvn compile”
3. type “mvn exec:java”
4. input is taken from the file input.txt kept at hw3/qn1_code/mithun-hw3/input.txt.
Note: this is at the same level at which pom.xml is kept.


Notes:
1.For Qn 1.1: Please use/uncomment the following entry in pom.xml to test 
 	 <!--For Qn 1.1-->
        <argument>information</argument>
        <argument>retrieval</argument>
2. For Qn 1.3: Please use the following entries in pom.xml to test the 3 sections of Qn 1.3
 	<!--For Qn 1.3.a-->
        <argument>information</argument>
        <argument>AND</argument>
        <argument>retrieval</argument>

        <!--For Qn 1.3.b-->
        <argument>information</argument>
        <argument>AND NOT</argument>
        <argument>retrieval</argument>

        <!--For Qn 1.3.c-->
        <argument>information</argument>
        <argument>AND</argument>
        <argument>retrieval</argument>
        <argument>1</argument>

Note: If you test more boolean queries, make sure they are all in the same argument. If there are more than 3 arguments, my code assumes that the 4th argument is the proximity distance.


3. For Qn 1.4

To test ClassicSimilarity instead of the default BM25 please uncomment the following lines of code:

line 37: // config.setSimilarity(new ClassicSimilarity());
line 129:   //searcher.setSimilarity(new ClassicSimilarity());

