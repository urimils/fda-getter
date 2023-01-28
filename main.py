import requests

class Result:
  def __init__(self, country, reason_for_recall, code_info, report_date, recalling_firm, event_id, voluntary_mandated):
    self.country = country
    self.reason_for_recall = reason_for_recall
    self.code_info = code_info
    self.report_date = report_date
    self.recalling_firm = recalling_firm
    self.event_id = event_id
    self.voluntary_mandated = voluntary_mandated

def appendToResults(results, response):
    for result in response.get('results'):
        results.append(Result(
            result['country'],
            result['reason_for_recall'],
            result['code_info'],
            result['report_date'],
            result['recalling_firm'],
            result['event_id'],
            result['voluntary_mandated']
            ))

## write results and latest skip so next iteration can be accumulative and not from scratch
def writeToDB(results, total):
    print('do nothing for now')

def main():
    limit = 1000
    skip = 0
    api_url = "https://api.fda.gov/food/enforcement.json?limit={limit}&skip={skip}".format(limit=limit, skip=skip)
    response = requests.get(api_url).json()
    total = response['meta']['results']['total']
    if (total > 26000):
        print('too many results for simple paging')
        return
    results = []
    appendToResults(results, response)
    skip = limit
    while skip < total:
        api_url = "https://api.fda.gov/food/enforcement.json?limit={limit}&skip={skip}".format(limit=limit, skip=skip)
        appendToResults(results, requests.get(api_url).json())
        skip += limit
    writeToDB(results, total)



    

if __name__ == "__main__":
    main()
