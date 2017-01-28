/**
  * Created by mithunpaul on 1/25/17.
  */
package initializer

import booleansearch._
import scala.io._
import util.control.Breaks._

object initalizer {
  def main(args: Array[String]): Unit = {

    println("Hi Siri, welcome to world of boolean retrieval")
    println("We are first going to print the dictionary-postings inverted index for the given input file.")
    println()
    booleansearch.Utilities.readFromFile()
    println()

    var queryString = ""
    breakable {
      while (true) {
        println("What query would you like to run on this index? Please capitalize the operator. Eg: approach AND drug. Type 0 to exit.")
        println(":")
        queryString = StdIn.readLine()

        if (queryString == "0") {
          println("Sad to see you leave. Do come back again. Bye.")
          sys.exit(0);

        }
        else {
          val verify = booleansearch.Utilities.verifyInputQueryStringForBinaryQuery(queryString)
          if (verify) {
            val queryResult = booleansearch.Utilities.parseTheQuery(queryString)
            if(queryResult.length>0) {
              println("Thank You. The documents in which you can find the results for your query:" + queryString + " are document ids:" + queryResult.mkString(","))
            }
            println("*************************************************")
            println()
          }
          else {
            println("Invalid query. Try again")
          }
        }
      }

    }
  }
}