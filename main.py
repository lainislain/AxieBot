import requests

header = {
    "Accept": "*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-US,en;q=0.5",
    "Connection":"keep-alive",
    "Content-Length":"308",
    "content-type":"application/json",
    "Host":"graphql-gateway.axieinfinity.com",
    "Origin":"https://marketplace.axieinfinity.com",
    "Referer":"https://marketplace.axieinfinity.com/axie/3861302",
    "TE":"Trailers",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0",
    "operationName":"GetAxieLatest",
    "variables": 
    {
        "from":0,
        "size":24,
        "sort":"Latest",
        "auctionType":"Sale",
        "criteria":{
            "region":'null',"parts":'null',"bodyShapes":'null',"classes":'null',"stages":'null',"numMystic":'null',"pureness":'null',"title":'null',"breedable":'null',"breedCount":'null',"hp":[],"skill":[],"speed":[],"morale":[]}},
        "query":"query GetAxieLatest($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
}


r = requests.post('https://graphql-gateway.axieinfinity.com/graphql', header)

print(r.json())