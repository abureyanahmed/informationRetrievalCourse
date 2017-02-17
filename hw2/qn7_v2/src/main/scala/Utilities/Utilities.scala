package booleansearch

import java.io.{File, FileNotFoundException, InputStream}
import java.util

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


      val pathToInputFile=resourcesDirectory+inputFileForInvIndex;
      println("value of the path to the file is"+pathToInputFile)

      for (line <- io.Source.fromFile(pathToInputFile).getLines()) {
        //println("getting here at 1");
        val content = line.split("\\s+");
       // println("getting here at 2");
        var termCounter = 1;
        //println("getting here at 3");


        if (content.length > 1) {
         // println("getting here at 4");

          val docid = content(1).toInt;

          var positionOfTheTerm=0;

          //for each term in a document
          for (individualToken <- content) {


            //ignore the first two individualToken since it contains only "doc 1"
            if (termCounter <= 2) {
              termCounter = termCounter + 1;
            }

            else {
              //for each of the term you are seeing, get its position and add it to the postings list data structure
              //i am calling this the inner data structure.
              val positions = new ListBuffer[(Int)]
              positions.append(positionOfTheTerm);
              positionOfTheTerm = positionOfTheTerm + 1;

              //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back
              if (dictionaryForInvertedIndex.contains(individualToken)) {
                //                var baseCounter = 0;
                //                var existingPostings = dictionaryForInvertedIndex(individualToken);
                //                existingPostings.append(docid);
                //                dictionaryForInvertedIndex += (individualToken -> existingPostings);
              }
              else {
                //else create a new postings list as value and the token as key.

                //                case class documentIDPositions (var docId:Int, var positions: ListBuffer[Int]);
                //                var dictionaryForInvertedIndex: Map[String, ListBuffer[documentIDPositions]] = Map();
                //

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
      case NonFatal(t) => {println(NonFatal.toString())}
      case _: Throwable => {println("throwable exception found\n")}
      case ex: Exception => {
        println("An exception happened. Not able to find the file. Full stack trace is being printed as below")
        println(ex.toString())
        System.exit(1);
      }
        throw new FileNotFoundException(inputFileForInvIndex)
    }

  }

  def printDictionaryPostings(dictionaryPostings: Map[String, ListBuffer[documentIDPositions]]): Unit = {

    for ((k, v) <- dictionaryPostings) {
      println(k + "->" )
      for ((postingsList) <- dictionaryPostings) {
        val documentId=postingsList._1
        println(documentId+ "->" )
      }


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


