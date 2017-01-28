package booleansearch

import java.io.{FileNotFoundException, InputStream}
import java.util

import scala.collection.mutable
import scala.collection.mutable._
import scala.io.Source
import scala.util.Try
import scala.annotation.switch

/**
  * Created by mithunpaul on 1/25/17.
  */



object  Utilities {

  val resourcesDirectory = "src/main/resources/"
  val inputFileForInvIndex = "inputfile.txt";
  var dictionaryForInvertedIndex:  Map [String, ListBuffer[Int]] = Map();
  var term1 = "";
  var operator = "";
  var term2 = "";

  def readFromFile() = {
    try {
      for (line <- Source.fromResource(inputFileForInvIndex).getLines()) {
        val content = line.split("\\s+");
        var termCounter = 1;


        if (content.length > 1) {

          val docid = content(1).toInt;

          //for each term in a document
          for (individualToken <- content) {

            //ignore the first two individualToken since it contains only "doc 1"
            if (termCounter <= 2) {
              termCounter = termCounter + 1;
            }

            else {
              if (dictionaryForInvertedIndex.contains(individualToken)) {
                //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back


                var baseCounter = 0;
                var existingPostings = dictionaryForInvertedIndex(individualToken);
                existingPostings.append(docid);
                dictionaryForInvertedIndex += (individualToken -> existingPostings);
              }
              else {
                //else create a new postings list as value and the token as key.
                val postings = new ListBuffer[(Int)]
                postings.append(docid);
                dictionaryForInvertedIndex += (individualToken -> postings);

              }
            }
          }

        }
      }

      printDictionaryPostings(dictionaryForInvertedIndex)


    } catch {

      case ex: Exception => println("An exception happened. Not able to find the file")
        throw new FileNotFoundException(inputFileForInvIndex)
    }

  }

  def printDictionaryPostings(dictionaryPostings: Map[String, ListBuffer[(Int)]]): Unit = {

    for ((k, v) <- dictionaryPostings) {
      println(k + "->" + v.mkString("->"))
    }

  }

  def parseTheQuery(userQuery: String): Unit = {
    operator match {
      case "AND" => {
        val conjunctedList= matchBooleanAndQuery(term1, term2, operator)
        println("Result:"+ conjunctedList.mkString(","))
      }
      case "OR" => print("operator is OR")
      case _ => print("invalid operator.")
    }
  }

  def matchBooleanAndQuery(term1: String, term2: String, myOperator: String): ListBuffer[Int] = {
    var conjList= new ListBuffer[Int]()

    var term1Postings=new ListBuffer[Int]()
    var term2Postings=new ListBuffer[Int]()
    if (dictionaryForInvertedIndex.contains(term1)) {
      //if the term is already present in the dictionary, retreive its postings list
       term1Postings = dictionaryForInvertedIndex(term1);
    }
    if (dictionaryForInvertedIndex.contains(term2)) {
      //if the term is already present in the dictionary, retreive its postings list
      term2Postings = dictionaryForInvertedIndex(term2);
    }
//    println("the postings for term 1 is:")
//    println(term1Postings)
//
//    println("the postings for term 2 is:")
//    println(term2Postings)

    conjList=conjunction(term1Postings,term2Postings)
    return conjList;

  }

  def conjunction(postingsOfTerm1: ListBuffer[Int], postingsOfTerm2: ListBuffer[Int]):ListBuffer[Int]=
  {
    val conjunctedList= new ListBuffer[Int]();
    var childListCounter=0
    var parentListCounter=0
    var parentlist=new ListBuffer[Int]();
    var childlist=new ListBuffer[Int]();
    if(postingsOfTerm1.length > postingsOfTerm2.length) {
       parentlist = postingsOfTerm1
       childlist = postingsOfTerm2
    }
    else {
      parentlist = postingsOfTerm2
      childlist = postingsOfTerm1
    }
    while(parentListCounter< parentlist.length && childListCounter < childlist.length) {
      if (childlist(childListCounter) == parentlist(parentListCounter)) {
        conjunctedList+=(childlist(childListCounter))
        childListCounter = childListCounter + 1
        parentListCounter = parentListCounter + 1
      }
      else {
        if (childlist(childListCounter) < parentlist(parentListCounter)) {
          childListCounter = childListCounter + 1
        }
        else {
          parentListCounter = parentListCounter + 1
        }
      }
    }

    //once we break out of the loop- which means the smaller list has finished, now write out the left over in parent list
    while (parentListCounter < parentlist.length) {
      conjunctedList+=parentlist(parentListCounter)
      parentListCounter = parentListCounter + 1
    }
    return conjunctedList

  }
  def verifyInputQueryStringForBinaryQuery(userQuery: String): Boolean = {
    println("verifying user input...")
    val queryContent = userQuery.split("\\s+");
    var flag = false;
    if (queryContent.length > 1) {
      term1 = queryContent(0);
      operator = queryContent(1);
      term2 = queryContent(2);
      if (operator == "AND" || operator == "OR") {
        println("yep,. Input query looks ok.")
        flag = true;
      }
      else {
        flag = false;
      }
    }
    else {
      flag = false;
    }
    return flag;
  }
}


