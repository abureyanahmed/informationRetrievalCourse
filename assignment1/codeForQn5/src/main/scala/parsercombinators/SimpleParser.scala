package parsercombinators


/**
  * Created by mithunpaul on 1/25/17.
  */
import scala.util.parsing.combinator._

case class WordFreq(word: String, count: Int) {
  override def toString = "Word <" + word + "> " +
    "occurs with frequency " + count
}


case class parsedQuery(term1: String, term2: String,operator: String) {
  override def toString = "query term 1 is  " + term1 + " ." +
    "query term 2 is  " + term2 +
    " and the operator is:" + operator
}

class SimpleParser extends RegexParsers {
  def parenthesis: Parser[String]   = """[(]+""".r       ^^ { _.toString }
  def word: Parser[String]   = """[a-z]+""".r       ^^ { _.toString }
  def operator: Parser[String]   = """[AND|OR]+""".r       ^^ { _.toString }
  def number: Parser[Int]    = """(0|[1-9]\d*)""".r ^^ { _.toInt }
  def freq: Parser[WordFreq] = word ~ number        ^^ { case wd ~ fr => WordFreq(wd,fr) }
  def parWordOperator: Parser[parsedQuery] = parenthesis ~ word ~ operator ~word        ^^ { case par ~ wd1 ~op ~ wd2=> parsedQuery(wd1,wd2,op) }

}
