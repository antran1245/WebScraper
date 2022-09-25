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
def printToCSV(posts, filename, header):
    try:
        with open(filename, 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(posts)
    except BaseException as e:
        print('BaseException:', filename, e)
    else:
        print('Data has been loaded successfully')

# Copy the content of the Fin Tech link.
# Create an array of class to represent each of the company.
# Read the information and correctly parse them into the correct class instance variables.
def finTech(filename, header):
    # Static URL
    URL = 'https://thefinancialtechnologyreport.com/the-top-100-financial-technology-companies-of-2022/'
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="td-post-content")
    # print(results.prettify())
    postings = results.find_all("p")
    # print(postings[5].find("b") == None)
    
    posts = []
    name = ""
    category = ""
    info = ""
    rank = 1
    for posting in postings[5:len(postings)-1]:
        
        # Check if strong tag is in the p tag to get the name of company
        if posting.find("strong") != None:
            title = posting.find("strong").text
            name = title[title.index('.')+2:]
            category = posting.text[posting.text.index('Category:')+10:]
        elif posting.text.strip() != "":
            info += posting.text+"\n\n"
        else:
            entry = Company(rank)
            entry.name = name
            entry.category =  category
            entry.info = info
            info = ""
            rank += 1
            posts.append(entry)
    
    # printToCSV(posts, filename, header)

def cloud100(filename, header):
    # Static website
    URL = "https://www.forbes.com/lists/cloud100/?sh=49fc6e5e7d9c"
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="table-row-group")
    # print(results[6].find_all("a")[0].find(class_="ceoName"))
    
    posts = []
    rank = 1
    company = ''
    category = ''
    hq = ''
    employees = ''
    valuation = ''
    ceo = ''
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
    
    # posts[0].printCompany()
    printToCSV(posts, filename, header)

if __name__=='__main__':
    
    # The Top 100 Financial Technology Companies of 2022
    # finTech('finTech.csv', ['Rank', 'Company', 'Category', 'Full Description'])
    
    # The Cloud
    cloud100('cloud100.csv', ['Rank', 'Company', 'Category', 'HQ Location', '# Employees', 'Valuation', 'Founders'])
    
