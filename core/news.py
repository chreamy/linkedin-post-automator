from eventregistry import *
er = EventRegistry(apiKey = 'b49ff879-8adc-497a-8785-46eec915c073', allowUseOfArchive = False)
import datetime
class News:
    def getUrls(topic):
        concept = er.getConceptUri(topic)
        USAUri = 'http://en.wikipedia.org/wiki/United_States'
        stockNewsUri = er.getConceptUri('Stock Market')
        q = QueryArticlesIter(
            conceptUri=concept,
            ignoreConceptUri=stockNewsUri,
            dateStart=(datetime.date.today()- datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            sourceLocationUri = [USAUri])
        # we limit here the results to 200. If you want more, remove or increasae maxItems
        out=[]
        for article in q.execQuery(er, sortBy="sourceImportance", sortByAsc=False, maxItems=5):
            out.append({'text':article['body'],'url':article['url'],'image':article['image']})
        return out