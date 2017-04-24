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

//  case class documentIDPositions(var docId: Int, var positions: ListBuffer[Int]);



  case class docIdLMValue(var docId: Int, var score: Double);



  //to store a ranks of doc ids like 3>4>2>1
  var docIdranks = new ListBuffer[Int]()

  //var listOfDocIdWordMaps = new ListBuffer[Map[String, Int]]()

  case class docIdWordFreq(var docId: Int, var wordsAndFreq: Map[String, Int]);
  var listOfDocIdWordMaps = new ListBuffer[docIdWordFreq]()

  var lamdba:Double = 0.5;


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
        //println(" no of files found in input directory is:" + noofFiles + ":Going to parallelize")
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
          var wordFreq: Map[String, Int] = Map();

          if (line != "") {
            // println("getting here at 1");
            val content = line.split("\\s+");
            // println("getting here at 2");
            var termCounter = 0;
            //  println("getting here at 3");

            var docid = 0
            if (content.length > 1) {
              val content = line.split("\\s+");
              //this counter is for actualtoken in sentences only- i.e we are ignoring the words doc and 1
              var positionOfTheTerm = 1;
              var docidCombined = content(1).split("#")

              var strippedValue = content(1).stripSuffix(":").trim
              strippedValue = strippedValue.stripPrefix("#").trim

              docid = strippedValue.toInt;

              var noOfTokensDenotingDocId = 1;

              //            //for each term in the sentence
              for (eachWord <- content) {
                //ignore the first two individualToken since it contains only "doc 1"
                if (termCounter <= noOfTokensDenotingDocId) {
                  termCounter = termCounter + 1;
                }

                else {

                  var individualToken = eachWord.stripSuffix("\"").trim
                  individualToken = individualToken.stripSuffix(".").trim
                  individualToken = individualToken.stripPrefix("\"").trim
                  individualToken = individualToken.stripSuffix(".").trim


                  //if the term is already present in the dictionary, retreive its postings list, attach the new docid and attach it back
                  if (wordFreq.contains(individualToken)) {

                    var existingFrequency = wordFreq(individualToken);
                    existingFrequency = existingFrequency + 1


                    wordFreq += (individualToken -> existingFrequency);
                  }
                  else {

                    wordFreq += (individualToken -> 1);

                  }
                }
              }
            }



            var objdocIdWordFreq = new docIdWordFreq(docid, wordFreq)
            listOfDocIdWordMaps.append(objdocIdWordFreq)
          }
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

  def parseQueryAndCalculateScores(query:String): Unit =
  {

    var wordDocIdrank: Map[String, ListBuffer[docIdLMValue] ] = Map();

    if (query != "") {

      //split the query into words
       val content = query.split("\\s+");


      //total number of words



      //for each word find its value in each of the maps

      for(queryWord<-content)
        {
          var totalWordsInCorpus=0


          var listOfDocIdValue = new ListBuffer[docIdLMValue]()

          var totalOccurenceOfThisWordInCorpus=0
          for(indivMaps<-listOfDocIdWordMaps)
            {

              var noOfWordsInThisDocument=0

              //run throuigh this document and find total number of words it has.
              for((key,value)<- indivMaps.wordsAndFreq)
                {
                  noOfWordsInThisDocument=noOfWordsInThisDocument+value;
                }

              //go through each of the document maps, and find how many times information occurs in it, keep adding it up.


              if(indivMaps.wordsAndFreq.contains(queryWord))
                {
                  //get its value and keep summing up
                  var noOfExistence= indivMaps.wordsAndFreq(queryWord)

                  totalOccurenceOfThisWordInCorpus=totalOccurenceOfThisWordInCorpus+noOfExistence
                }


              //var objdocIdLMValue = new docIdLMValue(indivMaps.docId, )

              totalWordsInCorpus=totalWordsInCorpus+noOfWordsInThisDocument
            }

          //go through the list of maps again and do the actual lm calculation now

          for(indivMaps<-listOfDocIdWordMaps)
          {

            var noOfWordsInThisDocument=0

            //run throuigh this document and find total number of words it has.
            for((key,value)<- indivMaps.wordsAndFreq)
            {
              noOfWordsInThisDocument=noOfWordsInThisDocument+value;
            }

            //go through each of the document maps, and find how many times information occurs in it, keep adding it up.

            var termDoc:Double=0
            var dbnoOfWordsInThisDocument:Double =noOfWordsInThisDocument
            var collectionValue:Double=0

            var dbtotalOccurenceOfThisWordInCorpus:Double =totalOccurenceOfThisWordInCorpus
            var dbtotalWordsInCorpus:Double =totalWordsInCorpus

            collectionValue=dbtotalOccurenceOfThisWordInCorpus/dbtotalWordsInCorpus

            if(indivMaps.wordsAndFreq.contains(queryWord))
            {
              //get its value and keep summing up
              var noOfExistence:Double = indivMaps.wordsAndFreq(queryWord)

              //do the lamda calculation here

              var dbnoOfExistence:Double =noOfExistence



              termDoc = dbnoOfExistence/dbnoOfWordsInThisDocument





            }

            else {

              //this value doesnt exist
              var dbnoOfExistence:Double =0
              termDoc = dbnoOfExistence/dbnoOfWordsInThisDocument
            }

            var scoreOfThisDoc:Double= ( (lamdba*termDoc ) +( (1-lamdba)*collectionValue ))
            println("word:"+queryWord+"\tscoreOfThisDoc:"+scoreOfThisDoc)


            var objdocIdLMValue = new docIdLMValue(indivMaps.docId,scoreOfThisDoc )
            listOfDocIdValue.append(objdocIdLMValue)
          }

          wordDocIdrank += (queryWord -> listOfDocIdValue);

        }


      println(wordDocIdrank.mkString("\n"));
    }


    //go through this list multiply for each document. store in a new map4
    var DocIdfinalValue: Map[Int, Double] = Map();

    var finalValueForDoc1:Double=1
    var finalValueForDoc2:Double=1
    var finalValueForDoc3:Double=1
    var finalValueForDoc4:Double=1

    for((indivQueryword,listDocs)<-wordDocIdrank)
    {

      //var wordDocIdrank: Map[String, ListBuffer[docIdLMValue] ] = Map();
      //case class docIdLMValue(var docId: Int, var score: Double);
      for(eachDoc<-listDocs)
        {
          if(eachDoc.docId==1)
            {
              finalValueForDoc1=eachDoc.score *finalValueForDoc1

            }
          if(eachDoc.docId==2)
          {
            finalValueForDoc2=eachDoc.score *finalValueForDoc2

          }
          if(eachDoc.docId==3)
          {
            finalValueForDoc3=eachDoc.score *finalValueForDoc3

          }
          if(eachDoc.docId==4)
          {
            finalValueForDoc4=eachDoc.score *finalValueForDoc4

          }
        }


    }


    println()
    println("\nfinalValueForDoc1:"+finalValueForDoc1)
    println("finalValueForDoc2:"+finalValueForDoc2)
    println("finalValueForDoc3:"+finalValueForDoc3)
    println("finalValueForDoc4:"+finalValueForDoc4)

    println("\nvalues of documents ids  and Language model values for the given query are as follows. ")
    DocIdfinalValue+=(1->finalValueForDoc1)
    DocIdfinalValue+=(2->finalValueForDoc2)
    DocIdfinalValue+=(3->finalValueForDoc3)
    DocIdfinalValue+=(4->finalValueForDoc4)


    println(DocIdfinalValue.mkString("\n"))


    println("\nRanked document ids and values are as follows. Top most doc id is the most relevant for this query.")
    //sort based on the value
    val sortedHashMap =   ListMap(DocIdfinalValue.toSeq.sortBy(_._2):_*)

    println(sortedHashMap.mkString("\n"))


  }
}

