from .board import Board
import json

class KanbanBoard(Board):
    def __init__(self, boardId, connection):
        Board.__init__(self, boardId, connection)
        
        # Populate the status sets
        boardConf = self.connection.customRequest(self.baseUrl+"/configuration")  .json()
        self.__statusToColumn = {}
        self.__columnIssues = {}
        for col in boardConf["columnConfig"]["columns"]:
            #print(json.dumps(col, sort_keys=True, indent=4))
            cName = col["name"]
            self.__columnIssues[cName] = set()
            for s in col["statuses"]:
                self.__statusToColumn[s["id"]] = cName

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=key,status&startAt=%d&maxResults=%d" % (startAt, maxResults)).json()
        # Sort issues by Category
        for i in r["issues"]:
            key = i["key"]
            statusId = i["fields"]["status"]["id"]
            self.__columnIssues[self.__statusToColumn[statusId]].add(key)

        return [( a, list(b) ) for a,b in self.__columnIssues.items() if len(b) > 0]
        
