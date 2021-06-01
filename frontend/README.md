# Minimum system requirements

1. OS: macOS, Windows, Linux
2. NodeJS Runtime Environment. To install follow : [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

# Steps to run the application

1. Open terminal from the projects root folder
2. Run `npm install`
3. Wait for packages to install
4. Run `npm start` - This runs the app in the development mode.
5. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

# Technologies used
1. React
2. JavaScript
3. HTML5
4. CSS3
5. Material-UI Library
6. Axios for mock REST APIs

# Walkthrough of the application

* Idea was to build a tool around the requirements of the challenge
* Assumption: This tool would be used by ML/AI engineers at Tesla to view and refine image datasets.
* I was given a set of images and a CSV file which contains information of the bounding boxes and their labels.
* I used a JS file as a mock database and used 'axios-mock-adapter' to mock a REST API interaction. Loaded the given data as JSON and populated the database to start with.
* Dashboard page shows a list of projects. Application is pre-loaded with the current project.
* Navigating inside a project would display the list of images and the bounding box drawn. Hover over the box shows the label.
* There are 3 view modes which resize and rearrange the images in the grid.
* Filters button opens up a toolbar where user can filter on 'Labels' and 'Hour of the day (scraped from the image name, just an idea)'
* Clicking on any image takes to a fullscreen view with options to edit label and resize and reposition the bounding box.
* Save option is provided to save the changes to the mock database.
* Upon filtering, the new set of images can be saved as a new project.
* Each project can be downloaded from the Dashboard page tiles as a CSV file resembling the original input.
