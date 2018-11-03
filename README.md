# A Book Review website
A web application built with  python **flask** framework, that allows users to search for books and leave
reviews. Users can also query for book details programmatically via the website's API.

## Getting Started
Fork and download this repo on your local machine. 

### PostgreSQL, Python and Flask
Follow these [instructions](https://docs.cs50.net/web/2018/x/projects/1/project1.html), for detailed steps on what and how to setup 
**PostgreSQL**, **Python** and **Flask** to use with this application.

### Goodreads API
This API was used to get access to review data for individual books. 
You will have to register with [Goodreads](https://www.goodreads.com/api),if you have not. 

Apply for an **API KEY** and set your environment variable on your machinge to **API_KEY = KEY GOTTEN FROM GOODREADS**. 
Without the **API KEY**, the application cannot make successful requests to goodreads API.

## Implementation
### Registeration
Users can register through the site's homepage and, if successful, will be redirected to the login page. Successful login
will give the user access to search for books stored in database. Users can also log out from the site. This was achieved 
through the use of **session**

### Books
Books can be searched according to **author**, **title**, and **isbn value**. All books matching the search query is displayed
on the site, with links to their respective page. Individual book links are created according to their **isbn value**.

### Reviews
User can leave rating and review of a book on the book site, which is available for view to other users. User cannot leave
more than one review per book. This was achieved by setting the **primary key** of the **review table** to the username.

### API access
Users can programmatically send a **GET** request using the book **isbn** to the **/api/isbn** route, and get a `JSON` response 
containing the book's **title**, **author**, **publication date**, **ISBN value**, **review count**, and **average score**.

A **404** error page is displayed for a book not found.

## Author
Kayode Oluborode

