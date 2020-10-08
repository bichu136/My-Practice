import sys
import glob
import lucene

from java.nio.file import Path, Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StoredField, StringField, TextField

from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader

from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory

class IR:
	directory = None
	analyzer = None
	indexer = None
	searcher = None
	queryparser = None
	MAX = 1000
	def __init__(self, path):
		self.directory = SimpleFSDirectory(Paths.get(path))
		self.analyzer = StandardAnalyzer()
		cf = IndexWriterConfig(self.analyzer)		
		cf.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
		self.indexer = IndexWriter(self.directory, cf)
		
	def index(self, path):
		print("Indexing " + path)
		for f in glob.glob(path + "\*.*"):
			r = open(f, "r", encoding="utf-8")
			content = r.read()
			
			doc = Document()
			noidung = TextField("noidung", content, Field.Store.YES)
			doc.add(noidung)
			self.indexer.addDocument(doc)

		self.indexer.close()
		
	def openIndex(self):
		reader = DirectoryReader.open(self.directory)
		self.searcher = IndexSearcher(reader)
		self.queryparser = QueryParser("noidung", self.analyzer)
	
	def search(self, strQry):
		query = self.queryparser.parse(strQry)
		hits = self.searcher.search(query, self.MAX)

		res = []
		for hit in hits.scoreDocs:
			doc = self.searcher.doc(hit.doc)
			res.append([doc.get("noidung"),hit.score])
		return res
		
lucene.initVM()
	


