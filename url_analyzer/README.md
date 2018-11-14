# Write-up

## Building this Solution
With no prior Django experience, I first went through the [Writing your first Django app tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/). For the most part, I used the same project structure for this project as was used in the tutorial (creating an app to handle analysis, same way of handling POST vs. GET requests in a view, ...). However, unlike the tutorial, I placed most of the logic for analyzing HTML in a separate file (`/analyze/utils.py`)   , outside of the view. Each part of the analysis was split into separate functions for reusability and testability. I wrote a few tests in `/analyze/tests.py`. If I had more time, I would have liked to create more tests.

After the HTML analysis was working reasonably, I created a `Website` model to cache the results of analyzing a webpage in the database. This part was fairly straightforward, as it was explained well in the Django tutorial.

Assumptions/decisions made:
- The function that checks HTML version doesn't support every version of HTML
    - Only supports HTML 4.01 and up
    - Assumption is that there aren't many sites that still use HTML versions version less than 4.01
- Cached results are not deleted immediately after they are stale (older than 24 hours)
    - Currently, we only check if a DB entry is old when a query is made for it 
    - After we retrieve the cached results, we check if it is stale
    - If it is stale, we delete the entry
    - Otherwise, we'll keep it in the DB and return the cached results
- To check if a webpage has a login form, I just check if the webpage has an `input` field of type `password`
    - A webpage generally should only have this if there is a login form
    - And you generally can't login without this

One problem I encountered was when checking if a link was accessible, some webpages would refuse a connection when too many requests are sent in a short period of time. To help fix this, I specified a `backoff_factor` such that a delay is applied in between attempts to connect. In some cases, this is still not enough though, and when that happens the current implementation just says that the link is inaccessible.

Time: 8-9 hours