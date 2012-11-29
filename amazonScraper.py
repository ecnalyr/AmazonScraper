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
    firstProductImage = firstProduct.find("div", {"class": "productImage"})
    return firstProductImage.a.img['src']


class amazonScrape:
    '''Uses a search term to scrape amazon for data,
    can return the image of the first search result'''
    def __init__(self, searchTerm):
        self.resultData = scrapeAmazon(searchTerm)

    def getData(self):
        return self.resultData

    def getImage(self, nthItem):
        '''Prints the url of the nth product's thumbnail image'''
        print thumbnail(self.resultData, nthItem)


##### Example output
userInput = raw_input('Enter a search term: ')
scrape = amazonScrape("userInput")
scrape.getImage(1)
