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
    println("What query would you like to run on this index? Please capitalize the operator. Eg: approach AND drug. Type 0 to exit.")

    var queryString = ""
    breakable {
      while (true) {
        println(":")
        queryString = StdIn.readLine()

        if (queryString == "0") {
          println("Sad to see you leave. Do come back again. Bye.")
          sys.exit(0);

        }
        else {
          val verify = booleansearch.Utilities.verifyInputQueryStringForBinaryQuery(queryString)

          if (verify) {
            break();
          }

          else {
            println("Invalid query. Try again")

          }
        }
      }

    }
    println("Thank You. Below are the documents where you can find results for your query:" + queryString)
    booleansearch.Utilities.parseTheQuery(queryString)
  }
}
