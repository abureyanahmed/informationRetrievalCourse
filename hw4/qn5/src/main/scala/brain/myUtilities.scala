
package brain
import scala.util.matching.Regex
import java.io.{File, FileNotFoundException, InputStream}
import java.util

import scala.collection.mutable
import scala.collection.mutable._
import scala.io.Source
import scala.util.Try
import scala.annotation.switch
import scala.util.control.NonFatal
import dataStructures._;
/**
  * Created by mithunpaul on 1/25/17.
  */


object  myUtilities {

  //the class where all the functions are stored.
  val resourcesDirectory = "./src/main/resources/"
  val inputDirectoryForTrainingSpam = "spam-train";
  val inputDirectoryForTrainingNSpam = "nonspam-train";



  def readAndProcessTrainingData() = {


    //read spam training data
    var fullScrapedDirectoryPath = resourcesDirectory + inputDirectoryForTrainingSpam


    //list of data structures
    var mapTrTokenSpam: Map[String, Int]= Map();
    var mapTrTokenNonSpam: Map[String, Int] = Map();
    var listOfAllTrTokens : Map[String, Int] = Map();


    //list of variables
    var totalSpamTokenFrequency:Double=0
    var totalNonSpamTokenFrequency:Double=0
    var noofSpamFiles:Double=0
    var noofNonSpamFiles:Double=0

    if (checkFolderExists(fullScrapedDirectoryPath)) {
       noofSpamFiles = new File(fullScrapedDirectoryPath).listFiles().length
      readTrainingData(fullScrapedDirectoryPath,mapTrTokenSpam)
      println("no of lines in mapTrTokenSpam is:" + mapTrTokenSpam.size)
    }


    //read nonspam training data
    val nonSpamTrainingFolder = resourcesDirectory + inputDirectoryForTrainingNSpam
    if (checkFolderExists(nonSpamTrainingFolder)) {
      noofNonSpamFiles = new File(nonSpamTrainingFolder).listFiles().length
      readTrainingData(nonSpamTrainingFolder,mapTrTokenNonSpam)
      println("no of lines in mapTrTokenNonSpam is:" + mapTrTokenNonSpam.size)
    }

    val totalTrainingFiles:Double=noofNonSpamFiles+noofSpamFiles
    val SpamPrior:Double=noofSpamFiles/totalTrainingFiles
    val NonSpamPrior:Double=noofNonSpamFiles/totalTrainingFiles

    println("value of SpamPrior is:" + SpamPrior)
    println("value of NonSpamPrior is:" + NonSpamPrior)


    /* var listOfAllTrTokens : Map[String, Int] = Map();


    //list of variables
    var totalSpamTokenFrequency:Double=0
    var totalNonSpamTokenFrequency:Double=0*/

    //combine tokens in both hashtable to get a total unique set of tokens. Also calculate total frequencies in each classe
    for((spamToken,freq)<-mapTrTokenSpam)
      {
        totalSpamTokenFrequency=totalSpamTokenFrequency+freq
        if (listOfAllTrTokens.contains(spamToken)) {
          //check for unique. add only if doesnt exist.
        }
        else {
          listOfAllTrTokens += (spamToken -> 1)
        }
      }

    //do the same for non spam hashtable also

    for((nonSpamToken,nonSpamfreq)<-mapTrTokenSpam)
    {
      totalNonSpamTokenFrequency=totalNonSpamTokenFrequency+nonSpamfreq
      if (listOfAllTrTokens.contains(nonSpamToken)) {
        //check for unique. add only if doesnt exist.
      }
      else {
        listOfAllTrTokens += (nonSpamToken -> 1)
      }
    }

    println("value of totalSpamTokenFrequency is:" + totalSpamTokenFrequency)
    println("value of totalNonSpamTokenFrequency is:" + totalNonSpamTokenFrequency)
  }

  def checkFolderExists(fullScrapedDirectoryPath: String): Boolean = {


    var noofFiles = 0

    val inputDirectoryToList = new File(fullScrapedDirectoryPath)
    if (inputDirectoryToList != None) {
      noofFiles = inputDirectoryToList.listFiles().length
    }
    else {
      println("input directory is empty")
      return false;

    }
    var documentCount = 1;

    if (noofFiles == 0) {
      //todo: throw an error here
      println("no files in the input directory")
      return false;

    }
    else {
      return true;
    }

  }

  def readTrainingData(folderToReadFrom: String, mapTrTokenSpam: Map[String, Int]= Map()) = {
    val listOfFiles = new File(folderToReadFrom).listFiles()
    var fileCounter = 0;
    for (indivFileName <- listOfFiles) {
      for (lineFromInput <- Source.fromFile(indivFileName).getLines()) {
        val words = lineFromInput.split("\\s+")
        for (wordToTrim <- words) {
          var indivWord = wordToTrim.trim();
          if (mapTrTokenSpam.contains(indivWord)) {
            var wordCounter = mapTrTokenSpam(indivWord)
            wordCounter = wordCounter + 1
            mapTrTokenSpam.put(indivWord, wordCounter);
          }
          else {
            if(mapTrTokenSpam != " ")
            mapTrTokenSpam += (indivWord -> 1)
          }
        }
      }
    }
  }

  def calculatePriors() = {

  }

}