#!/usr/bin/env python
"""Create an info sheet on all the UFC fights scheduled for today."""

"""
1. Check if there's a UFC event today, collect the event name
2. Get the list of fights
3. Get info on each fight, including:
    - Info on the fighters (from ESPN), including:
        - Betting odds
        - Height
        - Weight
        - Age
        - Reach
        - Stance
        - SIG STR LPM
        - SIG STR %
        - SIG STR ACC
        - TD AVG
        - TD ACC
        - SUB AVG
        - W-L-D
        - (T)KO Record
        - Submission Record
        - Last 5 fights
        - YouTube links of the last 5 fights for each fighter
4. Create a markdown file with the info for each fight, in chronological order
5. Save the file to the current directory


Agents:
ufc event search - checks if there's a UFC event today, and if so, returns the event name
fight info search - collects info on each fight, excluding video links
fight video link search - collects video links for each fight

*** we need to ensure that structured outputs are used to transfer info between agents to ensure that the info is consistent and accurate

"""

import asyncio

