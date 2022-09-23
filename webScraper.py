# Library
import requests
from bs4 import BeautifulSoup
import csv

# Class to represent the data from the HTML page to show on the csv
class Company:
    def __init__(self, rank):
        self.rank = rank
    
    def __iter__(self):
        return iter([self.rank, self.name, self.category, self.info])
    
    def printCompany(self):
        print(self.name + "\n" + self.category + "\n" + self.info)
        return

# Print the content from the HTML page to a csv file
def printToCSV(posts, filename):
    try:
        with open(filename, 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(posts)
    except BaseException as e:
        print('BaseException:', filename, e)
    else:
        print('Data has been loaded successfully')

# Copy the content of the Fin Tech link.
# Create an array of class to represent each of the company.
# Read the information and correctly parse them into the correct class instance variables.
def finTech():
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
            temp = Company(rank)
            temp.name = name
            temp.category =  category
            temp.info = info
            info = ""
            rank += 1
            posts.append(temp)
            
    return posts

def cloud100():
    # Static website
    URL = "https://www.forbes.com/lists/cloud100/?sh=49fc6e5e7d9c"
    # Get the content from URL
    page = requests.get(URL)
    # Parser the HTML content
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="table-row-group")
    print(results[0])

if __name__=='__main__':
    
    # The Top 100 Financial Technology Companies of 2022
    # posts = finTech('finTech.csv')
    
    # The Cloud
    cloud100()
    
    # printToCSV(posts)
