import React from 'react';
import "./styles.scss";
import {withRouter} from 'react-router-dom';


const Footer = () => {
    return(
        <div class = "footer">
            Data mined and visualized by <a class = "link-hover" target="_blank" href= "https://jasminegump.com/">Jasmine</a>.
        </div>
    )
}

export default withRouter(Footer);
