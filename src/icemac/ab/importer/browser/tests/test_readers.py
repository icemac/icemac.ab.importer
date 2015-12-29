def test_readers__Readers__1(address_book, browser):
    """It lists all registered import file readers."""
    browser.login('mgr')
    browser.open(browser.IMPORTER_OVERVIEW_URL)
    browser.getLink('Registered import file readers').click()
    assert browser.IMPORTER_READERS_LIST_URL == browser.url
    assert (['CSV file (comma separated fields, ISO-dates, UTF-8 encoded)'] ==
            browser.etree.xpath('//ul[@class="bullet"]/li/text()'))
