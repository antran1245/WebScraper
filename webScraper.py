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
            posts.append(entry)
    
    # printToCSV(posts, filename, headers)

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
    rank = 1
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
            entry = Company(rank)
            entry.company = company
            entry.short = short
            entry.revenue = revenue
            entry.equity = equity
            entry.founders = founders
            entry.investors = investors
            entry.full = full
            company = ''
            founders = ''
            equity = ''
            revenue = ''
            investors = ''
            full = ''
            rank += 1
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
        rank += 1
        posts.append(entry)
    
    printToCSV(posts, filename, headers)



if __name__=='__main__':
    
    # The Top 100 Financial Technology Companies of 2022
    # finTech('finTech.csv', ['Rank', 'Company', 'Category', 'Full Description'])
    
    # Forbes The Cloud
    # cloud100('cloud100.csv', ['Rank', 'Company', 'Category', 'HQ Location', '# Employees', 'Valuation', 'Founders'])
    
    # Forbes Next Billion Dollar Startups
    # startups('startups.csv', ['Rank', 'Company', 'Short Description', 'Revenue', 'Total Equity', 'Founders', 'Key Investors', 'Full Description'])
    
    # Y Combinator Top Private Companies - 2022
    combinator('yCombinator.csv', ['Rank', 'Company', 'Website', 'Short Description', 'HQ Location', 'Status', 'Batch', 'Breakthrough'])
    
    # 27 Insider
    # insider('insider.csv', ['Rank', 'Company', 'Short Description', 'Total  Equity Funding', 'Full Description'])