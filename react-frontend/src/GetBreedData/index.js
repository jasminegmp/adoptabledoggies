import React from 'react';
import axios from 'axios';
import BreedVisualization from '../BreedVisualization/index';

class GetBreedData extends React.Component {

    constructor(props) {
        super(props);
        
        this.state = {
            loading: true,
            data: null,
            width: 700,
            height: 500,
            id: "root",
            submit: false
        };
    }
    
  componentDidMount() {

    var self = this;
    axios.post('http://127.0.0.1:5000/query')
        .then(function(response){
            //console.log(response);
            self.setState({data: response});
            self.setState({loading: false});
    //Perform action based on response
    })
    .catch(function(error){
        console.log(error);
    //Perform action based on error
    });
    //this.drawChart(this.state.data);
  }

  renderItem = (dog, index) =>{
      console.log(dog)
        return(
            <div>
                <h1>{dog[1]} :{dog[2]}</h1>
            </div>
        )
}
        
  render(){
    return ( <div>
        {this.state.loading ? null : <BreedVisualization data = {this.state.data}/>
        //this.state.data.data.data.map((dog, index) => this.renderItem(dog, index))
        }
        </div>
    )
  }
  }
      
  export default GetBreedData;