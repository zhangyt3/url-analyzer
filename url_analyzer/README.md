# Write-up

## Building this Solution
With no prior Django experience, I first went through the [Writing your first Django app tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/). For the most part, I used the same project structure for this project as was used in the tutorial (creating an app to handle analysis, same way of handling POST vs. GET requests in a view, ...). However, unlike the tutorial, I placed most of the logic for analyzing HTML in a separate file (`/analyze/utils.py`)   , outside of the view. Each part of the analysis was split into separate functions for reusability and testability. I wrote a few tests in `/analyze/tests.py`. If I had more time, I would have liked to create more tests.

After the HTML analysis was working reasonably, I created a `Website` model to cache the results of analyzing a webpage in the database. This part was fairly straightforward, as it was explained well in the Django tutorial.






## Other
- Time
- Problems
- Corresponding solutions