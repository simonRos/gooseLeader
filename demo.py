import gooseLeader
from gooseLeader import gooseLeader

term = "trump"
demoSearch = gooseLeader()
demoSearch.userHTMLReport(
    demoSearch.getInfluUsers(
        10,demoSearch.search(term, 100000, "en", "mixed")),term)
