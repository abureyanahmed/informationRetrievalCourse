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

  var checkDirectionalProximity=false;

  //main used for including qn5.3
  def main(args: Array[String]): Unit = {

    println("Hello, welcome to world of Boolean Information Retrieval with proximity indicators for HW2")
    println("We are first going to print the dictionary-postings inverted index for the given input file, including positions.")
    println()
    booleansearch.Utilities.readFromFile()

    println()

    var queryString = ""
    breakable {
      while (true) {
        println("*************************************************")
        println("So, what would you like to do next?")
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
          checkDirectionalProximity=false
          println()
          println("What two word positional query would you like to run on this index? ")
          println("Eg: schizophrenia /1 drug")
          println("Eg: new /2 for")
          println("Type your input here:")

          //just basic parsing, checking number of words etc
          val queryStringForPos = StdIn.readLine()
          parse(parWordOperator, queryStringForPos) match {
            case Success(matched, _) => {
              //println("Success. Found a result for the query you asked.");
            }
            case Failure(msg, _) => {
              println("There is something wrong with the query you entered.: " + msg)

            }

            case Error(msg, _) => println("ERROR: " + msg)

          }
          println()
        }

        else if (typeOfProgram == "2") {

          checkDirectionalProximity=true


          println()
          println("What two word positional DIRECTIONAL query would you like to run on this index? ")
          println("Eg: schizophrenia /1 drug")
          println("Eg: new /2 for")
          println("Type your input here:")

          //just basic parsing, checking number of words etc
          val queryStringForPos = StdIn.readLine()
          parse(parWordOperator, queryStringForPos) match {
            case Success(matched, _) => {
              //println("Success. Found a result for the query you asked.");
            }
            case Failure(msg, _) => {
              println("There is something wrong with the query you entered.: " + msg)

            }

            case Error(msg, _) => println("ERROR: " + msg)

          }
          println()
        }

      }
    }
  }
}