#! C:\python2.7.16
##
## MODULE azure
##  try Bing search API
##
## Sumeet Sandhu
## Copyright (C) 2020- Elementary IP LLC
#############################################

if 1==1:
    directoryRoot = '/Users/SumeetSandhu/Documents/Climate/python/'
    import sys
    sys.path = [ directoryRoot , '/Users/SumeetSandhu/Documents/Patent/Code/Python/CONFIZ/Source' ]\
                  + sys.path
    sys.path = [  '/Users/SumeetSandhu/Documents/Patent/Code/Python/CONFIZ/Source/mytestenv' ,
                  '/Users/SumeetSandhu/Documents/Patent/Code/Python/CONFIZ/Source/mytestenv/lib/python2.7' ,
                 '/Users/SumeetSandhu/Documents/Patent/Code/Python/CONFIZ/Source/mytestenv/lib/python2.7/site-packages' ]\
                 + sys.path
    from azure.cognitiveservices.search.websearch import WebSearchClient
    from azure.cognitiveservices.search.websearch.models import SafeSearch
    from msrest.authentication import CognitiveServicesCredentials
    subscription_key1 = 'e718b920ffb24dbaa16233eab1169445'
    subscription_key2 = '86caa28f212b469a95ff40d1dd31d7a6'
    subscription_key = subscription_key1
    MY_ENDPOINT = 'https://climatecatalog.cognitiveservices.azure.com/'     #https://stackoverflow.com/questions/61035548/azure-bing-image-search-client-throws-resource-not-found
    client = WebSearchClient(endpoint=MY_ENDPOINT, credentials=CognitiveServicesCredentials(subscription_key))
    USER_AGENT = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2"
    #remove es-MX !
    markets = [ 'en-AU' , 'en-CA' , 'en-IN' , 'en-ID' , 'en-MY' , 'es-MX' , 'en-NZ' , 'en-PH' , 'en-ZA' , 'en-GB' , 'en-US' ] #https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-web-api-v7-reference#market-codes
    import init_UTIL
    from compiler.ast import flatten
    from datetime import datetime
    from time import sleep
    from collections import Counter
    from classify_IO import readCSV

if 1==1:
    tmp = readCSV(directoryRoot+'countryDomains.csv')  #https://www.worldstandards.eu/other/tlds/
    countryDomainD = {  re.search(r'(?<=^\.)[a-zA-Z]+(?= *)',w['Country code top-level domain (TLD)']).group(0) : w['Country / territory']
            for w in tmp if w.get('Country code top-level domain (TLD)') and w.get('Country / territory') and re.search(r'(?<=^\.)[a-zA-Z]+(?= *)',w['Country code top-level domain (TLD)'])  }
    queryD = {
        'data': [ 'climate data marketplace' , 'climate data' , 'climate database' , 'climate repository' ] ,
        'science' : [ 'climate measurement' , 'climate change measurement' , 'climate science data' , 'climate change data' , 'earth science data' ] ,
        'location' : [ 'geospatial climate data' , 'satellite data' , 'weather data' , 'local climate data' ] ,
        'nature' : [ 'environmental data' , 'ecological data' , 'ecosystem data' , 'nature data' ,  'climate conservation data' , 'nature conservation data' , 'climate species data' , 'climate deforestation data' ] ,
        'impact' : [ 'climate impact data' , 'climate pollution data' , 'climate water data' , 'climate soil data' , 'climate air data' , 'climate health data' ] ,
        'company' : [ 'climate corporate data' , 'sustainability data' , 'circular economy data' , 'sustainable supply chain data' , 'climate recycling data' , 'zero carbon data' , 'net zero data' , 'zero waste data' , 'climate manufacturing data' ] ,
        'economy' : [ 'climate economic data' , 'climate finance data' , 'climate commerce data' , 'climate investment data' , 'climate exchange data' , 'climate trade data' , 'climate credit data' , 'climate venture data' , 'climate funders data' ] ,
        'risk' : [ 'climate risk data' , 'climate resilience data' , 'climate insurance data' ] ,
        'energy' : [ 'climate energy data' , 'clean energy data' , 'renewable energy data' , 'climate solar data' , 'climate wind data'  ] ,
        'food' : [ 'climate agriculture data' , 'climate food data' , 'climate regeneration data' , 'regenerative agriculture data', 'permaculture data' , 'climate garden data' , 'climate home garden data' ] ,
        'infrastructure' : [ 'climate infrastructure data' , 'climate transportation data' , 'climate building data' , 'climate vehicle data' , 'net zero construction data' ] ,
        'ict' : [ 'climate sensor data' , 'climate blockchain data' , 'climate artificial intelligence data' , 'climate machine learning data' ] ,
        'entity' : [  'climate organizations data' , 'climate events data' , 'climate movements data' , 'climate services data' , 'climate jobs data' , 'climate careers data' , 'climate providers data' , 'climate consultants data' , 'climate leaders data' , 'climate volunteers data' , 'climate activists data' ] ,
        'government' : [  'climate government data' , 'climate policy data' , 'climate city data' , 'climate education data' , 'climate communication data' ]
        }                                        
    queries = sorted(flatten(queryD.values()))

if 1==2:    #ran several times as API throttled with 'out of quota' but worked after several minutes
    resultsL = []
    for query in queries:
        print('\r\nQuery: {}'.format(query))
        for market in markets:
            print ('\t{}'.format(market))
            resultO = client.web.search(query=query,pragma='no-cache',count=50,response_filter=['Webpages'],user_agent=USER_AGENT,market=market)
            if hasattr(resultO.web_pages, 'value'):
                resultL = resultO.web_pages.value
                print("\rResults# {}".format(len(resultL)))
                resultsL += [ dict(r.as_dict().items()+[ ('query',query),('market',market) ]) for r in resultL ]
            sleep(0.5)    #sleep between API calls - free account requires 3 calls/second, 1000/month
    jsonStr = json.dumps( resultsL, encoding='utf-8')
    timeStamp = '_{:%Y-%m-%d-%H-%M-%S}'.format(datetime.now())
    open(directoryRoot+'searchResults_'+timeStamp+'.json','w').write(jsonStr.encode("utf8"))

if 1==1:        #Open search results
    jsonStr = open(directoryRoot+'searchResults__2020-06-08-08-25-54.json','r').read()
    resultsLr = json.loads( jsonStr, encoding='utf-8')
    resultsL = [ eval(w) for w in set([ str(v) for v in resultsLr ]) ]  #unique results
    urlL = [ w['url'] for w in resultsL ]
    urls = sorted(set(urlL))

if 1==2:        #DOMAIN statistics
    r = [ re.search(r'https*\:\/\/(\w|\.|\-|\_)+\/', w).group(0) for w in urls if re.search(r'https*\:\/\/(\w|\.|\-|\_)+\/', w) ]
    Counter(r).most_common()    #top level url
    a = sorted(set(r))
    domains =  [ 'com' , 'org' , 'gov' , 'edu' , 'net' , 'int' , 'other' ] + countryDomainD.keys()
    domainD = { key : sorted(filter(lambda w: re.search(r'\.'+key+'\/* *$',w),a)) for key in domains if filter(lambda w: re.search(r'\.'+key+'\/* *$',w),a) }
    domainD['other'] = sorted(set(a)-set(flatten(domainD.values())))
    print('urls ={0}\tdomains ={1}'.format(len(r),len(a))
    stats = sorted([ (key,len(domainD[key])) for key in domainD.keys() ],key=lambda w:w[1],reverse=True)
    stats = map(lambda w: (countryDomainD[w[0]],w[1]) if w[0] in countryDomainD.keys() else w, stats)
    for w in stats: print w[0],'\t\t',w[1]

if 1==2:        #url/display_url/name/snippet statistics
    print('total URLs ={0},\tunique URLs ={1}'.format(len([ w['url'] for w in resultsL ]), len(set([ w['url'] for w in resultsL ]))))
    print('unique names ={0}, \tunique snippets ={1}, \tunique display_urls = {2}'.format(
        len(set([ w['name'] for w in resultsL ])) , len(set([ w['snippet'] for w in resultsL ])) , len(set([ w['display_url'] for w in resultsL ]))))
    urlD = { w:[] for w in urls }
    for w in resultsL:
        urlD[w['url']] += [ str({ key:w[key] for key in [ u'snippet', u'name', u'display_url' ] }) ]
    urlD = { key:[ eval(v) for v in sorted(set(urlD[key])) ] for key in urlD.keys() }
    a=filter(lambda w: len(w[1])>1, urlD.items())

if 1==2:        #URL statistics
    urlH = Counter(urlL).most_common()
    for w in urlH[0:50]: print w[0],'\t\t',w[1]
    
if 1==2:
    tmpD = dict(reduce(lambda u,v:u+v, [ [ (v,w[0]) for v in w[1] ] for w in queryD.items() ], []))
    topicD = { w:[] for w in queryD.keys() }
    for w in resultsL:
        topicD[tmpD[w['query']]] += [ w['url'] ]
    topicD = { key:sorted(set(topicD[key])) for key in topicD.keys() }
    
