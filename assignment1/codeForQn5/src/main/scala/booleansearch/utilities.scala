package booleansearch

import scala.io.Source;

/**
  * Created by mithunpaul on 1/25/17.
  */


val inputFile= "inputFile.txt";


object  Utilities {

  def readFromFile() = {
    try {
      var counterForHashmap = 0;
      for (line <- Source.fromResource(inputFile).getLines()) {
       println(line)
      }
    } catch {
      case ex: Exception => println("An exception happened. Not able to find the file")
    }

  }


}
