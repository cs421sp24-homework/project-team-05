# Software Requirement Specification

## Problem Statement
People often face the dilemma of what to do with items still in good working order when they are preparing for a long-distance move. This is especially true for students who are only planning to live in their new location for a few years. The cost of shipping these items may exceed their value, but it seems wasteful to simply discard them in a junkyard. Additionally, for students who have recently arrived at their new location, it may not be worthwhile to purchase brand new items, and it can be difficult to acquire things from a distance without access to transportation. Furthermore, trading in person with strangers may raise safety concerns, particularly considering the crime rate in cities like Baltimore.

## Proposed Solution
This application is a web service that addresses this dilemma by providing a platform for people, especially students, to post their pre-owned items online anytime when they have a product that is idled. For people who want to register an account, they have to pass the identity verification. Users can create a post that contains all necessary information about the product they want to sell, and share it with their friends or social media. They can also browse what other people are selling, and see if there is anything they need. Before a user decides to buy an item from another person, they can arrange all the transaction details within their private chat, like making a bargain. The buyer can prioritize deals within their immediate community. reduces the risk associated with transactions.

## Potential Clients
The JHU community

## Functional Requirements
The application should have the following functional requirements:

### Must Have
* As a user, I want to be able to use JHED to authenticate myself to access my account, so my personal information can be protected from unauthorized access.
* As a user, I want to have my own profile page, so I can keep track of my account information and item status.
* As a seller, I want to be able to post items I would like to sell, so people in need can buy them.
* As a seller, I want to identify the buyer if we meet in person so that I know I am talking to the right person.
* As a buyer, I want to buy items I see on the webpage that I am interested in.
* As a buyer, I want to be able to search for items, so I don't need to waste time on goods I'm not interested in.
* As a buyer, I want to filter what's for sale in my apartment by different categories, so I can get it safe and easy.
* As a buyer, I want to collect potential items I may buy in the future and organize them in a wishlist.
* As a seller, I want to make the communication in real time, so the trade can be more efficient.
* As a buyer, I want to rate and write reviews for the seller each time I make a purchase so other buyers can decide the credibility of the seller based on the rating.
### Nice to Have
* As a buyer, I want to see items near my address on my homepage, so I can browse items convenient for pick up.
* As a seller, I want the platform to notify me when buyers reach out to me, so I know someone is interested in my item.
* As a user, I want to make a transaction process through chat so I can buy/sell items via the webpage.

## Software Architecture & Technology Stack
### Web Application Version

**Type of Application:** Web Application

**Architecture:** The Sechand web application will follow the MVC architecture, designed for creating apps with rapid development.

**Frontend:**
- **Framework:** Vue.js, 
- **Styling:** Bootstrap,

**Backend:**
- **API:** Django,
- **Authentication:** Django

**Database:**
- **Primary Database:** Heroku built-in PostgreSQL
- **ORM:** Django built-in ORM

**Deployment:**
- **Hosting:** Heroku
- **Continuous Integration/Continuous Deployment (CI/CD):** Github Action

**Additional Technologies:**
- **Version Control:** Git and GitHub for version control and collaborative development.
- **Testing Frameworks:**
  - Frontend: Vitest
  - Backend: unittest

## Similar Existing Apps
* Ebay
* Facebook Market Place

From potential clients perspective, these two platforms are not specifically targeting students. 

Despite these apps could find potentially more items, the quality of the item is not guranteed, as long as the identity of the seller. 

Because we encourage sellers and buyers meet in-person when selling items, it would be easier for buyers to check the item's condition. Plus, with "by apartment location" filtering and verified student identity, both sellers and buyers can have a secure and efficient trade.
