
package brain
import scala.util.matching.Regex
import java.io._
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


  //list of input paths
  val resourcesDirectory = "./src/main/resources/"
  val inputDirectoryForTrainingSpam = "spam-train";
  val inputDirectoryForTrainingNSpam = "nonspam-train";

  //list of output files and paths
  val outputDirectoryPath = "./src/main/outputs/"


  val filemapTrTokenSpam ="mapTrTokenSpam.txt"
  val filemapTrTokenNonSpam ="mapTrTokenNonSpam.txt"
  val filelistOfAllTrTokens ="listOfAllTrTokens.txt"
  val filespamWeightage ="spamWeightage.txt"
  val filenonSpamWeightage ="nonSpamWeightage.txt"



  def readAndProcessTrainingData() = {


    //read spam training data
    var fullScrapedDirectoryPath = resourcesDirectory + inputDirectoryForTrainingSpam


    //list of data structures
    var mapTrTokenSpam: Map[String, Int]= Map();
    var mapTrTokenNonSpam: Map[String, Int] = Map();
    var listOfAllTrTokens : Map[String, Int] = Map();
    var spamWeightage : Map[String, Double] = Map();
    var nonSpamWeightage : Map[String, Double] = Map();


    //list of variables
    var totalSpamTokenFrequency:Double=0
    var totalNonSpamTokenFrequency:Double=0
    var noofSpamFiles:Double=0
    var noofNonSpamFiles:Double=0

    if (checkFolderExists(fullScrapedDirectoryPath)) {
       noofSpamFiles = new File(fullScrapedDirectoryPath).listFiles().length
      readTrainingData(fullScrapedDirectoryPath,mapTrTokenSpam)

    }


    //read nonspam training data
    val nonSpamTrainingFolder = resourcesDirectory + inputDirectoryForTrainingNSpam
    if (checkFolderExists(nonSpamTrainingFolder)) {
      noofNonSpamFiles = new File(nonSpamTrainingFolder).listFiles().length
      readTrainingData(nonSpamTrainingFolder,mapTrTokenNonSpam)

    }

    val totalTrainingFiles:Double=noofNonSpamFiles+noofSpamFiles
    val SpamPrior:Double=noofSpamFiles/totalTrainingFiles
    val NonSpamPrior:Double=noofNonSpamFiles/totalTrainingFiles

    println("value of SpamPrior is:" + SpamPrior)
    println("value of NonSpamPrior is:" + NonSpamPrior)


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

    for((nonSpamToken,nonSpamfreq)<-mapTrTokenNonSpam)
    {
      totalNonSpamTokenFrequency=totalNonSpamTokenFrequency+nonSpamfreq
      if (listOfAllTrTokens.contains(nonSpamToken)) {
        //check for unique. add only if doesnt exist.
      }
      else {
        listOfAllTrTokens += (nonSpamToken -> 1)
      }
    }

    println("no of lines in mapTrTokenNonSpam is:" + mapTrTokenNonSpam.size)
    println("no of lines in mapTrTokenSpam is:" + mapTrTokenSpam.size)
    println("no of lines in listOfAllTrTokens is:" + listOfAllTrTokens.size)
    println("value of totalSpamTokenFrequency is:" + totalSpamTokenFrequency)
    println("value of totalNonSpamTokenFrequency is:" + totalNonSpamTokenFrequency)


    calculateTermWeightage(totalSpamTokenFrequency,totalNonSpamTokenFrequency,mapTrTokenSpam,mapTrTokenNonSpam,listOfAllTrTokens , spamWeightage ,nonSpamWeightage )

    //write all the data structures to file for verification
    writeToFile(mapTrTokenNonSpam.mkString("\n"),filemapTrTokenNonSpam,outputDirectoryPath)
    writeToFile(mapTrTokenSpam.mkString("\n"),filemapTrTokenSpam,outputDirectoryPath)
    writeToFile(listOfAllTrTokens.mkString("\n"),filelistOfAllTrTokens,outputDirectoryPath)
    writeToFile(nonSpamWeightage.mkString("\n"),filenonSpamWeightage,outputDirectoryPath)
    writeToFile(spamWeightage.mkString("\n"),filespamWeightage,outputDirectoryPath)


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

  def calculateTermWeightage(totalSpamTokenFrequency:Double,totalNonSpamTokenFrequency:Double,
                              mapTrTokenSpam: Map[String, Int],mapTrTokenNonSpam: Map[String, Int] ,
                              listOfAllTrTokens : Map[String, Int] , spamWeightage : Map[String, Double],nonSpamWeightage : Map[String, Double]) = {

    //go through the list of all unique tokens, calculate spam weightage for each
    var totalUniqTokenCount=listOfAllTrTokens.size


    for((alltokens,myvalues)<-listOfAllTrTokens)
      {

        var spamFrequency=0
        //for each unique token, get its spam frequency, add 1,
        if(mapTrTokenSpam.contains(alltokens)) {
          spamFrequency = mapTrTokenSpam(alltokens)
          spamFrequency = spamFrequency + 1
        }
        else
          {
            spamFrequency = spamFrequency + 1
          }

        // divide it by (total spam term frequency+ total number of tokens- i.e length of listOfAllTrTokens)
        var spamWeightageOfThisToken=spamFrequency/(totalUniqTokenCount+totalSpamTokenFrequency)

        //add it to spam weightage Map
        spamWeightage += (alltokens -> spamWeightageOfThisToken)



        //do the same for non spam weightage

        var nonSpamFrequency=0
        //for each unique token, get its spam frequency, add 1,
        if(mapTrTokenNonSpam.contains(alltokens)) {
          nonSpamFrequency = mapTrTokenNonSpam(alltokens)
          nonSpamFrequency = nonSpamFrequency + 1
        }
        else
        {
          nonSpamFrequency = nonSpamFrequency + 1
        }

        // divide it by (total spam term frequency+ total number of tokens- i.e length of listOfAllTrTokens)
        var nonspamWeightageOfThisToken=nonSpamFrequency/(totalUniqTokenCount+totalNonSpamTokenFrequency)

        //add it to spam weightage Map
        nonSpamWeightage += (alltokens -> spamWeightageOfThisToken)



      }

    println("no of lines in totalUniqTokenCount is:" + totalUniqTokenCount)
    println("no of lines in spamWeightage is:" + spamWeightage.size)
    println("no of lines in nonSpamWeightage is:" + nonSpamWeightage.size)





  }

  def writeToFile(stringToWrite: String, outputFilename: String, outputDirectoryPath: String): Unit = {

    val outFileoutputFileForThisNewsArticle = new File(outputDirectoryPath, outputFilename)
    //remove if it exists. And create a new one to append And keep adding to it- in the for loop below.
    if (outFileoutputFileForThisNewsArticle.exists) {
      outFileoutputFileForThisNewsArticle.delete()
    }

//    // create a new file of the same name and write into it some emptyline
//    val file2 = new File(outputDirectoryPath + outputFilename)
//    val bw1 = new BufferedWriter(new FileWriter(file2))
//    bw1.write("")
//    bw1.close()


    val outFile = new File(outputDirectoryPath, outputFilename)
    val bw = new BufferedWriter(new FileWriter(outFile))
    bw.write(stringToWrite)
    bw.close()


  }
}