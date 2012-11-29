from bs4 import BeautifulSoup
import urllib2

def getAmazonSearchPage(searchTerm):
    '''Returns html data from an Amazon search page'''
    BaseSearchUrl = "http://www.amazon.com/s/?url=search-alias%3Daps&field-keywords="
    SearchUrlWithSearchTerm = BaseSearchUrl + searchTerm
    resultPage = urllib2.urlopen(SearchUrlWithSearchTerm)
    return resultPage


def scrapeAmazon(searchTerm):
    '''Returns BeautifulSoup formatted html data from Amazon'''
    resultPage = getAmazonSearchPage(searchTerm)
    soupResults = BeautifulSoup(resultPage)
    return soupResults


def thumbnail(soupData, nthItem):
    """Expects BeautifulSoup formatted html data and an int
    representing which product's thumbnail you want returned """
    resultString = "result_" + str(nthItem - 1)
    firstProduct = soupData.find(id=resultString)
    firstProductImageDiv = firstProduct.find("div", {"class": "productImage"})
    return firstProductImageDiv.a.img['src']


def categoryList(soupData):
    '''Expects BeautifulSoup formatted html data'''
    categoryLinkParentDiv = soupData.find("div", attrs={"id": "kindOfSort_content"})
    categoryStringDivs = categoryLinkParentDiv.findAll('li')
    return categoryStringDivs


def largestCategory(categories):
    '''Expects a list of categories from amazonScrape'''
    if categories:
        for item in categories:
            return item
    return "There are no categories in this list."


def nthCategory(categories, nthItem):
    '''Expects a list of categories from amazonScrape and an int
    representing which category you would like to return'''
    if nthItem > len(categories):
        return "Your nth value is too large for the number of categories in the list."
    return categories[nthItem - 1]


class amazonScrape:
    '''Uses a search term to scrape amazon for data,
    can return the image of the first search result'''
    def __init__(self, searchTerm):
        self.resultData = scrapeAmazon(searchTerm)
        self.categories = categoryList(self.resultData)

    def getData(self):
        return self.resultData

    def getImage(self, nthItem):
        '''Prints the url of the nth product's thumbnail image'''
        print thumbnail(self.resultData, nthItem)

    def getFirstItemsCategory(self):
        """Returns the first search result's largest category"""
        print largestCategory(self.categories)

    def getCategoryList(self):
        '''Returns list of all categories'''
        print self.categories

    def getNthCategory(self, nthItem):
        '''Returns nth category'''
        print nthCategory(self.categories, nthItem)


##### Example output
userInput = raw_input('Enter a search term: ')
scrape = amazonScrape(userInput)
scrape.getImage(1)
scrape.getFirstItemsCategory()
scrape.getNthCategory(2)
# scrape.getCategoryList()






