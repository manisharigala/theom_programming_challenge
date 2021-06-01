import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { ThemeProvider , createMuiTheme } from '@material-ui/core';
import blue from '@material-ui/core/colors/blue';
import orange  from '@material-ui/core/colors/orange';

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark',
    primary: blue,
    secondary: orange
  },
});
ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
        <App />
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
