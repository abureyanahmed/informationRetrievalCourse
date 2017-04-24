import scala.collection.mutable.ListBuffer
import scala.util.matching.Regex
import java.io.{File, FileNotFoundException, InputStream}
import java.util
import initializer._
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

  var dictionaryForInvertedIndex: Map[String, ListBuffer[documentIDPositions]] = Map();

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
        println("value of the path to the file is" + pathToInputFile)

        for (line <- io.Source.fromFile(pathToInputFile).getLines()) {


          // println("getting here at 1");
          val content = line.split("\\s+");
          // println("getting here at 2");
          var termCounter = 0;
          //  println("getting here at 3");


          if (content.length > 1) {
            val content = line.split("\\s+");
            //this counter is for actualtoken in sentences only- i.e we are ignoring the words doc and 1
            var positionOfTheTerm = 1;
            var docid = content(1).toInt;
            var noOfTokensDenotingDocId = 1;
            // println("getting here at 4");
            //there is confusion if the first word is going to be doc1 or doc space 1- writing code for both separated by a boolean flag
//            if (initializer.useDoc1) {
//              noOfTokensDenotingDocId = noOfTokensDenotingDocId + 1
//              println(content.mkString(" "))
//              //in hw2 input, there is no space between doc and 1.
//              //split it based on number
//              //create a regex for the number 1
//              val stringToSplit = "doc1dock"
//              val NumberOne = "1".r();
//              println(content(0))
//              //println(content(1))
//              //var firstword = content(0).split("\\d")
//              //var firstword = content(0).split(NumberOne).map(_.trim)
//              var firstword = stringToSplit.split("1")
//              println("length of firstword is" + firstword.length)
//              println(firstword(1))
//              docid = firstword(1).toInt;
//              println(docid)
//              //  println("getting here at 5");
//              //  println("getting here at 6");
//            }
//            //for each term in the sentence
            for (individualToken <- content) {
              //ignore the first two individualToken since it contains only "doc 1"
              if (termCounter <= noOfTokensDenotingDocId) {
                termCounter = termCounter + 1;
              }

              else {
                //for each of the term you are seeing, get its position and add it to the postings list data structure
                //i am calling this the inner data structure.
                val positions = new ListBuffer[(Int)]
                positions.append(positionOfTheTerm);
                positionOfTheTerm = positionOfTheTerm + 1;

                //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back
                if (dictionaryForInvertedIndex.contains(individualToken)) {

                  var existingPostings = dictionaryForInvertedIndex(individualToken);
                  val objdocumentIDPositions = documentIDPositions(docid, positions)
                  existingPostings.append(objdocumentIDPositions)
                  dictionaryForInvertedIndex += (individualToken -> existingPostings);
                }
                else {
                  val objdocumentIDPositions = documentIDPositions(docid, positions)
                  val postingsList = ListBuffer[documentIDPositions]();
                  postingsList.append(objdocumentIDPositions)
                  dictionaryForInvertedIndex += (individualToken -> postingsList);

                }
              }
            }
          }

        }
      }


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

