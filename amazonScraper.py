from bs4 import BeautifulSoup
import urllib2

def getAmazonSearchPage(searchTerm):
    '''Returns html data from an Amazon search page'''
    BaseSearchUrl = "http://www.amazon.com/s/?url=search-alias%3Daps&field-keywords="
    SearchUrlWithSearchTerm = BaseSearchUrl + searchTerm
    resultPage = getHtml(SearchUrlWithSearchTerm)
    return resultPage

def scrapeAmazon(searchTerm):
    '''Returns BeautifulSoup formatted html data from Amazon'''
    resultPage = getAmazonSearchPage(searchTerm)
    return soupify(resultPage)


def soupify(htmlData):
    '''Expects HTML data from a web page'''
    return BeautifulSoup(htmlData)


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
    return categoryLinkParentDiv.findAll('li')


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
    category = categories[nthItem - 1]
    return categoryWithoutMarkUp(category)


def categoryWithoutMarkUp(categoryMarkUp):
    '''Expects a single category (like from nthCategory)'''
    categoryStringDiv = categoryMarkUp.find("span", {"class": "refinementLink"})
    name = categoryStringDiv.string

    categoryCountDiv = categoryStringDiv.find_next("span", {"class": "narrowValue"})
    quantity = categoryCountDiv.string

    link = categoryMarkUp.find_next('a')['href']
    return link + " " + name + quantity


def fourStarsAndUp(parentLink):
    '''Expects a link to an Amazon search result page that has been sorted by category'''
    parentPage = soupify(getHtml(parentLink))
    starLinksOfPage = parentPage.find(text = "Avg. Customer Review").parent
    return starLinksOfPage.find_next('ul').find_next('li').find_next('a')['href']

def getHtml(url):
    '''Returns html data from a given url'''
    return urllib2.urlopen(url)




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
        '''Returns nth category without markup'''
        return nthCategory(self.categories, nthItem)

    def get4StarsAndUpFromNthCategory(self, nthCategory):
        '''Returns a link to the 4 star and up page for nth category'''
        realNumber = nthCategory
        category = self.getNthCategory(realNumber)
        parentLink = category.split()[0]
        return fourStarsAndUp(parentLink)


##### Example output
userInput = raw_input('Enter a search term: ')
scrape = amazonScrape(userInput)
scrape.getImage(1)
scrape.getFirstItemsCategory()
scrape.getNthCategory(1)
print "4 star and up link = " + scrape.get4StarsAndUpFromNthCategory(1)
# scrape.getCategoryList()
