package booleansearch
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

case class documentIDPositions (var docId:Int, var positions: ListBuffer[Int]);

object  Utilities {

  val resourcesDirectory = "./src/main/resources/"
  val inputFileForInvIndex = "inputfile.txt";

  var dictionaryForInvertedIndex: Map[String, ListBuffer[documentIDPositions]] = Map();
  //var term1 = "";
  var operator = "";
  //var term2 = "";

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

        //for (line <- io.Source.fromFile(pathToInputFile).getLines()) {
        for (line <- Source.fromResource(inputFileForInvIndex).getLines()) {


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
            if (initializer.useDoc1) {
              noOfTokensDenotingDocId = noOfTokensDenotingDocId + 1
              println(content.mkString(" "))
              //in hw2 input, there is no space between doc and 1.
              //split it based on number
              //create a regex for the number 1
              val stringToSplit = "doc1dock"
              val NumberOne = "1".r();
              println(content(0))
              //println(content(1))
              //var firstword = content(0).split("\\d")
              //var firstword = content(0).split(NumberOne).map(_.trim)
              var firstword = stringToSplit.split("1")
              println("length of firstword is" + firstword.length)
              println(firstword(1))
              docid = firstword(1).toInt;
              println(docid)
            //  println("getting here at 5");
            //  println("getting here at 6");
            }
            //for each term in the sentence
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

      printDictionaryPostings(dictionaryForInvertedIndex)


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

  def printDictionaryPostings(dictionaryPostings: Map[String, ListBuffer[documentIDPositions]]): Unit = {

    println("going to print postings list:")
    for ((k, v) <- dictionaryPostings) {
      print(k + "->")
      for ((postingsList) <- v) {
        val documentId = postingsList.docId
        print(documentId + ":")
        //print each of the positions in this document
        for (positions <- postingsList.positions) {
          //print in this format: Gates: 1: 〈3〉; 2: 〈6〉; 3: 〈2,17〉; 4: 〈1〉;
          print(",<" + positions + ">")
        }
        print(";")
      }
      println("");


    }

  }


  case class TermNotFoundException(excptn: String) extends Exception

  def parseTheQueryForNonDirectionalProximitySearch(term1Passed: String, term2Passed: String, proximityIndicator: Int): ListBuffer[Int] = {
    var returnList = ListBuffer[Int]()

//    println("term1="+term1Passed)
//    println("term2="+term2Passed)
    try {
      returnList = checkTermsExist(term1Passed, term2Passed, proximityIndicator)

    }

    catch {
      case ex: TermNotFoundException => println(ex.excptn)
    }
    return returnList
  }

  //
  //
  //    def parseTheQuery(userQuery: String): ListBuffer[Int] = {
  //      var returnList = ListBuffer[Int]()
  //      try {
  //        operator match {
  //          case "AND" => {
  //            returnList = checkTermsExist(term1, term2, operator)
  //          }
  //          case "OR" =>
  //          {
  //            // returnList = matchBooleanORQuery(term1, term2, operator)
  //          }
  //          case _ => print("invalid operator.")
  //        }
  //      }
  //      catch{
  //        case ex: TermNotFoundException => println("The terms you entered for query doesn't exist in the given postings list. Try again.")
  //      }
  //      return returnList
  //    }

  //  def conjunctionGivenListAndTerm(term1: String, term2Postings: ListBuffer[Int]): ListBuffer[Int] = {
  //    var conjList = new ListBuffer[Int]()
  //    var term1Postings = new ListBuffer[Int]()
  //    //var term2Postings = new ListBuffer[Int]()
  //    if (dictionaryForInvertedIndex.contains(term1)) {
  //      //if the term is already present in the dictionary, retreive its postings list
  //      term1Postings = dictionaryForInvertedIndex(term1);
  //    }
  //    else {
  //      throw new TermNotFoundException("Given term not found in the list.")
  //    }
  //
  //    conjList = conjunction(term1Postings, term2Postings)
  //    return conjList;
  //
  //  }
  //
  def checkTermsExist(term1: String, term2: String, proximityIndicator: Int): ListBuffer[Int] = {
//    println("getting into checkTermsExist");
//    println("term1="+term1)
//    println("term2="+term2)
    var conjList = new ListBuffer[Int]()

    var term1Postings = new ListBuffer[documentIDPositions]();
    var term2Postings = new ListBuffer[documentIDPositions]();

    //
    if (dictionaryForInvertedIndex.contains(term1)) {
      //if the term is already present in the dictionary, retreive its postings list
      term1Postings = dictionaryForInvertedIndex(term1);
    }
    else {
      throw new TermNotFoundException("Given term not found in the list.")
    }
    if (dictionaryForInvertedIndex.contains(term2)) {
      //if the term is already present in the dictionary, retreive its postings list
      term2Postings = dictionaryForInvertedIndex(term2);
    }
    else {
      throw new TermNotFoundException("Given term not found in the list.")
    }

    if(initializer.checkDirectionalProximity==true)
      {
        println("initializer.checkDirectionalProximity ==true . going to get into checkProximityForDirectional");

        conjList = checkProximityForDirectional(term1, term2, term1Postings, term2Postings, proximityIndicator)
      }
    else {
      println("initializer.checkDirectionalProximity ==false . going to get into checkProximityForNonDirectional");

      conjList = checkProximityForNonDirectional(term1, term2, term1Postings, term2Postings, proximityIndicator)
    }
    return conjList;

  }

  //a function to check if both the terms even exist in the same document. Else exit to square one.
  def checkProximityForNonDirectional(term1:String, term2:String, postingsOfTerm1: ListBuffer[documentIDPositions], postingsOfTerm2: ListBuffer[documentIDPositions], proximityIndicator: Int): ListBuffer[Int] = {

    println("inside checkProximityForNonDirectional")
    var flagDocIdMatch = false;
    for (objdocumentIDPositions1 <- postingsOfTerm1) {
      val documentId1 = objdocumentIDPositions1.docId
      var positionsList1 = ListBuffer[Int]();
      positionsList1=objdocumentIDPositions1.positions;
      //the values here will be the list of objdocumentIDPositions



      for (objdocumentIDPositions2 <- postingsOfTerm2) {
        val documentId2 = objdocumentIDPositions2.docId

        var positionsList2 = ListBuffer[Int]();
        positionsList2=objdocumentIDPositions2.positions;

        //if you find the corresponding doc id in the list of term2, proceed, else your job is done, just exit.
        if (documentId1 == documentId2) {

          for (positions1 <- positionsList1) {
            for (positions2 <- positionsList2) {

              //find which one is bigger- i cant find a nicer way of doing mod operator. There is %, but its an overkill
              if(positions2>positions1) {

               // println("found that positions2 is bigger than positions1")
                if ((positions2 -positions1) == proximityIndicator) {
                  println("Found that the two terms that you asked viz., \""+term1+"\" and \""+term2 +"\" exist in the proximity of: " + proximityIndicator+" in the document with Document Id: "+documentId1)
                  flagDocIdMatch = true;
                }

              }
              else
              if(positions2 < positions1)
                {
                  if ((positions1-positions2) == proximityIndicator) {
                    println("Found that the two terms that you asked viz., \""+term1+"\" and \""+term2 +"\" exist in the proximity of: " + proximityIndicator+" in the document with Document Id: "+documentId1)
                    flagDocIdMatch = true;
                  }
                }
              else
                {throw new TermNotFoundException("They are both at the same position. Error")}

            }
          }
        }
      }

    }
    if (flagDocIdMatch == false) {
      throw new TermNotFoundException("Given terms viz., \""+term1+"\" and \""+term2 +"\" don't exist in the same document, atleast not in the proximity you asked for.")
    }



    //        //print each of the positions in this document
    //        for (positions <- objdocumentIDPositions.positions) {
    //          //print in this format: Gates: 1: 〈3〉; 2: 〈6〉; 3: 〈2,17〉; 4: 〈1〉;
    //          print(",<" + positions + ">")
    //        }
    //print(";")
    val conjunctedList = new ListBuffer[Int]();
    return conjunctedList


  }


  def checkProximityForDirectional(term1:String, term2:String, postingsOfTerm1: ListBuffer[documentIDPositions], postingsOfTerm2: ListBuffer[documentIDPositions], proximityIndicator: Int): ListBuffer[Int] = {

   // println("inside checkProximityForDirectional")

    //val objdocumentIDPositions = new documentIDPositions(Int, ListBuffer[Int]);
    //var term2Postings = new ListBuffer[documentIDPositions]();
    var flagDocIdMatch = false;
    for (objdocumentIDPositions1 <- postingsOfTerm1) {
      val documentId1 = objdocumentIDPositions1.docId
      var positionsList1 = ListBuffer[Int]();
      positionsList1=objdocumentIDPositions1.positions;
      //the values here will be the list of objdocumentIDPositions

      //
      //          postingsList.append(objdocumentIDPositions)
      //          dictionaryForInvertedIndex += (individualToken -> postingsList);

      // println("current document id for term 1 is:" + documentId1)

      for (objdocumentIDPositions2 <- postingsOfTerm2) {
        val documentId2 = objdocumentIDPositions2.docId

        var positionsList2 = ListBuffer[Int]();
        positionsList2 = objdocumentIDPositions2.positions;
        //println("current document id for term 2 is:" + documentId2)

        //if you find the corresponding doc id in the list of term2, proceed, else your job is done, just exit.
        if (documentId1 == documentId2) {

          //println("found that these two terms exist in the same document which is document number:" + documentId2)
          // println("going to start proximity search.")
          for (positions1 <- positionsList1) {
            for (positions2 <- positionsList2) {

              //println("term 1 "+term1+" is at position:" + positions1)
              // println("term 2 "+term2+" is at position:" + positions2)
              // println("value of proximityIndicator is:" + proximityIndicator)

              //in case of directional search,
              //if position of term1 (i.e the first term the user entered on teh left side of /2) is greater than position of term2, throw error.
              if (positions1 > positions2) {
                {
                  throw new TermNotFoundException("In a directional query you cant have the second position lesser than the first position.")
                }
              }


              //find which one is bigger- i cant find a nicer way of doing mod operator. There is %, but its an overkill
              if (positions2 > positions1) {

                // println("found that positions2 is bigger than positions1")
                if ((positions2 - positions1) == proximityIndicator) {
                  println("Found that the two terms that you asked viz., \"" + term1 + "\" and \"" + term2 + "\" exist in the proximity of: " + proximityIndicator + " in the document with Document Id: " + documentId1)
                  flagDocIdMatch = true;
                }

              }
              //              else
              //              if(positions2 < positions1)
              //              {
              //                // println("found that positions1 is bigger than positions2")
              //
              //                //if they have asked for directional query, position 2 has to be bigger than position 1
              //                if(initializer.checkDirectionalProximity==true)
              //                {
              //
              //                }
              //
              //
              //                if ((positions1-positions2) == proximityIndicator) {
              //                  println("Found that the two terms that you asked viz., \""+term1+"\" and \""+term2 +"\" exist in the proximity of: " + proximityIndicator+" in the document with Document Id: "+documentId1)
              //                  flagDocIdMatch = true;
              //                }
              //              }
              else {
                throw new TermNotFoundException("They are both at the same position. Error")
              }

            }
          }
        }
      }

    }
    if (flagDocIdMatch == false) {
      throw new TermNotFoundException("Given terms viz., \""+term1+"\" and \""+term2 +"\" don't exist in the same document, atleast not in the proximity you asked for.")
    }



    //        //print each of the positions in this document
    //        for (positions <- objdocumentIDPositions.positions) {
    //          //print in this format: Gates: 1: 〈3〉; 2: 〈6〉; 3: 〈2,17〉; 4: 〈1〉;
    //          print(",<" + positions + ">")
    //        }
    //print(";")
    val conjunctedList = new ListBuffer[Int]();
    return conjunctedList


  }



  def conjunction(postingsOfTerm1: ListBuffer[Int], postingsOfTerm2: ListBuffer[Int]): ListBuffer[Int] = {
    val conjunctedList = new ListBuffer[Int]();
    var childListCounter = 0
    var parentListCounter = 0
    var parentlist = new ListBuffer[Int]();
    var childlist = new ListBuffer[Int]();
    if (postingsOfTerm1.length > postingsOfTerm2.length) {
      parentlist = postingsOfTerm1
      childlist = postingsOfTerm2
    }
    else {
      parentlist = postingsOfTerm2
      childlist = postingsOfTerm1
    }
    while (parentListCounter < parentlist.length && childListCounter < childlist.length) {
      if (childlist(childListCounter) == parentlist(parentListCounter)) {
        conjunctedList += (childlist(childListCounter))
        childListCounter = childListCounter + 1
        parentListCounter = parentListCounter + 1
      }
      else {
        if (childlist(childListCounter) < parentlist(parentListCounter)) {
          childListCounter = childListCounter + 1
        }
        else {
          parentListCounter = parentListCounter + 1
        }
      }
    }
    return conjunctedList

  }

  //
  //
  //  def disjunction(postingsOfTerm1: ListBuffer[Int], postingsOfTerm2: ListBuffer[Int]): ListBuffer[Int] = {
  //    val disjList = new ListBuffer[Int]();
  //    var childListCounter = 0
  //    var parentListCounter = 0
  //    var parentlist = new ListBuffer[Int]();
  //    var childlist = new ListBuffer[Int]();
  //    if (postingsOfTerm1.length > postingsOfTerm2.length) {
  //      parentlist = postingsOfTerm1
  //      childlist = postingsOfTerm2
  //    }
  //    else {
  //      parentlist = postingsOfTerm2
  //      childlist = postingsOfTerm1
  //    }
  //    while (parentListCounter < parentlist.length && childListCounter < childlist.length) {
  //      if (childlist(childListCounter) == parentlist(parentListCounter)) {
  //        disjList += (childlist(childListCounter))
  //        childListCounter = childListCounter + 1
  //        parentListCounter = parentListCounter + 1
  //      }
  //      else {
  //        if (childlist(childListCounter) < parentlist(parentListCounter)) {
  //          disjList += (childlist(childListCounter))
  //          childListCounter = childListCounter + 1
  //        }
  //        else {
  //          disjList += (parentlist(parentListCounter))
  //          parentListCounter = parentListCounter + 1
  //        }
  //      }
  //    }
  //
  //    //once we break out of the loop- which means the smaller list has finished, now write out the left over in parent list
  //    while (parentListCounter < parentlist.length) {
  //      disjList += parentlist(parentListCounter)
  //      parentListCounter = parentListCounter + 1
  //    }
  //    return disjList
  //
  //  }


  def verifyInputQueryStringForNonDirectional(userQuery: String): Boolean = {
    println("verifying user input...")
    val queryContent = userQuery.split("\\s+");
    var flag = false;
    if (queryContent.length > 2) {
      //if the query has 3 words
     val term1 = queryContent(0);
      operator = queryContent(1);
      val term2 = queryContent(2);
      println("term1="+term1)
      println("term2="+term2)
      //a regular expression to check if the query has a slash followed by an integer
      val regexForSlashInt = new Regex("/[0-9]");
      println((regexForSlashInt.findAllIn(operator)).mkString(","))
      sys.exit(1);
      //        if (operator.matches(regexForSlashInt) {
      //          println("yep,. Input query looks ok.")
      //          flag = true;
      //        }
      //        else {
      //          flag = false;
      //        }
    }
    else {
      flag = false;
    }
    return flag;
  }
}