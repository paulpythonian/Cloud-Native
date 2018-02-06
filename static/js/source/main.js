import React, { Component } from 'react';
import { render } from 'react-dom'

import 'react-route'
import 'jquery'
import 'ajax'

class Main extends ComponentO{
    render(){
        return(
            <div>
                <h1>Welcome to cloud-native-app</h1>
            </div>
        );
    }
}

render(<Main/>, document.getElementById('react'));
