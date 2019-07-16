import time
from random import randint
from selenium.common.exceptions import NoSuchElementException
from .util import click_element
from .util import web_address_navigator
from .xpath import read_xpath




def get_story_data(browser, tag, logger):
    """not used fort the moment, more coding needed to understand this"""
    query_hash = "cda12de4f7fd3719c0569ce03589f4c4"

    graphql_query_URL = "https://www.instagram.com/graphql/query/?query_hash" \
                        "={}".format(query_hash)+"&variables={\"reel_ids\":[],\"tag_names\":[\"{}\"],\"location_ids\":[]," \
                        "\"highlight_reel_ids\":[],\"precomposed_overlay\":false,\"show_story_viewer_list\":true," \
                        "\"story_viewer_fetch_count\":50,\"story_viewer_cursor\":\"\"," \
                        "\"stories_video_dash_manifest\":false}".format(tag)

    print(graphql_query_URL)

    web_address_navigator(browser, graphql_query_URL)


def watch_story(browser, elem, logger, type):
    """
        Load Tag Stories, and watch it until there is no more stores
        to watch for the related element
    """

    if type is "tag":
        story_link = "https://www.instagram.com/explore/tags/{}".format(elem)
    else:
        story_link = "https://www.instagram.com/{}".format(elem)

    web_address_navigator(browser, story_link)

    # wait for the page to load
    time.sleep(randint(2, 6))

    story_elem = browser.find_element_by_xpath(
        read_xpath(watch_story.__name__+"_for_{}".format(type), "explore_stories"))

    if not story_elem:
        logger.info("'{}' {} POSSIBLY does not exist", elem, type)
        raise NoSuchElementException
    else:
        # load stories/view stories
        click_element(browser, story_elem)

    # watch stories until there is no more stories available
    logger.info('Watching stories...')
    while True:
        try:
            browser.find_element_by_xpath(
                read_xpath(watch_story.__name__+"_for_{}".format(type), "wait_finish"))
            time.sleep(randint(2, 6))
        except NoSuchElementException:
            break


