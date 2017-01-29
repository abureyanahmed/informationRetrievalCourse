package parsercombinators


/**
  * Created by mithunpaul on 1/25/17.
  */
import scala.util.parsing.combinator._


case class WordFreq(word: String, count: Int) {
  override def toString = "Word <" + word + "> " +
    "occurs with frequency " + count
}


case class parseMyQuery(term1: String, term2: String, operator1: String, operator2: String, term3: String) {
  override def toString = "query term 1 is  " + term1 + " ." +
    "query term 2 is  " + term2 +
    " and the operator is:" + operator1


  println("Going to parse this query...")
  val queryResult1 = booleansearch.Utilities.parseTheQueryGivenAll3Terms(term1, term2, operator1)

  if (queryResult1.length > 0) {
    val queryResult2 = booleansearch.Utilities.conjunctionGivenListAndTerm(term3, queryResult1)
    if (queryResult2.length > 0) {
      println("Thank You. The documents in which you can find the results for your query are document ids: " + queryResult2.mkString(","))
    }
    else {
      println("Thank You. Unfortunately, there were no documents that matched your query. Please try again with another query.")
    }
  }
  else {
    println("Thank You. Unfortunately, there were no documents that matched your query. Please try again with another query.")
  }


  println()


}

class SimpleParser extends RegexParsers {
  def lparenthesis: Parser[String]   = """[(]""".r       ^^ { _.toString }
  def rparenthesis: Parser[String]   = """[)]""".r       ^^ { _.toString }
  def word: Parser[String]   = """[a-z]+""".r       ^^ { _.toString }
  def operator: Parser[String]   = """[AND|OR]+""".r       ^^ { _.toString }
  def number: Parser[Int]    = """(0|[1-9]\d*)""".r ^^ { _.toInt }
  def freq: Parser[WordFreq] = word ~ number        ^^ { case wd ~ fr => WordFreq(wd,fr) }
  //def parWordOperator: Parser[parseMyQuery] = lparenthesis ~ word ~ operator ~ word  ~ rparenthesis      ^^ { case lpar ~ wd1 ~op ~ wd2 ~ rpar=> parseMyQuery(wd1,wd2,op) }
  def parWordOperator: Parser[parseMyQuery] = lparenthesis ~ word ~ operator ~ word  ~ rparenthesis   ~ operator ~ word   ^^ { case lpar ~ wd1 ~op1 ~ wd2 ~ rpar ~op2 ~wd3=> parseMyQuery(wd1,wd2,op1,op2,wd3) }

}
