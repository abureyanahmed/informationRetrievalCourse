use maven

mvn compile
mvn 


todo: 

update mvn version
submit class path addition shell script?
move to another folder and check
or move to chung.cs. and check


For Qn 1.3: Please use the following entries in pom.xml to test the 3 sections of Qn 1.3


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

