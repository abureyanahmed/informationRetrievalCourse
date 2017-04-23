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
      *
            * calculate the Probability of being in class SPam :
            *   i.e find prior of class spam from training data.
            *   for each word
            *     get its corresponding term weightage value for class spam
            *     product it all up (or sum it up, if you are taking log)

      * calculate the Probability of being in class SPam :
      *   i.e find prior of class spam from training data.
      *   for each word
      *     get its corresponding term weightage value for class spam
      *     product it all up (or sum it up, if you are taking log)
      *
      *     * Based on the classification, and whichever class has highr MAP value, add label to another data structure
      * with docid,label, original label.
      * :
       For each file in testing nonspam data, read through each lines.
      * for each word,
      * calculate the Probability of being in class SPam and Class Non Spam.
      * Based on the classification, and whichever has highr MAP value, add label to another data structure
      * with docid,gold,predicted labels.
      **
      *Calculate F1 score
      *
      * */
    myUtilities.readAndProcessTrainingData()


  }
}