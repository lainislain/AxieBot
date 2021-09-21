
import requests
import pandas as pd
import json
from web3 import Web3
from solcx import compile_source

# header 


def run_query() :
    """
        gets lastest N axies on market
    """
    headers = {
        'authority': 'graphql-gateway.axieinfinity.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOjM3OTE0NjQsImFjdGl2YXRlZCI6ZmFsc2UsInJvbmluQWRkcmVzcyI6IjB4YjMxZjM3OThhNDI3NjAzZjk1ZTI5NzcwOGU4NGM0MjRlY2NiYmEzMyIsImV0aEFkZHJlc3MiOm51bGwsImlhdCI6MTYzMTg3MjI1NiwiZXhwIjoxNjMyNDc3MDU2LCJpc3MiOiJBeGllSW5maW5pdHkifQ.tyj0F2ikySIPApOMjUVZTr3T5QvPCs57kg2v87IZTYo',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://marketplace.axieinfinity.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://marketplace.axieinfinity.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    # variables and query // size is how many axies u want to get

    data = '{"operationName":"GetAxieLatest","variables":{"from":0,"size":15,"sort":"Latest","auctionType":"Sale"},"query":"query GetAxieLatest($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\\n axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\\n total\\n results {\\n ...AxieRowData\\n __typename\\n }\\n __typename\\n }\\n}\\n\\nfragment AxieRowData on Axie {\\n id\\n image\\n class\\n name\\n genes\\n owner\\n class\\n stage\\n title\\n breedCount\\n level\\n parts {\\n ...AxiePart\\n __typename\\n }\\n stats {\\n ...AxieStats\\n __typename\\n }\\n auction {\\n ...AxieAuction\\n __typename\\n }\\n __typename\\n}\\n\\nfragment AxiePart on AxiePart {\\n id\\n name\\n class\\n type\\n specialGenes\\n stage\\n abilities {\\n ...AxieCardAbility\\n __typename\\n }\\n __typename\\n}\\n\\nfragment AxieCardAbility on AxieCardAbility {\\n id\\n name\\n attack\\n defense\\n energy\\n description\\n backgroundUrl\\n effectIconUrl\\n __typename\\n}\\n\\nfragment AxieStats on AxieStats {\\n hp\\n speed\\n skill\\n morale\\n __typename\\n}\\n\\nfragment AxieAuction on Auction {\\n startingPrice\\n endingPrice\\n startingTimestamp\\n endingTimestamp\\n duration\\n timeLeft\\n currentPrice\\n currentPriceUSD\\n suggestedPrice\\n seller\\n listingIndex\\n state\\n __typename\\n}\\n"}'

    # sending Post request with data and headers

    response = requests.post('https://graphql-gateway.axieinfinity.com/graphql', headers=headers, data=data)

    # to json
    response = response.json()
    return response

def buy_axie(axie):

    content = """
    [
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "settleAuction",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    """
    contract_abi = json.loads(content)
    contract_address = '0x213073989821f738a7ba3520c3d31a1f9ad31bbd'

    contract_address = Web3.toChecksumAddress(contract_address)
    weth_address = '0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5'
    weth_address = Web3.toChecksumAddress(weth_address)
    # use infura 
    provider_url = ''
    w = Web3(Web3.HTTPProvider(provider_url))
    
    contract = w.eth.contract(abi=contract_abi, address=contract_address)

    # _seller, _token(RONIN WETH CONTRACT), _bidAmount, _listingIndex, _listingState
    data = contract.functions.settleAuction(Web3.toChecksumAddress(axie['auction']['seller']), weth_address, int(axie['auction']['currentPrice']), int(axie['auction']['listingIndex']), int(axie['auction']['state']))
    print(contract.encodeABI(fn_name='settleAuction'))


def select_axie(data, priceUsd):

    # filtering axies data
    # each axie have it's
    # ['id', 'image', 'class', 'name', 'genes', 'owner', 'stage', 'title', 'breedCount', 'level', 'parts', 'stats', 'auction', '__typename']
    data = data['data']['axies']['results']
    for axies in data:
        #if float(axies['auction']['currentPriceUSD']) <= priceUsd:
        print("Axie {} with current price of {} Usd, seller is : {}".format(axies['id'], axies['auction']['currentPriceUSD'], axies['auction']['seller']))
        print(axies)
        return axies



data = run_query()
buy_axie(select_axie(data, 300))
#print(contract_abi)
# printing data to screen 
#print(data)


# how to access Data and check cards  + price and purity + breed 
# using pandas  and json we have 
# response = response['data']['axies']['results']

# print(getList(response))
#rawData = pd.DataFrame(response, columns=['id', 'image', 'class', 'name', 'genes', 'owner', 'stage', 'title', 'breedCount', 'level', 'parts', 'stats', 'auction', '__typename'])

#print( rawData )
