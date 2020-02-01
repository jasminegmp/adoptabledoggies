## Adoptable Doggies
To reveal the most common types of breeds and other information about dogs up for adoption, I analysed adoptable dogs in the counties of Southern California in January 2020.
I mined almost 200,000 datapoints throughout January 2020 using Petfinder's API, then used D3 to display the results found.

## Technologies used
* [React](https://reactjs.org/) for Javascript library
* [Flask](https://www.palletsprojects.com/p/flask/) for web framework
* [Pandas](https://pandas.pydata.org/) for data mining
* [PetFinder API](https://www.petfinder.com/developers/) for data
* [SimpleMaps](https://simplemaps.com/data/us-zips) to map zipcodes to counties
* [D3](https://d3js.org/) for data visualization
* [Heroku](https://heroku.com) for hosting
* [SCSS](https://sass-lang.com/) for styling
* [Visual Studio Code](https://code.visualstudio.com/) for coding
* [Yarn](https://yarnpkg.com/) for package manager



## Setup to Run Locally

### install dependencies
    * `yarn install`
    * `pip install -r requirements.txt`
    * `yarn add topojson`
    * `yarn add d3`

### Run Development Local

1. Start flask backend server
    - `npm run serve`
    - Optional: add env variable `DEV=True` for hot reloading on server

2. (In seperate tab): Start react dev server with hot reloader
    `npm start`

3. Visit http://localhost:3000.

    If you see, "data from the backend received," all is well.

### Setup to Deploy To Heroku

1. [Push your project to github](https://github.com/new)  

2. Create new app on heroku.

3. (On heroku) Click "settings" tab
    - add **nodejs** and **python** buildpacks. 

4. (on heroku) click "deploy" tab
    - select "Connect on Github" for deployment method. 

5. Click "Deploy Branch" under "Manual deploy" row.


## Other Credit

* [Flask initial boiler plate help](https://github.com/DZGoldman/flask-react-minimal-boilerplate)
* [D3 References](https://bl.ocks.org/)


 