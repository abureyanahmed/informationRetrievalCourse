
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

    var trainLen = mapTrTokenSpam.size
    //read spam training data
    var fullScrapedDirectoryPath = resourcesDirectory + inputDirectoryForTrainingSpam

    if (checkFolderExists(fullScrapedDirectoryPath)) {

      readSpamNSpamData(fullScrapedDirectoryPath)

    }

    println("no of lines in mapTrTokenSpam is:" + mapTrTokenSpam.size)


    //read nonspam training data
    fullScrapedDirectoryPath = resourcesDirectory + inputDirectoryForTrainingNSpam
    if (checkFolderExists(fullScrapedDirectoryPath)) {

      readSpamNSpamData(fullScrapedDirectoryPath)

    }

    println("no of lines in mapTrTokenSpam is:" + mapTrTokenSpam.size)


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

  def readSpamNSpamData(folderToReadFrom: String) = {


    val listOfFiles = new File(folderToReadFrom).listFiles()



    var fileCounter = 0;

    for (indivFileName <- listOfFiles) {

      for (lineFromInput <- Source.fromFile(indivFileName).getLines()) {
        

        val words = lineFromInput.split("\\s+")
        for (indivWord <- words) {

          if (mapTrTokenSpam.contains(indivWord)) {
            var wordCounter = mapTrTokenSpam(indivWord)
            wordCounter = wordCounter + 1
            mapTrTokenSpam.put(indivWord, wordCounter);
          }

          else {
            mapTrTokenSpam += (indivWord -> 1)
          }

        }
      }
    }


  }
}