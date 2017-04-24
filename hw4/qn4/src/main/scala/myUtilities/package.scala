import org.clulab.processors.Document

import scala.collection.mutable.ListBuffer
import scala.util.matching.Regex
import java.io.{File, FileNotFoundException, InputStream}
import java.util

import initializer._
import org.clulab.agiga

import scala.collection.mutable
import scala.collection.mutable._
import scala.io.Source
import scala.util.Try
import scala.annotation.switch
import scala.util.control.NonFatal
/**
  * Created by mithunpaul on 1/25/17.
  */

/**
  * Created by mithunpaul on 4/23/17.
  */
package object myUtilities {

  val resourcesDirectory = "./src/main/resources/"
  val inputFileForInvIndex = "inputfile.txt";

  case class documentIDPositions(var docId: Int, var positions: ListBuffer[Int]);


  var listOfDocIdWordMaps = new ListBuffer[Map[String, Int]]()

  var operator = "";


  def readFromFile() = {
    try {





      var noofFiles = 0

      val inputDirectoryToList = new File(resourcesDirectory)
      if (inputDirectoryToList != None) {
        noofFiles = inputDirectoryToList.listFiles().length
      }
      else {
        println("input directory is empty")
      }
      if (noofFiles == 0) {
        //todo: throw an error here
        println("no files in the input directory")
      }
      else {
        println(" no of files found in input directory is:" + noofFiles + ":Going to parallelize")
        val listOfFiles = new File(resourcesDirectory).listFiles()
        val pathToInputFile = resourcesDirectory + inputFileForInvIndex;

//        for (indivFileName <- listOfFiles) {
//
//
//          println("value of the path to the file is" + pathToInputFile)
//
//          val doc = agiga.toDocuments(indivFileName.getAbsolutePath)
//
//          for (newsArticles <- doc) {
//
//            println(newsArticles)
//
//          }
//        }

        for (line <- io.Source.fromFile(pathToInputFile).getLines()) {

          //create a map for each document
          var wordFreq: Map[String, Int ] = Map();


          // println("getting here at 1");
          val content = line.split("\\s+");
          // println("getting here at 2");
          var termCounter = 0;
          //  println("getting here at 3");


          if (content.length > 1) {
            val content = line.split("\\s+");
            //this counter is for actualtoken in sentences only- i.e we are ignoring the words doc and 1
            var positionOfTheTerm = 1;
            var docidCombined = content(1).split("#")

           var strippedValue = content(1).stripSuffix(":").trim
             strippedValue = strippedValue.stripPrefix("#").trim

            var docid=strippedValue.toInt;

            var noOfTokensDenotingDocId = 1;

//            //for each term in the sentence
            for (individualToken <- content) {
              //ignore the first two individualToken since it contains only "doc 1"
              if (termCounter <= noOfTokensDenotingDocId) {
                termCounter = termCounter + 1;
              }

              else {
                //for each of the term you are seeing, get its position and add it to the postings list data structure
                //i am calling this the inner data structure.
//                val positions = new ListBuffer[(Int)]
//                positions.append(positionOfTheTerm);
//                positionOfTheTerm = positionOfTheTerm + 1;


                //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back
                if (wordFreq.contains(individualToken)) {

                  var existingFrequency = wordFreq(individualToken);
                  existingFrequency=existingFrequency+1


                  wordFreq += (individualToken -> existingFrequency);
                }
                else {

                  wordFreq += (individualToken -> 1);

                }
              }
            }
          }


          listOfDocIdWordMaps.append(wordFreq)
        }


      }

      println(listOfDocIdWordMaps.mkString("\n"))


    } catch {
      case NonFatal(t) => {
        println(NonFatal.toString())
      }

      case ex: Exception => {
        println("An exception happened. Not able to find the file. Full stack trace is being printed as below")
        println(ex.toString())

      }
      case _: Throwable => {
        println("throwable exception found\n")
      }
        throw new FileNotFoundException(inputFileForInvIndex)
    }

  }
}

