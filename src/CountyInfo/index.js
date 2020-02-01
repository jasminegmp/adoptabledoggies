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
      axios.get('https://api.jsonbin.io/b/5e34b84e50a7fe418c576743')
          .then(function(data){
              self.setState({countyData: data});
              self.extractData();
      })
      .catch(function(error){
          console.log(error);
      });
  }

  extractData = () =>{
    const {countyData, county} = this.state;
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
