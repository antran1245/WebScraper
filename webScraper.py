# Library
import requests
from bs4 import BeautifulSoup
import csv

# Class to represent the data from the HTML page to show on the csv
class Company:
    def __init__(self, rank):
        self.rank = rank
    
    def __iter__(self):
        return iter([*list(self.__dict__.values())])
    
    def printCompany(self):
        print([*list(self.__dict__.values())])
        return

# Print the content from the HTML page to a csv file
def printToCSV(posts, filename, headers):
    try:
        with open(filename, 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(posts)
    except BaseException as e:
        print('BaseException:', filename, e)
    else:
        print('Data has been loaded successfully')

# Copy the content of the Fin Tech link.
# Create an array of class to represent each of the company.
# Read the information and correctly parse them into the correct class instance variables.
def finTech(filename, headers):
    # Static URL
    URL = 'https://thefinancialtechnologyreport.com/the-top-100-financial-technology-companies-of-2022/'
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find(class_="td-post-content")
    # print(container.prettify())
    results = container.find_all("p")
    # print(results[5].find("b") == None)
    
    # Save all to an array
    posts = []
    
    # Placeholder for the row entry
    name = ""
    category = ""
    info = ""
    rank = 1
    
    # Start from 5 because the needed content start then
    for result in results[5:len(results)-1]:
        
        # Check if strong tag is in the p tag to get the name of company
        if result.find("strong") != None:
            title = result.find("strong").text
            name = title[title.index('.')+2:]
            category = result.text[result.text.index('Category:')+10:]
        elif result.text.strip() != "":
            info += result.text+"\n\n"
        else:
            entry = Company(rank)
            entry.name = name
            entry.category =  category
            entry.info = info
            entry.position = "Y"
            info = ""
            rank += 1
            posts.append(entry)
    
    printToCSV(posts, filename, headers)

# Get a copy of the Cloud 100 article.
# Parse into CSV.
def cloud100(filename, headers):
    # Static website
    URL = "https://www.forbes.com/lists/cloud100/?sh=49fc6e5e7d9c"
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="table-row-group")
    # print(results[6].find_all("a")[0].find(class_="ceoName"))
    
    # Save all to an array
    posts = []
    
    # Placeholder for the row in each set of table-row-group
    rank = 1
    company = ''
    category = ''
    hq = ''
    employees = ''
    valuation = ''
    ceo = ''
    
    # Many groups of table-row-group.
    # Each a tags content a company detail
    for result in results:
        for post in result.find_all("a"):
            company = post.find(class_="organizationName").text
            category = post.find(class_="industry").text
            hq = post.find(class_="headquarters").text
            employees = post.find(class_="employees").text
            valuation = post.find(class_="marketValue").text
            ceo = post.find(class_="ceoName").text
            entry = Company(rank)
            rank += 1
            entry.company = company
            entry.category = category
            entry.hq = hq
            entry.employees = employees
            entry.valuation = valuation
            entry.ceo = ceo
            entry.position = "Y"
            posts.append(entry)
    
    printToCSV(posts, filename, headers)

# Parse when all info are siblings
def startups(filename, headers):
    # Static website
    URL = "https://www.forbes.com/sites/amyfeldman/2022/08/16/next-billion-dollar-startups-2022/?sh=7fd6e1485308"
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find(class_="article-body")
    # Get all the immediate children of the article-body element
    results = container.find_all(recursive=False)
    
    posts = []
    company = ''
    founders = ''
    equity = ''
    revenue = ''
    investors = ''
    short = ''
    full = ''
    
    startParse = False
    for result in results[9:len(results)]:
        if result.name == 'h3':
            company = result.find('strong').text
        if result.name == 'h4':
            if result.find('br') != None:
                break
            elif founders == '':
                founders = result.find('strong').text
            elif equity == '':
                equity = result.find('strong').text
            elif revenue == '':
                revenue = result.find('strong').text
            elif investors == '':
                investors = result.find('strong').text
        if result.name == 'p':
            full = result.text
            entry = Company('n/a')
            entry.company = company
            entry.short = short
            entry.revenue = revenue
            entry.equity = equity
            entry.founders = founders
            entry.investors = investors
            entry.full = full
            entry.position = "Y"
            company = ''
            founders = ''
            equity = ''
            revenue = ''
            investors = ''
            full = ''
            posts.append(entry)
            
    printToCSV(posts, filename, headers)

# Read from multi-table and parse them correctly
def combinator(filename, headers):
    # Static website
    URL = "https://www.ycombinator.com/topcompanies"
    breakthroughURL = "https://www.ycombinator.com/topcompanies/breakthrough"
    publicURL = "https://www.ycombinator.com/topcompanies/public"
    # Get the content from URL
    page = requests.get(URL)
    breakthroughPage = requests.get(breakthroughURL)
    publicPage = requests.get(publicURL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    breakthroughSoup = BeautifulSoup(breakthroughPage.content, "html.parser")
    publicSoup = BeautifulSoup(publicPage.content, "html.parser")
    
    container = soup.find("tbody")
    results = container.find_all('tr')
    breakthroughCompanys = breakthroughSoup.find_all(class_="company-name")
    breakthroughDict = {breakthroughCompanys[i].text: 'Y' for i in range(0, len(breakthroughCompanys))}
    publicCompanys = publicSoup.find("tbody").find_all('tr')
    
    # spread the pulic list into the private companys list
    results.extend(publicCompanys)
    
    posts = []
    rank = 1
    company = ''
    website = ''
    short = ''
    hq = ''
    status = ''
    batch = ''
    breakthrough = ''
    breakthroughIndex = 0
    for result in results:
        company = result.find(class_="name").find(class_="company-name").text
        website = result.find(class_="name").find(class_="company-website", href=True)['href']
        short = result.find(class_="company-overview").text
        hq = result.find(class_="headquarters").text
        status = result.find(class_="status").text
        batch = result.find(class_="small-batch").text
        if company in breakthroughDict:
            breakthrough = 'Y'
            breakthroughIndex += 1
        else:
            breakthrough = 'N'
        entry = Company(rank)
        entry.company = company
        entry.website = website
        entry.short = short
        entry.hq = hq
        entry.status = status
        entry.batch = batch
        entry.breakthrough = breakthrough
        entry.position = "Y"
        rank += 1
        posts.append(entry)
    
    printToCSV(posts, filename, headers)

def insider(filename, headers):
    # Static website
    URL = "https://www.businessinsider.com/most-promising-consumer-tech-startups-of-2022-8"
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find(class_="slide-wrapper")
    results = container.find_all("div", recursive=False)
    
    posts = []
    company = ""
    short = ""
    equity = ""
    full = ""
    for result in results:
        pTags = result.find_all('p')
        company = pTags[0].find('a').text
        equity = pTags[3].find('strong').next_sibling
        i = 0
        while not equity[i].isalpha():
            i += 1
        equity = equity[0:i] + " M"
        full = pTags[4].find('strong').next_sibling + "\n\n" + pTags[5].find('strong').next_sibling
        entry = Company('n/a')
        entry.company = company
        entry.short = short
        entry.equity = equity
        entry.full = full
        entry.position = "Y"
        posts.append(entry)
    
    printToCSV(posts, filename, headers)

def mergeCSV(filename, mainCompanysList, compareDict):
    mergeList = []
    with open(filename, 'r', encoding='utf-8') as f:
        dict_reader = csv.DictReader(f)
        mergeList = list(dict_reader)
        
    for company in mergeList:
        if company['Company'] not in compareDict:
            entry = {'Rank': company['Rank']}
            entry['Company'] = company['Company'] if 'Company' in company else ''
            entry['Website'] = company['Website'] if 'Website' in company else ''
            entry['Category'] = company['Category'] if 'Category' in company else ''
            entry['Short Description'] = company['Short Description'] if 'Short Description' in company else ''
            entry['Year Founded'] = company['Year Founded'] if 'Year Founded' in company else ''
            entry['HQ Location'] = company['HQ Location'] if 'HQ Location' in company else ''
            entry['# Employees'] = company['# Employees'] if '# Employees' in company else ''
            entry['Revenue'] = company['Revenue'] if 'Revenue' in company else ''
            entry['Ticker'] = company['Ticker'] if 'Ticker' in company else ''
            entry['Total Equity Funding'] = company['Total Equity Funding'] if 'Total Equity Funding' in company else ''
            entry['Valuation ($B)'] = company['Valuation ($B)'] if 'Valuation ($B)' in company else ''
            entry['Founders'] = company['Founders'] if 'Founders' in company else ''
            entry['Key Investors'] = company['Key Investors'] if 'Key Investors' in company else ''
            entry['The Information Top 50'] = 'N'
            entry['Wealthfront 2021'] = 'N'
            entry['LinkedIn Top Startups 2021'] = 'N'
            entry['F-Prime'] = 'N'
            entry['TC Unicorn'] = 'N'
            entry['The Information 2022 Likely IPOs'] = 'N'
            entry['Founder Collective'] = 'N'
            entry["Founder's Fund"] = 'N'
            entry['Sequoia'] = 'N'
            entry['Benchmark Capital'] = 'N'
            entry['General Catalyst'] = 'N'
            entry['Sutter Hill Ventures'] = 'N'
            entry['Felicis Ventures'] = 'N'
            entry['Cota Capital'] = 'N'
            entry['Costanoa Ventures'] = 'N'
            entry['Elevation Partners'] = 'N'
            entry['Garuda.vc'] = 'N'
            
            entry['FinTech Top 100'] = 'Y' if 'finTech.csv' == filename else 'N'
            entry["Forbes Next Billion Dollar Startups"] = 'Y' if 'startups.csv' == filename else 'N'
            entry['Forbes The Cloud 100'] = 'Y' if 'cloud100.csv' == filename else 'N'
            entry['Insider 27 Most Promising'] = 'Y' if 'insider.csv' == filename else 'N'
            entry['YCombinator Top Private Companies'] = 'Y' if 'yCombinator.csv' == filename else 'N'
            
            entry['Full Description'] = company['Full Description'] if 'Full Description' in company else ''
            entry['LinkedIn Profile Link'] = company['LinkedIn Profile Link'] if 'LinkedIn Profile Link' in company else ''
            entry['Crunchbase Profile Link'] = company['Crunchbase Profile Link'] if 'Crunchbase Profile Link' in company else ''
            mainCompanysList.append(entry)
            compareDict[company['Company']] = len(mainCompanysList)-1
        else:
            # print(company['Company'])
            # print(mainCompanysList[compareDict[company['Company']]]['Company'])
            mainCompanysList[compareDict[company['Company']]]['FinTech Top 100'] = 'Y' if 'finTech.csv' == filename else 'N'
            mainCompanysList[compareDict[company['Company']]]["Forbes Next Billion Dollar Startups"] = 'Y' if 'startups.csv' == filename else 'N'
            mainCompanysList[compareDict[company['Company']]]['Forbes The Cloud 100'] = 'Y' if 'cloud100.csv' == filename else 'N'
            mainCompanysList[compareDict[company['Company']]]['Insider 27 Most Promising'] = 'Y' if 'insider.csv' == filename else 'N'
            mainCompanysList[compareDict[company['Company']]]['YCombinator Top Private Companies'] = 'Y' if 'yCombinator.csv' == filename else 'N'


def mainList(filename, headers):
    mainCompanysList = []
    compareDict = {}
    with open("mainCompanyList.csv", 'r', encoding='utf-8') as f:
        dict_reader = csv.DictReader(f)
        mainCompanysList = list(dict_reader)

    for idx, company in enumerate(mainCompanysList):
        compareDict[company['Company']] = idx
    
    mergeCSV("finTech.csv", mainCompanysList, compareDict)
    mergeCSV("cloud100.csv", mainCompanysList, compareDict)
    mergeCSV("insider.csv", mainCompanysList, compareDict)
    mergeCSV("startups.csv", mainCompanysList, compareDict)
    mergeCSV("yCombinator.csv", mainCompanysList, compareDict)
    posts = []
    for company in mainCompanysList:
        posts.append(list(company.values()))
    printToCSV(posts, filename, headers)


if __name__=='__main__':
    
    # # The Top 100 Financial Technology Companies of 2022
    # finTech('finTech.csv', ['Rank', 'Company', 'Category', 'Full Description', 'FinTech Top 100'])
    
    # # Forbes The Cloud
    # cloud100('cloud100.csv', ['Rank', 'Company', 'Category', 'HQ Location', '# Employees', 'Valuation', 'Founders', 'Forbes The Cloud 100'])
    
    # # Forbes Next Billion Dollar Startups
    # startups('startups.csv', ['Rank', 'Company', 'Short Description', 'Revenue', 'Total Equity', 'Founders', 'Key Investors', 'Full Description', 'Forbes Next Billion Dollar Startups'])
    
    # # Y Combinator Top Private Companies - 2022
    # combinator('yCombinator.csv', ['Rank', 'Company', 'Website', 'Short Description', 'HQ Location', 'Status', 'Batch', 'Breakthrough', 'YCombinator Top Private Companies'])
    
    # # 27 Insider
    # insider('insider.csv', ['Rank', 'Company', 'Short Description', 'Total  Equity Funding', 'Full Description', 'Insider 27 Most Promising'])
    
    mainList('mainList.csv',  ['#', 'Company', 'Website', 'Category', 'Short Description', 'Year Founded', 'HQ Location', '# Employees', 'Revenue', 'Ticker', 'Total Equity Funding', 'Valuation ($B)',
    'Founders', 'Key Investors', 'The Information Top 50', 'Wealthfront 2021', 'LinkedIn Top Startups 2021', 'F-Prime', 'TC Unicorn', 'The Information 2022 Likely IPOs', 'Founder Collective', "Founder's Fund",
    'Sequoia', 'Benchmark Capital', 'General Catalyst', 'Sutter Hill Ventures', 'Felicis Ventures', 'Cota Capital', 'Costanoa Ventures', 'Elevation Partners', 'Garuda.vc', 'FinTech Top 100',
    "Forbes Next Billion Dollar Startups", 'Forbes The Cloud 100', 'Insider 27 Most Promising', 'YCombinator Top Private Companies', 'Full Description', 'LinkedIn Profile Link', 'Crunchbase Profile Link'])