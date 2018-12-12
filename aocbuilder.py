#!/usr/bin/env python3
# coding: utf-8

"""A simple tool to retrieve all the AoC exercises."""

import datetime
import os
import re
import requests
from tomd import Tomd


class AoCBuilder:
    """Main class."""

    def __init__(self, token, year=2015):
        """Invoke the builder with a token."""
        if not token:
            raise RuntimeError("You must provide an authentication token")

        self._aoc_uri = "https://adventofcode.com/{year}/day/{day}"  # will format() it

        self._token = token
        self._session = requests.Session()

        self._start_year = year
        if year < 2015:  # No AoC before 2015
            self._start_year = 2015

        with open("resource/README-AoC.md") as f:
            self._year_readme = f.read()

        self._year_readme_text = ""
        self._year_titles = []

        self._pattern_title = re.compile(r'''--- Day \d+: (.*) ---''')
        self._pattern_gl = re.compile(r'''Good luck!.*\n''')

    def request(self, url, **kwargs):
        """Make a request and return the result."""
        try:
            result = self._session.request(url=url, method="GET", **kwargs)
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            raise

        if result.status_code == 200:
            return result

    @staticmethod
    def create_folder(folder):
        """Create a folder."""
        try:
            os.mkdir(folder)
        except FileExistsError:
            print(f"{folder} exists, skip creation.")
            pass

    def _build_year_readme(self, year):
        """Create the README.md of the main AoC folder."""
        days = ""
        for idx, title in enumerate(self._year_titles):
            days += "- [Day {day:02d}: {title}](day{day:02d}/)\n".format(day=idx + 1, title=title)

        with open(f"AdventOfCode{year}/README.md", 'w') as readme:
            readme.write(self._year_readme.format(year=year, text=self._year_readme_text, days=days))

        self._year_readme_text = ""
        self._year_titles = []

    def _scrap(self, year, day, day_dir):
        """Scrap data from AoC website."""
        url = self._aoc_uri.format(year=year, day=day)
        response = self.request(url, cookies={"session": self._token})

        if not response:
            print(f"Exercise for {day}/12/{year} is not available")
            return

        html = response.text

        self._year_titles.append(self._pattern_title.search(html).groups()[0])
        # Why not group(0) ? Because it returns matching text with pattern,
        # not just the matching text itself

        begin = end = 0

        if day == 1:  # we get the introduction text
            # No BS4 ? Not for this trivial parsing
            begin = html.find('</h2>') + len('</h2>')
            end_str = self._pattern_gl.search(html).group(0)
            end = html.find(end_str) + len(end_str)
            self._year_readme_text = Tomd(html[begin:end]).markdown

        # Get the problem wording
        begin = end if end else html.find('</h2>') + len('</h2>')
        end = html.find('</article>') + len('</article>')
        problem_text = Tomd(html[begin:end]).markdown

        with open(f"{day_dir}/README.md", 'w') as readme:
            readme.write(f"# {self._year_titles[-1]}")
            readme.write(problem_text)

        # Get the input
        response = self.request(f"{url}/input", cookies={"session": self._token})
        inpiout = response.text

        with open(f"{day_dir}/input", 'w') as input_file:
            input_file.write(inpiout)

    def build(self):
        """Main loop."""
        now = datetime.datetime.now()
        current_year = now.year if now.month == 12 else now.year - 1

        for year in range(self._start_year, current_year + 1):
            root_dir = f"AdventOfCode{year}"
            print(f"Creating folder {root_dir}...")
            self.create_folder(root_dir)

            for day in range(1, 26):
                day_dir = f"{root_dir}/day{day:02d}"
                print(f"Creating folder {day_dir}...")
                self.create_folder(day_dir)

                self._scrap(year, day, day_dir)

            self._build_year_readme(year)
