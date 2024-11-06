# PhotoShare Web Application

PhotoShare is a web-based photo-sharing platform inspired by Flickr, developed as a project for our Database Systems course. The primary objective of the project was to design, implement, and document the back-end of a web application using **Django** and **PostgreSQL**. Our platform enables users to register, create albums, upload and manage photos, and engage with content through tags, likes, and comments. It includes robust user and photo management features, a recommendation system, and search functionalities that enrich the user experience.

## Features

### User Management
- **User Registration & Authentication:** Users can sign up, providing necessary details. Duplicate emails are restricted.
- **Friends List:** Users can add friends and view their friend lists, enhancing social connectivity on the platform.

### Album & Photo Management
- **Album Creation:** Registered users can create, edit, and delete albums, with each album containing photos.
- **Photo Upload & Management:** Photos can be uploaded to albums and are accessible to all users. Photos can be tagged to allow thematic browsing.
  
### Tag Management
- **Personal & Global Tag Views:** Users can categorize photos by tags, allowing both personal and global browsing by tag.
- **Popular Tags:** Displays the most popular tags, helping users discover trending content.

### Content Interaction
- **Comments:** Users and visitors can leave comments on photos, with registered users' comments contributing to an engagement score.
- **Like Functionality:** Users can like photos, and each photo shows the count of likes and the names of users who liked it.

### Advanced Search and Recommendations
- **Photo Search by Tags:** Allows both visitors and users to search photos by entering multiple tags.
- **Friends-of-Friends Recommendations:** Users receive friend recommendations based on their existing friends’ connections.
- **You-may-also-like Suggestions:** Personalized photo recommendations based on frequently used tags in the user's photo uploads.

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, JavaScript (Django templates).
- **Database Management:** PostgreSQL

## Project Highlights
- **Django ORM & PostgreSQL:** Leveraged Django’s ORM to structure and manage relational data with PostgreSQL, implementing complex queries for user recommendations and advanced search.
- **Scalable Database Design:** Efficiently structured tables to manage relationships between users, albums, photos, tags, and comments.

## How to Run the Project Locally
//todo
