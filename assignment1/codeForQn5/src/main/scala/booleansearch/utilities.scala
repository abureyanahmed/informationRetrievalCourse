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
  var dictionaryForInvertedIndex: Map[String, ListBuffer[(Integer)]] = Map()
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
                var postings = new ListBuffer[(Integer)]
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

  def printDictionaryPostings(dictionaryPostings: Map[String, ListBuffer[(Integer)]]): Unit = {

    for ((k, v) <- dictionaryPostings) {
      println(k + "->" + v.mkString("->"))
    }

  }

  def parseTheQuery(userQuery: String): Unit =
  {
    operator match{
      case "AND" => println("operator is AND")
      case "OR" => print("operator is OR")
      case _ => print("invalid operator.")
    }

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


