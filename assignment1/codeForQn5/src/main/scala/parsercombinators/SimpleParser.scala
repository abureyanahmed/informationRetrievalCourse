package parsercombinators


/**
  * Created by mithunpaul on 1/25/17.
  */
import scala.util.parsing.combinator._

class SimpleParser extends RegexParsers {
  def word: Parser[String]    = """[a-z]+""".r ^^ { _.toString }
}
