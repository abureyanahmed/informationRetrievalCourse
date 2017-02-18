package booleansearch

import java.io.{File, FileNotFoundException, InputStream}
import java.util
import initializer._
import scala.collection.mutable
import scala.collection.mutable._
import scala.io.Source
import scala.util.Try
import scala.annotation.switch
import scala.util.control.NonFatal
/**
  * Created by mithunpaul on 1/25/17.
  */

case class documentIDPositions (var docId:Int, var positions: ListBuffer[Int]);

object  Utilities {

  val resourcesDirectory = "./src/main/resources/"
  val inputFileForInvIndex = "inputfile.txt";

  var dictionaryForInvertedIndex: Map[String, ListBuffer[documentIDPositions]] = Map();
  var term1 = "";
  var operator = "";
  var term2 = "";

  def readFromFile() = {
    try {
      var noofFiles = 0

      val inputDirectoryToList = new File(resourcesDirectory)
      if (inputDirectoryToList != None) {
        noofFiles = inputDirectoryToList.listFiles().length
      }
      else {
        println("input directory is empty")
      }


      if (noofFiles == 0) {
        //todo: throw an error here
        println("no files in the input directory")

      }
      else {

        println(" no of files found in input directory is:" + noofFiles + ":Going to parallelize")
        //commenting out the parallelized part since it was giving errors in a non multi core machine
        //        val listOfFiles = new File(fullScrapedDirectoryPath).listFiles().par
        //        listOfFiles.tasksupport = new ForkJoinTaskSupport(new scala.concurrent.forkjoin.ForkJoinPool(nthreads))

        val listOfFiles = new File(resourcesDirectory).listFiles()
        //for (line <- Source.fromResource(inputFileForInvIndex).getLines()) {


        val pathToInputFile = resourcesDirectory + inputFileForInvIndex;
        println("value of the path to the file is" + pathToInputFile)

        for (line <- io.Source.fromFile(pathToInputFile).getLines()) {


          println("getting here at 1");
          val content = line.split("\\s+");
           println("getting here at 2");
          var termCounter = 0;
          println("getting here at 3");


          if (content.length > 1) {
            val content = line.split("\\s+");

            //this counter is for actualtoken in sentences only- i.e we are ignoring the words doc and 1
            var positionOfTheTerm = 1;

            var docid = content(1).toInt;

            var noOfTokensDenotingDocId=1;

            println("getting here at 4");
            //there is confusion if the first word is going to be doc1 or doc space 1- writing code for both separated by a boolean flag
            if(initializer.useDoc1)
            {
              noOfTokensDenotingDocId=noOfTokensDenotingDocId+1
              println(content.mkString(" "))
              //in hw2 input, there is no space between doc and 1.
              //split it based on number

              //create a regex for the number 1
              val stringToSplit="doc1dock"
              val NumberOne="1".r();
              println(content(0))
              //println(content(1))
              //var firstword = content(0).split("\\d")
              //var firstword = content(0).split(NumberOne).map(_.trim)
              var firstword =stringToSplit.split("1")

              println("length of firstword is"+firstword.length)
              println(firstword(1))
              System.exit(1)


               docid = firstword(1).toInt;
              println(docid)
              println("getting here at 5");

              println("getting here at 6");

            }



            //for each term in a document
            for (individualToken <- content) {


              //ignore the first two individualToken since it contains only "doc 1"
              if (termCounter <= noOfTokensDenotingDocId) {
                termCounter = termCounter + 1;
                //positionOfTheTerm = positionOfTheTerm +1;


              }

              else {
                //for each of the term you are seeing, get its position and add it to the postings list data structure
                //i am calling this the inner data structure.
                val positions = new ListBuffer[(Int)]
                positions.append(positionOfTheTerm);
                positionOfTheTerm = positionOfTheTerm + 1;

                //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back
                if (dictionaryForInvertedIndex.contains(individualToken)) {

                  var existingPostings = dictionaryForInvertedIndex(individualToken);
                  val objdocumentIDPositions = documentIDPositions(docid, positions)
                  //val postingsList = ListBuffer[documentIDPositions]();
                  existingPostings.append(objdocumentIDPositions)
                  dictionaryForInvertedIndex += (individualToken -> existingPostings);
                  //                existingPostings.append(docid);
                  //                dictionaryForInvertedIndex += (individualToken -> existingPostings);
                }
                else {
                  //else create a new postings list as value and the token as key.


                  val objdocumentIDPositions = documentIDPositions(docid, positions)
                  val postingsList = ListBuffer[documentIDPositions]();
                  postingsList.append(objdocumentIDPositions)





                  dictionaryForInvertedIndex += (individualToken -> postingsList);

                }
              }
            }
          }

        }
      }

      printDictionaryPostings(dictionaryForInvertedIndex)


    } catch {
      case NonFatal(t) => {
        println(NonFatal.toString())
      }

      case ex: Exception => {
        println("An exception happened. Not able to find the file. Full stack trace is being printed as below")
        println(ex.toString())

      }
      case _: Throwable => {
        println("throwable exception found\n")
      }
        throw new FileNotFoundException(inputFileForInvIndex)
    }

  }

  def printDictionaryPostings(dictionaryPostings: Map[String, ListBuffer[documentIDPositions]]): Unit = {

    println("going to print postings list:")
    for ((k, v) <- dictionaryPostings) {
      print(k + "->")
      for ((postingsList) <- v) {
        val documentId = postingsList.docId
        print(documentId + ":")
        //print each of the positions in this document
        for (positions <- postingsList.positions) {
          //print in this format:
          //Gates: 1: 〈3〉; 2: 〈6〉; 3: 〈2,17〉; 4: 〈1〉;

          print(",<" + positions + ">")
        }
        print(";")
      }
      println("");


    }

  }

  //
  //  case class TermNotFoundException(excptn: String) extends Exception
  //
  //  def parseTheQueryGivenAll3Terms(term1Passed: String,term2Passed: String,operatorPassed: String): ListBuffer[Int] = {
  //    var returnList = ListBuffer[Int]()
  //    try {
  //      operatorPassed match {
  //        case "AND" => {
  //          //returnList = matchBooleanAndQuery(term1Passed, term2Passed, operatorPassed)
  //        }
  //        case "OR" =>
  //        {
  //          //returnList = matchBooleanORQuery(term1Passed, term2Passed, operatorPassed)
  //        }
  //        case _ => print("invalid operator.")
  //      }
  //    }
  //    catch{
  //      case ex: TermNotFoundException => println("The terms you entered for query doesn't exist in the given postings list. Try again.")
  //    }
  //    return returnList
  //  }
  //
  //
  //  def parseTheQuery(userQuery: String): ListBuffer[Int] = {
  //    var returnList = ListBuffer[Int]()
  //    try {
  //      operator match {
  //        case "AND" => {
  //          //returnList = matchBooleanAndQuery(term1, term2, operator)
  //        }
  //        case "OR" =>
  //        {
  //          // returnList = matchBooleanORQuery(term1, term2, operator)
  //        }
  //        case _ => print("invalid operator.")
  //      }
  //    }
  //    catch{
  //      case ex: TermNotFoundException => println("The terms you entered for query doesn't exist in the given postings list. Try again.")
  //    }
  //    return returnList
  //  }

  //  def conjunctionGivenListAndTerm(term1: String, term2Postings: ListBuffer[Int]): ListBuffer[Int] = {
  //    var conjList = new ListBuffer[Int]()
  //    var term1Postings = new ListBuffer[Int]()
  //    //var term2Postings = new ListBuffer[Int]()
  //    if (dictionaryForInvertedIndex.contains(term1)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term1Postings = dictionaryForInvertedIndex(term1);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //
  //    conjList = conjunction(term1Postings, term2Postings)
  //    return conjList;
  //
  //  }
  //
  //  def matchBooleanAndQuery(term1: String, term2: String, myOperator: String): ListBuffer[Int] = {
  //    var conjList = new ListBuffer[Int]()
  //
  //    var term1Postings = new ListBuffer[Int]()
  //    var term2Postings = new ListBuffer[Int]()
  //    if (dictionaryForInvertedIndex.contains(term1)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term1Postings = dictionaryForInvertedIndex(term1);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //    if (dictionaryForInvertedIndex.contains(term2)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term2Postings = dictionaryForInvertedIndex(term2);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //
  //    conjList = conjunction(term1Postings, term2Postings)
  //    return conjList;
  //
  //  }

  //  def matchBooleanORQuery(term1: String, term2: String, myOperator: String): ListBuffer[Int] = {
  //    var disjList = new ListBuffer[Int]()
  //
  //    var term1Postings = new ListBuffer[Int]()
  //    var term2Postings = new ListBuffer[Int]()
  //    if (dictionaryForInvertedIndex.contains(term1)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term1Postings = dictionaryForInvertedIndex(term1);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //    if (dictionaryForInvertedIndex.contains(term2)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term2Postings = dictionaryForInvertedIndex(term2);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //
  //    disjList = disjunction(term1Postings, term2Postings)
  //    return disjList;
  //
  //  }
  //

  //  def conjunction(postingsOfTerm1: ListBuffer[Int], postingsOfTerm2: ListBuffer[Int]): ListBuffer[Int] = {
  //    val conjunctedList = new ListBuffer[Int]();
  //    var childListCounter = 0
  //    var parentListCounter = 0
  //    var parentlist = new ListBuffer[Int]();
  //    var childlist = new ListBuffer[Int]();
  //    if (postingsOfTerm1.length > postingsOfTerm2.length) {
  //      parentlist = postingsOfTerm1
  //      childlist = postingsOfTerm2
  //    }
  //    else {
  //      parentlist = postingsOfTerm2
  //      childlist = postingsOfTerm1
  //    }
  //    while (parentListCounter < parentlist.length && childListCounter < childlist.length) {
  //      if (childlist(childListCounter) == parentlist(parentListCounter)) {
  //        conjunctedList += (childlist(childListCounter))
  //        childListCounter = childListCounter + 1
  //        parentListCounter = parentListCounter + 1
  //      }
  //      else {
  //        if (childlist(childListCounter) < parentlist(parentListCounter)) {
  //          childListCounter = childListCounter + 1
  //        }
  //        else {
  //          parentListCounter = parentListCounter + 1
  //        }
  //      }
  //    }
  //    return conjunctedList
  //
  //  }
  //
  //
  //  def disjunction(postingsOfTerm1: ListBuffer[Int], postingsOfTerm2: ListBuffer[Int]): ListBuffer[Int] = {
  //    val disjList = new ListBuffer[Int]();
  //    var childListCounter = 0
  //    var parentListCounter = 0
  //    var parentlist = new ListBuffer[Int]();
  //    var childlist = new ListBuffer[Int]();
  //    if (postingsOfTerm1.length > postingsOfTerm2.length) {
  //      parentlist = postingsOfTerm1
  //      childlist = postingsOfTerm2
  //    }
  //    else {
  //      parentlist = postingsOfTerm2
  //      childlist = postingsOfTerm1
  //    }
  //    while (parentListCounter < parentlist.length && childListCounter < childlist.length) {
  //      if (childlist(childListCounter) == parentlist(parentListCounter)) {
  //        disjList += (childlist(childListCounter))
  //        childListCounter = childListCounter + 1
  //        parentListCounter = parentListCounter + 1
  //      }
  //      else {
  //        if (childlist(childListCounter) < parentlist(parentListCounter)) {
  //          disjList += (childlist(childListCounter))
  //          childListCounter = childListCounter + 1
  //        }
  //        else {
  //          disjList += (parentlist(parentListCounter))
  //          parentListCounter = parentListCounter + 1
  //        }
  //      }
  //    }
  //
  //    //once we break out of the loop- which means the smaller list has finished, now write out the left over in parent list
  //    while (parentListCounter < parentlist.length) {
  //      disjList += parentlist(parentListCounter)
  //      parentListCounter = parentListCounter + 1
  //    }
  //    return disjList
  //
  //  }


  //  def verifyInputQueryStringForBinaryQuery(userQuery: String): Boolean = {
  //    println("verifying user input...")
  //    val queryContent = userQuery.split("\\s+");
  //    var flag = false;
  //    if (queryContent.length > 2) {
  //      term1 = queryContent(0);
  //      operator = queryContent(1);
  //      term2 = queryContent(2);
  //      if (operator == "AND" || operator == "OR") {
  //        println("yep,. Input query looks ok.")
  //        flag = true;
  //      }
  //      else {
  //        flag = false;
  //      }
  //    }
  //    else {
  //      flag = false;
  //    }
  //    return flag;
  //  }
}


