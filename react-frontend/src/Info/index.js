import React from 'react';
import Footer from '../Footer/index';
import {withRouter} from 'react-router-dom';

class Info extends React.Component {
  

  render() {
    return (
        <div>
            <h1>Adoptable Doggies</h1>
            <p class = "info">Dogs are our best friends yet so many of them still need homes.
            </p>
            <p class = "info">
            To reveal the most common types of breeds and other information about dogs up for adoption, I analysed adoptable dogs in the counties of Southern California in January 2020.</p>
            <p class = "info">
                To create this map, I mined almost 200,000 datapoints throughout January 2020 using <a target="_blank" href = "https://www.petfinder.com/">Petfinder</a>'s API.
            </p>
            <p class = "info">
                To map counties to zipcodes, I ussed <a target="_blank" href = "https://simplemaps.com/data/us-zips">Simple Maps</a>.
            </p>
            <Footer/>
        </div>
    );
  }
}

export default withRouter(Info);