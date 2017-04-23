
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



    var listGoldPredictedLabel = new ListBuffer[goldPredictedLabel]()


    processTestingData( spamWeightage,nonSpamWeightage , SpamPrior,NonSpamPrior,listGoldPredictedLabel)

    calculateF1Score(listGoldPredictedLabel)



  }

  def calculateF1Score(listGoldPredictedLabel : ListBuffer[goldPredictedLabel]): Unit= {


    var TP:Double=0;
    var FP:Double=0;
    var TN:Double=0;
    var FN:Double=0;
    var accuracyNr:Double=0

    //go through the list and calculate TP,FP etc
    for(indivLabels<-listGoldPredictedLabel)
      {

        //every time the labels match, accuracy increases

        if(indivLabels.goldLabel==indivLabels.predictedLabel)
          {

            accuracyNr=accuracyNr+1
          }

        //if gold label is spam and predicted label is spam, increase TP
        if(indivLabels.goldLabel=="spam" && indivLabels.predictedLabel=="spam")
          {
            TP=TP+1;
          }

//        //if gold label is not-spam and predicted label is spam, increase FP
//        if(indivLabels.goldLabel=="non-spam" && indivLabels.predictedLabel=="spam")
//        {
//          FP=FP+1;
//        }
        //if gold label is spam and predicted label is nonspam, increase FN
        if(indivLabels.goldLabel=="spam" && indivLabels.predictedLabel=="non-spam")
        {
          FN=FN+1;
        }
        //if gold label is nonspam and predicted label is nonspam, increase TP
        //update: qn says ignore non-spam
//        if(indivLabels.goldLabel=="non-spam" && indivLabels.predictedLabel=="non-spam")
//        {
//          TN=TN+1;
//        }

      }

    var accuracy:Double=accuracyNr/listGoldPredictedLabel.size
    println("\naccuracy:"+accuracy)

    println("\nTP:"+TP)
    println("FP:"+FP)
    println("FN:"+FN)
    println("TN:"+TN)

    var precision:Double = TP/(TP+FP)

    var recall:Double = TP/(TP+FN)

    println("\nprecision:"+precision)
    println("recall:"+recall)

    var F1score:Double=2*precision*recall/(precision+recall)

    println("F1score:"+F1score)

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
            //if the value doesnt exist in spam map, assign it value of 1
            spamFrequency = spamFrequency + 1
          }



        // divide it by (total spam term frequency+ total number of tokens- i.e length of listOfAllTrTokens)
        var spamWeightageOfThisToken=spamFrequency/(totalUniqTokenCount+totalSpamTokenFrequency)

//        //used for debugging
//        if(alltokens=="linda")
//        {
//          println()
//          println("linda, "+"\tspamFrequency:"+spamFrequency+"\ttotalUniqTokenCount:"+totalUniqTokenCount+"\ttotalSpamTokenFrequency"+totalSpamTokenFrequency+"\tspamWeightageOfThisToken:"+spamWeightageOfThisToken)
//        }

        //just to check if scaling the values makes a difference.
        spamWeightageOfThisToken=spamWeightageOfThisToken*100000000
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

//        if(alltokens=="linda")
//        {
//
//          println("linda, "+"\tnonSpamFrequency:"+nonSpamFrequency+"\ttotalUniqTokenCount:"+totalUniqTokenCount+"\ttotalNonSpamTokenFrequency"+totalNonSpamTokenFrequency+"\tnonspamWeightageOfThisToken:"+nonspamWeightageOfThisToken)
//          println()
//        }


        //var localnonspamWeightageOfThisToken:Double=nonspamWeightageOfThisToken
        nonspamWeightageOfThisToken=nonspamWeightageOfThisToken*100000000

        //add it to non spam weightage Map
        nonSpamWeightage += (alltokens -> nonspamWeightageOfThisToken)



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

        if(indivFileName.getName()=="spmsgb90.txt") {
          //appendToFile("\n\nfilename:" + indivFileName.getName() , fileLogFile, outputDirectoryPath)
        }
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
              if(indivFileName.getName()=="spmsgb90.txt") {
               // appendToFile("\n word :" + indivWord + " mySpamWeightage:" + mySpamWeightage + " log(mySpamWeightage):" + log(mySpamWeightage) + " sumofTermWeightsSpam:" + sumofTermWeightsSpam, fileLogFile, outputDirectoryPath)
              }
            }
            else {
              // println("this word doesnt have spam weightage:"+indivWord)
             // appendToFile("\n word :" + indivWord + " doesnt have spam weightage" , fileLogFile, outputDirectoryPath)
            }


            //do the same for non spam class
            if (nonSpamWeightage.contains(indivWord)) {
              var mynonSpamWeightage = nonSpamWeightage(indivWord)

              /*product it all up (or sum it up, if you are taking log)*/
              sumofTermWeightsNonSpam=sumofTermWeightsNonSpam + log(mynonSpamWeightage)
              if(indivFileName.getName()=="spmsgb90.txt") {
             //    appendToFile("\n word :" + indivWord + " mynonSpamWeightage:" + mynonSpamWeightage +" log(mynonSpamWeightage):"+log(mynonSpamWeightage)+ " sumofTermWeightsNonSpam:" + sumofTermWeightsNonSpam, fileLogFile, outputDirectoryPath)
              }

            }
            else {
           //   appendToFile("\n word :" + indivWord + " doesnt have non spam weightage" , fileLogFile, outputDirectoryPath)
            }



          }

        }


        //calculate cmap score for both classes
        var CmapSpam= scala.math.log10(SpamPrior)+sumofTermWeightsSpam
        var CmapNonSpam= scala.math.log10(nonSpamPrior )+sumofTermWeightsNonSpam





        var predLabel="spam"
        if(CmapNonSpam>CmapSpam)
        {
          predLabel="non-spam"
          appendToFile("\nfound that CmapNonSpam is  > CmapSpam",fileLogFile ,outputDirectoryPath)
        }



        //code to debug. take it outside if loop later.
        if( goldLabel=="non-spam") {
          appendToFile("\n\nfilename:" + indivFileName.getName() + "\tgoldLabel:" + goldLabel + "\tpredLabel:" + predLabel + "\tCmapSpam:" + CmapSpam + "\tCmapNonSpam:" + CmapNonSpam, fileLogFile, outputDirectoryPath)
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