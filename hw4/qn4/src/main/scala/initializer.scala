//package GradabilityClassifier
//testing for push from chung

package initializer


import scala.io._
import util.control.Breaks._;

import scala.collection.mutable.ArrayBuffer

object initializer {
  def main(args: Array[String]) = println("Exiting main program")

  println("Hello, welcome to world of Language Model Information Retrieval ")

  println("We are first going to read the document provided as input.")


  try {


    myUtilities.readFromFile()

    var queryString = ""
    breakable {
      while (true) {
        println("*************************************************")
        println("So, what query would you like to enter: ")
        println("Type 0 to exit.")

        println("Type your input here:")
        //val typeOfProgram = StdIn.readLine()
        val queryStringForPos = StdIn.readLine()

        if (queryStringForPos == "0") {
          println("Sad to see you leave. Do come back again. Bye.")
          sys.exit;

        }


        else {
          //var query = "information retrieval"
          var query = queryStringForPos

          println()


          //just basic parsing, checking number of words etc
          //
          //          parse(parWordOperator, queryStringForPos) match {
          //            case Success(matched, _) => {
          //              //println("Success. Found a result for the query you asked.");
          //            }
          //            case Failure(msg, _) => {
          //              println("There is something wrong with the query you entered.: " + msg)
          //
          //            }
          //
          //            case Error(msg, _) => println("ERROR: " + msg)
          //
          //          }
          println()




          //hard coded query for the time being.


          myUtilities.parseQueryAndCalculateScores(query)

          println()

        }
      }
    }
  }


  catch {
    // handling any other exception that might come up
    case unknown: Throwable => println("Got this unknown exception: " + unknown.printStackTrace)
  }
}