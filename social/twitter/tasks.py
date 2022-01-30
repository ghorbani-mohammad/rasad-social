import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from celery import shared_task
from celery.utils.log import get_task_logger

from network import models as net_models

logger = get_task_logger(__name__)


def scroll(driver, counter):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_counter = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        scroll_counter += 1
        if new_height == last_height or scroll_counter > counter:
            break
        last_height = new_height


def get_post_detail(article):
    detail = {}
    for item in ['reply', 'retweet', 'like']:
        detail[f'{item}_count'] = int(
            article.find_element(
                By.XPATH,
                f".//div[@role='button' and @data-testid='{item}']",
            )
            .get_attribute('aria-label')
            .split()[0]
        )
    return detail


@shared_task(name="store_twitter_posts")
def store_twitter_posts(
    channel_id, post_id, body, replies_counter, retweets_counter, likes_counter
):
    exists = net_models.Post.objects.filter(
        network_id=post_id, channel_id=channel_id
    ).exists()
    data = {
        "replies_count": replies_counter,
        "retweets_count": retweets_counter,
        "likes_count": likes_counter,
    }
    if not exists:
        net_models.Post.objects.create(
            channel_id=channel_id, network_id=post_id, body=body, data=data
        )
    else:
        post = net_models.Post.objects.filter(body=body, channel_id=channel_id).first()
        post.data = data
        post.save()


@shared_task(name="get_posts")
def get_posts(channel_id):
    channel = net_models.Channel.objects.get(pk=channel_id)
    channel_url = channel.username
    driver = webdriver.Remote(
        "http://social_firefox:4444/wd/hub",
        DesiredCapabilities.FIREFOX,
    )
    driver.get(channel_url)
    scroll(driver, 2)
    articles = driver.find_elements(By.TAG_NAME, "article")
    time.sleep(10)
    articles = driver.find_elements(By.TAG_NAME, "article")
    for article in articles:
        try:
            body = article.find_element(
                By.XPATH,
                ".//div[@dir='auto' and starts-with(@id,'id__') and not(contains(@data-testid, 'socialContext'))]",
            )
            post_id = int(
                article.find_element(
                    By.XPATH,
                    ".//a[@role='link' and @dir='auto' and starts-with(@id,'id__')]",
                )
                .get_attribute('href')
                .split('/')[-1]
            )
            post_body = body.text
            post_detail = get_post_detail(article)
            store_twitter_posts.delay(
                channel_id,
                post_id,
                post_body,
                post_detail['reply_count'],
                post_detail['retweet_count'],
                post_detail['like_count'],
            )
        except Exception as e:
            logger.error(e)
    driver.quit()
