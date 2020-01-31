import React from 'react';
import "./styles.scss";
import {withRouter} from 'react-router-dom';


const Footer = () => {
    return(
        <div className = "footer">
            Data mined and visualized by <a className = "link-hover" href= "https://jasminegump.com/">Jasmine</a>. See it on <a className = "link-hover" href= "https://github.com/jasminegmp/adoptabledoggies">Github</a>. 
            
        </div>
    )
}

export default withRouter(Footer);
