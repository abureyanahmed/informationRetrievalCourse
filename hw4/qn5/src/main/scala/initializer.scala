/**
  * Created by mithunpaul on 1/25/17.
  */
package SpamClassifier

import scala.io._
import util.control.Breaks._;
import brain._;

object initializer {

  //this code combines various functions
  def main(args: Array[String]): Unit = {


    /** *************
      * For Training.
      *
      * read training spam data into memory
      * For each file in training spam data, read through each lines.
      * for each word, add two hashmaps.
      * Token-SpamCount
      * Token-NonSpamCount
      *
      * Calculate total number of words in class spam
      * * Calculate total number of words in class not-spam
      * Calculate prior for each class
      *
      * For spam_map:
      * calculate sum of all token frequencies
      *
      * For each word in spam_map:
      * 1) calculate token fequency and store to another hashmap
      * ****************************************
      * For testing:
      * * For each file in testing spam data, read through each lines.
      * for each word,
      * calculate the Probability of being in class SPam and Class Non Spam.
      * Based on the classification, and whichever has highr MAP value, add label to another data structure
      * with docid,label, original label.
      * :
      * repeat the same for non-spam test dataset
      **
      *Calculate F1 score
      *
      * */
    myUtilities.readAndProcessTrainingData()

    //    println()
    //
    //    var queryString = ""
    //    breakable {
    //      while (true) {
    //        println("*************************************************")
    //        println("So, what would you like to do next?")
    //        println("Type 0 to exit.")
    //        println("Type 1 for Boolean proximity queries (non directional)")
    //        println("Type 2 for Boolean proximity queries (directional)")
    //
    //        println("Type your input here:")
    //        val typeOfProgram = StdIn.readLine()
    //
    //        if (typeOfProgram == "0") {
    //          println("Sad to see you leave. Do come back again. Bye.")
    //          sys.exit;
    //
    //        }
    //
    //
    //        else if (typeOfProgram == "1") {
    //          checkDirectionalProximity=false
    //          println()
    //          println("What two word positional query would you like to run on this index? ")
    //          println("Eg: schizophrenia /1 drug")
    //          println("Eg: new /2 for")
    //          println("Type your input here:")
    //
    //          //just basic parsing, checking number of words etc
    //          val queryStringForPos = StdIn.readLine()
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
    //          println()
    //        }
    //
    //        else if (typeOfProgram == "2") {
    //
    //          checkDirectionalProximity=true
    //
    //
    //          println()
    //          println("What two word positional DIRECTIONAL query would you like to run on this index? ")
    //          println("Eg: schizophrenia /1 drug")
    //          println("Eg: new /2 for")
    //          println("Type your input here:")
    //
    //          //just basic parsing, checking number of words etc
    //          val queryStringForPos = StdIn.readLine()
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
    //          println()
    //        }


  }
}