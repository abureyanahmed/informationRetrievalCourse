
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

    if (checkFolderExists(fullScrapedDirectoryPath)) {


      var mapTrTokenSpam: Map[String, Int]= Map();


      readTrainingData(fullScrapedDirectoryPath,mapTrTokenSpam)

      println("no of lines in mapTrTokenSpam is:" + mapTrTokenSpam.size)


    }




    //read nonspam training data
    val nonSpamTrainingFolder = resourcesDirectory + inputDirectoryForTrainingNSpam
    if (checkFolderExists(nonSpamTrainingFolder)) {



      var mapTrTokenNonSpam: Map[String, Int] = Map();

      readTrainingData(nonSpamTrainingFolder,mapTrTokenNonSpam)
      println("no of lines in mapTrTokenNonSpam is:" + mapTrTokenNonSpam.size)

    }




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

//  def readNonSpamTrData(folderToReadFrom: String,mapTrTokenNonSpam: Map[String, Int]) = {
//
//
//    val listOfFiles = new File(folderToReadFrom).listFiles()
//
//
//
//    var fileCounter = 0;
//
//    for (indivFileName <- listOfFiles) {
//
//      for (lineFromInput <- Source.fromFile(indivFileName).getLines()) {
//
//
//        val words = lineFromInput.split("\\s+")
//        for (wordToTrim <- words) {
//
//         var indivWord = wordToTrim.trim();
//
//          if (mapTrTokenNonSpam.contains(indivWord)) {
//            var wordCounter = mapTrTokenNonSpam(indivWord)
//            wordCounter = wordCounter + 1
//            mapTrTokenNonSpam.put(indivWord, wordCounter);
//          }
//
//          else {
//            mapTrTokenNonSpam += (indivWord -> 1)
//          }
//
//        }
//      }
//    }
//
//
//  }
}