API
======

There is an API for querying our server, using the api is by following the below
template: opa.org.il/api/v?/?<api_request> (simply replace the ? with the
API version and the <api_request> with the desired api call)

Below are it's versions:

Version 1
~~~~~~~~~~~~~~~
There are 2 types of available queries:
1. articleId=<ID> - This queries for a specific article with the ID of <ID>

2. query=<search_term> - This searches the historical DB and provides with
articles in which the <search_term> appears.
