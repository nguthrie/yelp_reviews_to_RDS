import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def main_scraper(url, csv_name):
    """
    Calls all helper functions to assemble final data.
    :param soup: html soup object
    :return: list of data as columns. i.e all usernames as first list
    """

    soup = get_soup(url)

    usernames = get_usernames(soup)
    review_date = get_dates(soup)
    star_ratings = get_star_ratings(soup)
    friend_count, review_count = get_friend_and_review_counts(soup)
    review_text = get_review_texts(soup)

    list_of_data = [usernames, review_date, star_ratings, friend_count, review_count, review_text]
    create_csv(list_of_data, csv_name)


def get_usernames(soup):
    """Takes soup, returns list of usernames."""

    regex = r'target="">(.*)\.<\/a>'
    usernames = []
    username_matches = soup.find_all('a', class_="lemon--a__373c0__IEZFH link__373c0__1G70M "
                                                 "link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE")
    for username_match in username_matches:

        username = re.search(regex, str(username_match))
        if username:
            usernames.append(username.group(1))
    print("Collected usernames.")
    return usernames


def get_review_texts(soup):
    """
    Takes soup, returns list of review texts.
    Notes: removed ',' in output to simplify SQL upload.
    """
    regex = r'lang="en">(.*)<\/span'
    review_texts = []
    review_matches = soup.find_all('p', class_="lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__"
                                               "3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-")
    for review_match in review_matches:

        review = re.search(regex, str(review_match))
        review = re.sub(r'<br/>', '', review.group(1))
        review = re.sub(r',', '', review)
        if review:
            review_texts.append(review)
    print("Collected review texts.")
    return review_texts


def get_star_ratings(soup):
    """Takes soup, and returns list of star ratings."""
    # note: gets the star rating for the restaurant as well as first match, so remove the first match
    # note: when using this functions on multiple pages, make sure to not get irrelevant stars

    regex = r'aria-label="([\d\. ]*)star rating'
    star_matches = soup.find_all('div', class_="lemon--div__373c0__1mboc stickySidebar--heightContext__373c0__133M8 "
                                               "tableLayoutFixed__373c0__12cEm arrange__373c0__2C9bH "
                                               "padding-b4__373c0__uiolV border--bottom__373c0__3qNtD border-color"
                                               "--default__373c0__3-ifU")
    star_ratings = re.findall(regex, str(star_matches))
    star_ratings_minus_first_stars = star_ratings[1:]
    print("Collected star ratings.")
    return star_ratings_minus_first_stars


def get_friend_and_review_counts(soup):
    """Takes soup, and returns separate lists of friends and review counts."""
    # note: triple matches friends, so take each third element only
    # note: missing values are set to 0 to make sure column lengths match
    friend_regex = r'<b>([\d]*)<\/b> friends'
    review_regex = r'<b>([\d]*)<\/b> reviews'
    friend_numbers, review_numbers = [], []
    friend_number_matches = soup.find_all('span', class_="lemon--span__373c0__3997G")
    last_added = ""     # is set to "F" for friend or "R" for review
    for i, friend_number_match in enumerate(friend_number_matches):
        friend_number = re.search(friend_regex, str(friend_number_match))
        review_number = re.search(review_regex, str(friend_number_match))
        if friend_number and i % 3 == 0:
            if last_added == 'F':
                review_numbers.append(0)
            friend_numbers.append(friend_number.group(1))
            last_added = 'F'
        if review_number and i % 3 == 0:
            if last_added == 'R':
                friend_numbers.append(0)
            review_numbers.append(review_number.group(1))
            last_added = 'R'
    print("Collected friend counts and review counts.")
    return friend_numbers, review_numbers


def get_dates(soup):
    """Takes soup, and returns list of dates each review was given on."""
    regex = r'([\d]{1,2}\/[\d]{1,2}\/[\d]{4})'
    dates = []
    date_matches = soup.find_all('span', class_="lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0"
                                                "__jCeOG text-align--left__373c0__2XGa-")
    for date_match in date_matches:
        date = re.search(regex, str(date_match))
        if date:
            dates.append(date.group(1))
    print("Collected dates.")
    return dates


def create_csv(list_of_lists, csv_name):
    """
    Takes a list of lists, with each column matching the names below.
    :param list_of_lists:
    :return:
    """

    reviews_df = pd.DataFrame(columns=['username', 'review_date', 'star_rating', 'friend_count',
                                       'reivew_count', 'review_text'])

    for index, data in enumerate(list_of_lists):
        reviews_df.iloc[:, index] = data

    reviews_df.to_csv(csv_name, index=False)


if __name__ == "__main__":

    pass
    # input_url = "https://www.yelp.ca/biz/lov-king-west-toronto-2"
    # csv_name = "reviews.csv"
    # main_scraper(input_url, csv_name)
