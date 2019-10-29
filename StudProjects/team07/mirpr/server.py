import os
from nltk.parse.corenlp import CoreNLPServer

stanford = os.path.join("stanford-corenlp")

server = CoreNLPServer(
   os.path.join(stanford, "/home/mek/stanford-corenlp/stanford-corenlp-3.9.2.jar"),
   os.path.join(stanford, "/home/mek/stanford-corenlp/stanford-corenlp-3.9.2-models.jar")
)

server.start()
