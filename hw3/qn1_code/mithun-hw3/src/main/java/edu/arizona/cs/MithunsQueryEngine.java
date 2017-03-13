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
            System.out.println("Welcome to  Homework 3!");

            StandardAnalyzer analyzer = new StandardAnalyzer();
            Directory index = new RAMDirectory();

            IndexWriterConfig config = new IndexWriterConfig(analyzer);

            IndexWriter w = new IndexWriter(index, config);
            addDoc(w, "information retrieval is the most awesome class I ever took.");
            addDoc(w, "the retrieval of private information from your emails is a job that the NSA loves.");
            addDoc(w, "at university of arizona you learn about data science.");
            addDoc(w, "the labrador retriever is a great dog.");
            w.close();

           // Query myQuery = readQuery(args, analyzer);
           // Query myQuery = readQuery(args, analyzer);

            String querystr = args.length > 0 ? args[0] : "lucene";
            Query myQuery= new QueryParser("title", analyzer).parse(querystr);


            IndexReader reader = DirectoryReader.open(index);
            IndexSearcher searcher = new IndexSearcher(reader);

            ScoreDoc[] hits = searchEngine(searcher, myQuery);
            displayResults(searcher, hits);
        }
        catch (IOException ex)
        {
            System.out.println(ex.getMessage());
        }
        catch (ParseException ex) {
            System.out.println(ex.getMessage());
        }
    }

    private static void addDoc(IndexWriter w, String title) throws IOException {
        Document doc = new Document();
        doc.add(new TextField("title", title, Field.Store.YES));
        //doc.add(new StringField("isbn", isbn, Field.Store.YES));
        w.addDocument(doc);
    }

//    private static Query readQuery(String[] args, StandardAnalyzer analyzer) {
//
//        QueryParser qprsr=
//        Query q= new Query();
//        try {
//
//
//       }
//       catch (ParseException ex) {
//           System.out.println(ex.getMessage());
//       }
//
//        return q;
//    }

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

    private static void displayResults( IndexSearcher searcher,ScoreDoc[] hits) {

        try {
            System.out.println("Found " + hits.length + " hits.");
            for (int i = 0; i < hits.length; ++i) {
                int docId = hits[i].doc;
                Document d = searcher.doc(docId);
                System.out.println((i + 1) + ". " + d.get("isbn") + "\t" + d.get("title"));
            }
        }
        catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
    }
}
