import gooseLeader
from gooseLeader import gooseLeader

term = input('Enter a search term: ')
demoSearch = gooseLeader()
demoSearch.userHTMLReport(
    demoSearch.getInfluUsers(
        10,demoSearch.search(term, 1000000, "en", "mixed")),term)
