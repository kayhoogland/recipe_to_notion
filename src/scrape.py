import os
from notion_client import Client
from recipe_scrapers import scrape_me


def client():
    return Client(auth=os.environ["API_TOKEN"])


def bullet_item(item):
    return {
        "object": "block",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "text": {"content": item},
                }
            ]
        },
    }


def numbered_item(item):
    return {
        "object": "block",
        "numbered_list_item": {
            "rich_text": [
                {
                    "text": {"content": item},
                }
            ]
        },
    }


def heading_2(text):
    return {
        "object": "block",
        "heading_2": {"rich_text": [{"text": {"content": text}}]},
    }


def ingredients(l):
    return [bullet_item(i) for i in l]


def instructions(l):
    return [numbered_item(i) for i in l]


def notion_request(url):
    scraper = scrape_me(url)
    parent = {"database_id": os.environ["DATABASE_ID"]}
    cover = {"external": {"url": scraper.image()}}
    properties = {
        "Name": {"title": [{"text": {"content": scraper.title()}}]},
        "Link": {"url": scraper.url},
    }
    children = [
        heading_2("Ingrediënten"),
        *ingredients(scraper.ingredients()),
        heading_2("Bereiding"),
        *instructions(scraper.instructions_list()),
    ]

    response = client().pages.create(
        parent=parent, properties=properties, cover=cover, children=children
    )
    return response["url"]
