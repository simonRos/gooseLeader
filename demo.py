import gooseLeader
from gooseLeader import gooseLeader

demoSearch = gooseLeader()

demoSearch.userHTMLReport(demoSearch.getInfluUsers(25,demoSearch.search("trump", 10000, "en", "mixed")),"demo")
