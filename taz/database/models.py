#!/usr/bin/env python

""" models.py - Model definitions for the Aussie database """

__authors__ = ["Jared Smith"]
__copyright_ = "Copyright 2015, OSSEE"
__license__ = "MIT"

import sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class RedditSubreddit(DeclarativeBase):
    """Sqlalchemy subreddit model"""
    __tablename__ = "reddit_subreddits"

    id = Column(Integer, primary_key=True)
    display_name = Column('display_name', String, nullable=True)
    url = Column('url', String, nullable=True)
    subscribers = Column('subscribers', Integer, nullable=True)
    subreddit_type = Column('type', String, nullable=True)
    language = Column('language', String, nullable=True)

