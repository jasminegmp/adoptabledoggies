import React from 'react';
import Loader from '../Loader/index';
import axios from 'axios';
import D3CountyViz from '../D3CountyViz/index';

class CountyInfo extends React.Component {

  constructor(props) {
    super(props);
    
    this.state = {
      county: this.props.county,
      extractedCountyData: null,
      countyData: null,
      loading: true,
    };
  }

  componentDidMount() {
    var self = this;
      axios.post('http://127.0.0.1:5000/counties_data')
          .then(function(data){
              //console.log(response);
              self.setState({countyData: data});
              self.extractData();
              //self.setState({loading: false});
      //Perform action based on response
      })
      .catch(function(error){
          console.log(error);
      //Perform action based on error
      });
  }

  extractData = () =>{
    const {countyData, county, loading, extractedCountyData} = this.state;
    countyData.data.map((item, index) => {
        if (item.county === county){
            this.setState({extractedCountyData: item, loading: false})
        }
    })
  }

  render() {
    if(this.state.loading) {
      return <Loader/>;
    } 
    return (
        <div>
            <D3CountyViz data = {this.state.extractedCountyData}/>
        </div>
    );
  }
}

export default CountyInfo;
