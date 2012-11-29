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


def largestCategory(soupData):
    '''Expects BeautifulSoup formatted html data'''
    categoryLinkParentDiv = soupData.find("div", attrs={"id": "kindOfSort_content"})
    categoryStringDiv = categoryLinkParentDiv.find("span", {"class": "refinementLink"})
    print categoryLinkParentDiv
    categoryCountDiv = categoryStringDiv.find_next("span", {"class": "narrowValue"})
    return categoryStringDiv.string+" with"+categoryCountDiv.string+" results."


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

    def getFirstItemsCategory(self):
        """Returns the first search result's largest category"""
        print largestCategory(self.resultData)


##### Example output
userInput = raw_input('Enter a search term: ')
scrape = amazonScrape(userInput)
scrape.getImage(1)
scrape.getFirstItemsCategory()



#### notes
# <div id="kindOfSort_content"
# <ul>
# <li>
# follow the first <a href> tag
# the <span class="childRefinementLink">Electronics</span> right under the <a>
#     tag contains the name of the category

# Given "apple" - the link should be "http://www.amazon.com/s/ref=sr_nr_i_0?rh=k%3Aapple%2Ci%3Aelectronics&keywords=apple&ie=UTF8&qid=1354192313"
# or "s/ref=sr_nr_i_0?rh=k%3Aapple%2Ci%3Aelectronics&keywords=apple&ie=UTF8&qid=1354192313" in Electronics
# I can take out the "ref=sr_nr_i_0"



