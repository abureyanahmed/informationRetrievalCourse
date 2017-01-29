/**
  * Created by mithunpaul on 1/25/17.
  */
package initializer

import booleansearch._

import scala.io._
import util.control.Breaks._
import booleansearch._
import parsercombinators.SimpleParser;

object initializer extends SimpleParser{

  //this is the main function for qn1 and qn2. Commenting it to test parser for qn3
//  def main(args: Array[String]): Unit = {
//
//    println("Hi Siri, welcome to world of boolean retrieval")
//    println("We are first going to print the dictionary-postings inverted index for the given input file.")
//    println()
//    booleansearch.Utilities.readFromFile()
//    println()
//
//    var queryString = ""
//    breakable {
//      while (true) {
//        println("*************************************************")
//        println("What query would you like to run on this index? Please capitalize the operator as shown in Examples below.")
//        println("Eg: schizophrenia AND drug")
//        println("Eg: breakthrough OR new")
//        println("Type 0 to exit.")
//
//        println("Type your input here:")
//        queryString = StdIn.readLine()
//
//        if (queryString == "0") {
//          println("Sad to see you leave. Do come back again. Bye.")
//          sys.exit;
//
//        }
//        else {
//          val verify = booleansearch.Utilities.verifyInputQueryStringForBinaryQuery(queryString)
//          if (verify) {
//            val queryResult = booleansearch.Utilities.parseTheQuery(queryString)
//            if (queryResult.length > 0) {
//              println("Thank You. The documents in which you can find the results for your query:\"" + queryString + "\" are document ids: " + queryResult.mkString(","))
//            }
//            else {
//              println("Thank You. Unfortunately, there were no documents that matched your query :\"" + queryString + "\". Please try again with another query.")
//            }
//            println()
//          }
//          else {
//            println("Invalid query. Try again")
//            println()
//          }
//        }
//      }
//
//    }
//  }


  //main used for including qn5.3
  def main(args: Array[String]): Unit = {

    println("Hi Siri, welcome to world of Boolean Information Retrieval")
    println("We are first going to print the dictionary-postings inverted index for the given input file.")
    println()
    booleansearch.Utilities.readFromFile()
    println()

    var queryString = ""
    breakable {
      while (true) {
        println("*************************************************")
        println("Type 0 to exit.")
        println("Type 1 for simple two word boolean queries .")
        println("Type 2 for multiword boolean queries .")

        println("Type your input here:")
        val typeOfProgram = StdIn.readLine()

        if (typeOfProgram == "0") {
          println("Sad to see you leave. Do come back again. Bye.")
          sys.exit;

        }


        else  if (typeOfProgram == "1"){
          println()
          println("What boolean two word simple query would you like to run on this index? Please capitalize the operator as shown in Examples below.")
          println("Eg: schizophrenia AND drug")
          println("Eg: breakthrough OR new")
          println("Type your input here:")
          queryString = StdIn.readLine()
          val verify = booleansearch.Utilities.verifyInputQueryStringForBinaryQuery(queryString)
          if (verify) {
            val queryResult = booleansearch.Utilities.parseTheQuery(queryString)
            if (queryResult.length > 0) {
              println("Thank You. The documents in which you can find the results for your query:\"" + queryString + "\" are document ids: " + queryResult.mkString(","))
            }
            else {
              println("Thank You. Unfortunately, there were no documents that matched your query :\"" + queryString + "\". Please try again with another query.")
            }
            println()
          }
          else {
            println("Invalid query. Try again")
            println()
          }
        }

        else  if (typeOfProgram == "2"){

          println("What multi word  query would you like to run on this index? Please capitalize the operator as shown in Examples below.")
          println("Eg: (drug OR treatment) AND schizophrenia")
          println("Type your input here:")
          val queryStringForMl = StdIn.readLine()
          println(parse(word, queryStringForMl))

        }
      }

    }
  }
}