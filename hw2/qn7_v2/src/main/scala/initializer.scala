/**
  * Created by mithunpaul on 1/25/17.
  */
package initializer

import scala.io._
import util.control.Breaks._;
import parsercombinators.SimpleParser;

object initializer  extends SimpleParser {

  //there is confusion if the first word is going to be doc1 or doc space 1- writing code for both separated by a boolean flag
  val useDoc1 = false;

  //main used for including qn5.3
  def main(args: Array[String]): Unit = {

    println("Hi Siri, welcome to world of Boolean Information Retrieval- HW2")
    println("We are first going to print the dictionary-postings inverted index for the given input file.")
    println()
    booleansearch.Utilities.readFromFile()

    println()

    var queryString = ""
    breakable {
      while (true) {
        println("*************************************************")
        println("What would you like to do?")
        println("Type 0 to exit.")
        println("Type 1 for Boolean proximity queries (non directional)")
        println("Type 2 for Boolean proximity queries (directional)")

        println("Type your input here:")
        val typeOfProgram = StdIn.readLine()

        if (typeOfProgram == "0") {
          println("Sad to see you leave. Do come back again. Bye.")
          sys.exit;

        }


        else if (typeOfProgram == "1") {
          println()
          println("What two word positional query would you like to run on this index? ")
          println("Eg: schizophrenia /2 drug")
          println("Eg: breakthrough /3 new")
          println("Type your input here:")

          //just basic parsing, checking number of words etc

          val queryStringForPos = StdIn.readLine()
          parse(parWordOperator, queryStringForPos) match {
            case Success(matched, _) => {
              println("Success. Found a result for the query you asked.");
            }
            case Failure(msg, _) => {
              println("There is something wrong with the query you entered.: " + msg)
              //              parse(parWordOperatorWordPar, queryStringForPos) match {
              //                case Success(matched, _) => {
              //                  println("Found that :" + matched)
              //                }
              //case Failure(msg, _) => println("There is something wrong with the query you entered.: " + msg)


            }
            //println("There is something wrong with the query you entered.: " + msg)


            case Error(msg, _) => println("ERROR: " + msg)

          }


          //           val queryResult = booleansearch.Utilities.parseTheQuery(queryString)
          //          parse(queryString)
          //          SimpleParser.parse(SimpleParser.word(myString))

          //            if (queryResult.length > 0) {
          //              println("Thank You. The documents in which you can find the results for your query:\"" + queryString + "\" are document ids: " +
          //                "" + queryResult.mkString(","))
          //            }
          //            else {
          //              println("Thank You. Unfortunately, there were no documents that matched your query :\"" + queryString + "\". Please try again with another query.")
          //            }
          println()
        }
        //          else {
        //            println("Invalid query. Try again")
        //            println()
        //          }


        //        else if (typeOfProgram == "2") {
        //
        //          println("What multi word  query would you like to run on this index? Please capitalize the operator as shown in Examples below.")
        //          println("Eg: (drug OR treatment) AND schizophrenia")
        //          println("Type your input here:")
        //          val queryStringForMl = StdIn.readLine()
        //          parse(parWordOperator, queryStringForMl) match {
        //            case Success(matched, _) => {
        //              println("Found that :" + matched)
        //            }
        //            case Failure(msg, _) => {
        //              parse(parWordOperatorWordPar, queryStringForMl) match {
        //                case Success(matched, _) => {
        //                  println("Found that :" + matched)
        //                }
        //                case Failure(msg, _) => println("There is something wrong with the query you entered.: " + msg)
        //                case Error(msg, _) => println("ERROR: " + msg)
        //
        //              }
        //              //println("There is something wrong with the query you entered.: " + msg)
        //            }
        //            case Error(msg, _) => println("ERROR: " + msg)
        //
        //          }
        ////
        ////
        ////
        ////        }
        //
        //      }
      }
    }
  }
}