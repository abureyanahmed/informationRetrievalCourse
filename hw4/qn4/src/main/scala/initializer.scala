//package GradabilityClassifier
//testing for push from chung

package initializer



import scala.collection.mutable.ArrayBuffer

object initializer {
  def main(args: Array[String]) = println("Exiting main program")


  try {

    myUtilities.readFromFile()

    //hard coded query for the time being.
    var query="information retrieval"

    myUtilities.parseQueryAndCalculateScores(query)

    println()

    }


  catch {
    // handling any other exception that might come up
    case unknown: Throwable => println("Got this unknown exception: " + unknown.printStackTrace)
  }
}