# CouponChef
[](https://d112y698adiu2z.cloudfront.net/photos/production/software_thumbnail_photos/002/717/540/datas/medium.png)

## [Project Demo](https://www.youtube.com/watch?v=C1cfvL4F5nk)

## [DevPost](https://devpost.com/software/couponchef?ref_content=user-portfolio&ref_feature=in_progress)

## Inspiration

We wanted to help college students worry less about food and have more variety of what they can make given their limited budget. Not many people take advantage of coupon books that they get in their mails, and those who do do not know what to make all the time. Thus, we created CouponChef to allow college students to create delicious dishes with the cheapest prices possible.

## What it does

CouponChef takes an image that the user uploads and identifies the food items using the ChatGPT API. The website then outputs the top five recipes that use the most food items from the coupon book and their missing ingredients, nutrition values, and steps as well.

## How we built it

We used Reactjs and Nextjs for the frontend and stylized the website using HTML and CSS. We used the ChatGPT API to parse the names of the food items into a json file. We then made calls to the Spoonacular API using Python given the food items in the json file and retrieved the recipe datas of the recipes that use the most ingredients listed in the coupon book.

## Challenges we ran into

We ran into some challenges with connecting the ChatGPT API to the frontend in Reactjs and Nextjs. We also took awhile to figure out how to use the Spoonacular API as none of us have ever used it before. We also ran into some technical issues with Github as we were all not that familiar with it and had sync errors with the different branches.

## Accomplishments that we're proud of

Although none of us knew each other before the hackathon, we are proud that we were able to work together and create a project. Some of us had little experience with the tools we used for the project given our majors and had to learn along the way within a short amount of time, but we are proud that we were still able to finish the project on time.

## What we learned

We were able to learn how to utilize the ChatGPT API to take images and parse out certain things that we wanted. We learned how to make calls to the Spoonacular API and retrieve the necessary data we needed for our website. All of us took on roles that we were less familiar in, which allowed us to make the most of this learning experience.

## What's next for CouponChef

In the future, we plan to make it so that users can upload multiple images at once so that they can see more recipes given a wider variety of ingredients. We also want to add more recipe details such as the total price per serving for each recipe to improve the quality of life of users.
