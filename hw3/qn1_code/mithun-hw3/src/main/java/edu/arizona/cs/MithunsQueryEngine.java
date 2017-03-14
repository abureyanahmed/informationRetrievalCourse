package edu.arizona.cs;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;


public class MithunsQueryEngine {
    public static void main(String[] args) {

        try {
            System.out.println("********Welcome to  Homework 3!");

            StandardAnalyzer analyzer = new StandardAnalyzer();
            Directory index = new RAMDirectory();

            IndexWriterConfig config = new IndexWriterConfig(analyzer);

            IndexWriter w = new IndexWriter(index, config);
            addDoc(w, "information retrieval is the most awesome class I ever took.","Document #1");
            addDoc(w, "the retrieval of private information from your emails is a job that the NSA loves.","Document #2");
            addDoc(w, "at university of arizona you learn about data science.","Document #3");
            addDoc(w, "the labrador retriever is a great dog.","Document #4");
            w.close();




            //String querystr = "title:information AND title:dog";

            //args.length > 0 ? args[0] : "lucene";


            //String querystr = "title:information OR title:retrieval";Score:1.1655893
            //String querystr = "information AND retrieval";

            //Score:1.1655893
            //String querystr = "title:information AND title:retrieval"; //Score:1.1655893
            //String querystr = "title:awesome OR title:retrieval";
            /*1. Document #1	Score:1.595089
2. Document #2	Score:0.58279467
*/

            /*String querystr = "title:retrieval   -title:awesome";
            For Qn 1.1 found 1 hits for your query:title:retrieval   -title:awesome
1. Document #2	Score:0.58279467
*/

            //String querystr = "title:information -title:retrieval";
            /*String querystr = "title:information AND -title:retrieval";
            For Qn 1.1 found 0 hits for your query:title:information AND -title:retrieval
                    */
            String querystr="";
            //for proximity queries we wanted the syntax with double quotes
            //Eg:"retriever dog"~3


            //if the length of arguments is less than or equal to 3, we assume simple boolean query.

            if(args.length>3) {
                querystr = querystr+"\"";
                //else assume proximity query
                for (int i = 0; i < args.length; i++) {
                    System.out.println(args[i]);
                    //querystr=querystr+args[i];

                    try {
                        int op1 = Integer.parseInt(args[i]);
                        String newquerystr = querystr.trim();
                        querystr = newquerystr;
                        querystr = querystr + "\"";
                        querystr = querystr + "~" + op1;
                    } catch (NumberFormatException e) {
                        System.out.println("Wrong number");
                        querystr = querystr + args[i];
                        querystr = querystr + " ";
                    }


                }
            }
            else
            {
                for (int i = 0; i < args.length; i++) {
                    querystr = querystr + args[i];
                    querystr = querystr + " ";
                }



            }


//            querystr=querystr+"information retrieval";
//            querystr = querystr+"\"";
//            querystr = querystr+"~1";

            System.out.println("the query string is:"+querystr);
            Query myQuery= new QueryParser("title", analyzer).parse(querystr);


            IndexReader reader = DirectoryReader.open(index);
            IndexSearcher searcher = new IndexSearcher(reader);

            ScoreDoc[] hits = searchEngine(searcher, myQuery);
            displayResults(searcher, hits,querystr);
        }
        catch (IOException ex)
        {
            System.out.println(ex.getMessage());
        }
        catch (ParseException ex) {
            System.out.println(ex.getMessage());
        }
    }

    private static void addDoc(IndexWriter w, String title, String docId) throws IOException {
        Document doc = new Document();
        doc.add(new TextField("title", title, Field.Store.YES));
        doc.add(new StringField("docid", docId, Field.Store.YES));
        w.addDocument(doc);
    }

    private static ScoreDoc[] searchEngine( IndexSearcher searcher, Query myQuery) {
        int hitsPerPage = 10;
        ScoreDoc[] hits= new ScoreDoc[99999];

        try {
            TopDocs docs = searcher.search(myQuery, hitsPerPage);
            hits = docs.scoreDocs;

        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
        return hits;
    }

    private static void displayResults( IndexSearcher searcher,ScoreDoc[] hits, String querystr) {

        try {
            System.out.println("Found " + hits.length + " hits for your query:"+querystr);
            for (int i = 0; i < hits.length; ++i) {
                int docId = hits[i].doc;
                Document d = searcher.doc(docId);
                float docScore = hits[i].score ;
                System.out.println((i + 1) + ". " + d.get("docid") + "\t" +"Score:"+docScore);
            }
        }
        catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
    }
}
