# CS50 project 2
This is my work for the project 2 of the CS50's Web programming with Python and Javascript. You will find a Django project with a app named auctions.
The goal of this project was to build an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”<br/>
Here are the caractetistics of the web application:
* Models: The application has 5 models (User, Auction, Bid, Comment, Watchlist).
* Create Listing: Users is able to visit a page to create a new listing. He has to specify a title for the listing, a text-based description, what the starting bid should be, a URL for an image for the listing and a category.
* Active Listings Page: The default route of the application gives a view all of the currently active auction listings. For each active listing, this page displays the title, description, current price, photo, category, date of the last bid and the author of the listing.
* Listing Page: Clicking on a listing takes users to a page specific to that listing. On that page, users is able to view all details about the listing, including the current price for the listing.
  * If the user is signed in, the user is able to add the item to their “Watchlist.” If the item is already on the watchlist, the user is able to remove it.
  * If the user is signed in, the user is able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
  * If the user is signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * A closed listing page notifies who is the winner.
  * Users who are signed in are able to add comments to the listing page. The listing page displays all comments that have been made on the listing.
* Watchlist: Users who are signed in are able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.
* Categories: Users are able to visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.
* Django Admin Interface: Via the Django admin interface, a site administrator is able to view, add, edit, and delete any listings, comments, and bids made on the site.

You can see a video demo here: https://www.youtube.com/watch?v=WwHJmchKqoU <br/>
To run the web application locally use the command:<br/>
python3 manage.py runserver
