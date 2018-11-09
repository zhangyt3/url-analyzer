# url-analyzer

The objective is to build a rest backend that does some analysis of a web-page/URL.
## Functional Requirements
* The backend should receive the URL of the webpage being analyzed as a parameter. 
* After processing the results should be returned to the user. The result comprises the following information:
** What HTML version has the document?
** What is the page title?
** How many headings of what level are in the document?
** How many internal and external links are in the document? Are there any inaccessible links and how many?
** Did the page contain a login-form?

In case the URL given by the user is not reachable an error message should be sent as a response. The message should contain the HTTP status-code and some useful error description.

## Non-Functional Requirements:

The backend should cache the scraping results for each URL for 24 hours such that your backend does not have to redo the scraping for any given URL within the next 24 hours.


## Your Solution
Please write an application handling all the wanted features. HINT: for document analysis consider using a library.

Please write the backend using Python 3 and Django. You can use any additional libraries you want.

## Submission of Results
Please provide the result as a Git repository with this content:

1. The project with all source files.
2. A short text document that lists the main steps of building your solution as well as all assumptions/decisions you made in case of unclear requirements or missing information. Additionally, write how much time did the project take you, what were parts where you had a problem and how did you solve it. If you couldn’t solve something let us know what did you try doing.
