from sqlitedict import SqliteDict
import numpy as np

linksDB = SqliteDict('phase2-links.sqlite', autocommit=True)
metadataDB = SqliteDict('phase2-metadata.sqlite', autocommit=True)

d = 0.1
pageRanks = {}
pageRanksTemp = {}
for page, metadata in metadataDB.items():
    pageRanks[page] = 1
    pageRanksTemp[page] = 1

numberIterations = 3
for iteration in range(numberIterations):
    for page, metadata in metadataDB.items():
        score = 0
        for childPage, metadata in metadataDB.items():
            if int(page) in linksDB[childPage]['out']:
                score += pageRanks[childPage] / len(linksDB[childPage]['out'])
        pageRanksTemp[page] = d + (1-d) * score
    pageRanks = pageRanksTemp

for pageID, rank in pageRanks.items():
    data = metadataDB[pageID]
    index = len(data)
    np.insert(data, index, rank)
