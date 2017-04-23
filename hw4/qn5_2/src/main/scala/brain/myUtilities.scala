
package brain
import scala.util.matching.Regex
import java.io._
import java.util
import scala.math._
import scala.collection.mutable
import scala.collection.mutable.{ListBuffer, _}
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
  val inputDirectoryForTestingSpam = "spam-test";
  val inputDirectoryForTestingNSpam = "nonspam-test";

  //list of output files and paths
  val outputDirectoryPath = "./src/main/outputs/"


  val filemapTrTokenSpam ="mapTrTokenSpam.txt"
  val filemapTrTokenNonSpam ="mapTrTokenNonSpam.txt"
  val filelistOfAllTrTokens ="listOfAllTrTokens.txt"
  val filespamWeightage ="spamWeightage.txt"
  val filenonSpamWeightage ="nonSpamWeightage.txt"
  val fileGoldPredLabels ="fileGoldPredLabels.txt"
  val fileLogFile ="fileLogFile.txt"

  case class goldPredictedLabel(var docId:String, var goldLabel:String, var predictedLabel:String);





  def readAndProcessTrainingData() = {


    /************************Training Part*********************/

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
    writeToFile("LogFile:\n",fileLogFile ,outputDirectoryPath)


    /************************Testing Part*********************/


    //list of data structures
    //var predictedLabels: Map[String, String, String]= Map();
    //var mapTrTokenSpam: Map[String, Int]= Map();


    //antonym adjectivePairs found for a given template
    var listGoldPredictedLabel = new ListBuffer[goldPredictedLabel]()


    processTestingData( spamWeightage,nonSpamWeightage , SpamPrior,NonSpamPrior,listGoldPredictedLabel)



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

    val outFile = new File(outputDirectoryPath, outputFilename)
    val bw = new BufferedWriter(new FileWriter(outFile))
    bw.write(stringToWrite)
    bw.close()


  }

  def processTestingData( spamWeightage : Map[String, Double],nonSpamWeightage : Map[String, Double], SpamPrior:Double,nonSpamPrior:Double ,listOfGoldPredictedLabel: ListBuffer[goldPredictedLabel]): Unit =
  {

    //read and predict spam training data
    var goldLabel="spam"
    var fullPathinputDirectoryForTestingSpam = resourcesDirectory + inputDirectoryForTestingSpam
    getPrediction(goldLabel,fullPathinputDirectoryForTestingSpam,spamWeightage : Map[String, Double],nonSpamWeightage : Map[String, Double], SpamPrior:Double,nonSpamPrior:Double ,listOfGoldPredictedLabel: ListBuffer[goldPredictedLabel])


    println("no of lines in listOfGoldPredictedLabel is:" + listOfGoldPredictedLabel.size)

    //read and predict nonspam training data
    goldLabel="non-spam"
    var fullPathinputDirectoryForTestingNonSpam = resourcesDirectory + inputDirectoryForTestingNSpam
    getPrediction(goldLabel,fullPathinputDirectoryForTestingSpam,spamWeightage : Map[String, Double],nonSpamWeightage : Map[String, Double], SpamPrior:Double,nonSpamPrior:Double ,listOfGoldPredictedLabel: ListBuffer[goldPredictedLabel])


    println("no of lines in listOfGoldPredictedLabel is:" + listOfGoldPredictedLabel.size)


    writeToFile(listOfGoldPredictedLabel.mkString("\n"),fileGoldPredLabels,outputDirectoryPath)




  }


  def getPrediction( goldLabel:String,  fullPathinputDirectoryForTestingSpam:String, spamWeightage : Map[String, Double],nonSpamWeightage : Map[String, Double], SpamPrior:Double,nonSpamPrior:Double ,listOfGoldPredictedLabel: ListBuffer[goldPredictedLabel]): Unit =
  {


    if (checkFolderExists(fullPathinputDirectoryForTestingSpam)) {
      //read spam-testing data

      val listOfFiles = new File(fullPathinputDirectoryForTestingSpam).listFiles()
      var fileCounter = 0;
      for (indivFileName <- listOfFiles) {

        /* For each file in testing spam data, read through each lines.

        calculate the Probability of being in class Spam :
    *   i.e find prior of class spam from training data.
    *
    *   val SpamPrior:Double
    *   */

        var sumofTermWeightsSpam:Double=0
        var sumofTermWeightsNonSpam:Double=0




        for (lineFromInput <- Source.fromFile(indivFileName).getLines()) {
          val words = lineFromInput.split("\\s+")
          for (wordToTrim <- words) {

            var indivWord = wordToTrim.trim();

            /*for each word     *     get its corresponding term weightage value for class spam*/


            if (spamWeightage.contains(indivWord)) {
              var mySpamWeightage = spamWeightage(indivWord)

              /*product it all up (or sum it up, if you are taking log)*/
              sumofTermWeightsSpam=sumofTermWeightsSpam + log(mySpamWeightage)
            }
            else {
              // println("this word doesnt have spam weightage:"+indivWord)
            }


            //do the same for non spam class
            if (nonSpamWeightage.contains(indivWord)) {
              var mynonSpamWeightage = nonSpamWeightage(indivWord)

              /*product it all up (or sum it up, if you are taking log)*/
              sumofTermWeightsNonSpam=sumofTermWeightsNonSpam + log(mynonSpamWeightage)
            }
            else {
              // println("this word doesnt have non-spam weightage:"+indivWord)
            }


          }
        }


        //calculate cmap score for both classes
        var CmapSpam= scala.math.log10(SpamPrior)+sumofTermWeightsSpam
        var CmapNonSpam= scala.math.log10(nonSpamPrior )+sumofTermWeightsNonSpam





        var predLabel="spam"
        if(CmapNonSpam>CmapSpam)
        {
          predLabel="nonspam"
          appendToFile("found that CmapNonSpam is  > CmapSpam",fileLogFile ,outputDirectoryPath)
        }



        //code to debug. take it outside if loop later.
        if( goldLabel=="nonspam") {
          appendToFile("\n\nfilename:" + indivFileName.getName() + " goldLabel:" + goldLabel + " predLabel:" + predLabel + " CmapSpam:" + CmapSpam + " CmapNonSpam:" + CmapNonSpam, fileLogFile, outputDirectoryPath)
        }

        //add the document id and its labels
        var objGoldPred = new goldPredictedLabel(indivFileName.getName(),goldLabel, predLabel)
        listOfGoldPredictedLabel+=objGoldPred


      }

    }

   // println(listOfGoldPredictedLabel.mkString("\n"));

  }

  def appendToFile(stringToWrite: String, outputFilename: String, outputDirectoryPath: String): Unit = {

    val outFile = new File(outputDirectoryPath, outputFilename)
    val bw = new BufferedWriter(new FileWriter(outFile, true))
    bw.write(stringToWrite)
    bw.close()
  }


}