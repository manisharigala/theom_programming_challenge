import { Box, InputLabel, Typography } from '@material-ui/core';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import FormControl from '@material-ui/core/FormControl';
import IconButton from '@material-ui/core/IconButton';
import InputBase from '@material-ui/core/InputBase';
import MenuItem from '@material-ui/core/MenuItem';
import Paper from '@material-ui/core/Paper';
import Select from '@material-ui/core/Select';
import { makeStyles } from '@material-ui/core/styles';
import SearchIcon from '@material-ui/icons/Search';
import axios from 'axios';
import React, { useEffect } from 'react';
import CollapsibleTable from '../../components/Results';
import { API_URL } from '../../config';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: '2px 4px',
    display: 'flex',
    alignItems: 'center',
  },
  input: {
    marginLeft: 24,
    flex: 1,
  },
  iconButton: {
    padding: 10,
  },
  formControl: {
     width: 100
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));


export default function GetCarData() {
  const classes = useStyles();
  const [selected, setSelected] = React.useState('Any');
  const [searchKey, setSearchKey] = React.useState('');
  const [fieldOptions, setFieldOptions] = React.useState([]);
  const [searchResults, setSearchResults] = React.useState([]);
  const [error, setError] = React.useState("");
  const [showLoader, setShowLoader] = React.useState(false);

  const handleChange = (event) => {
    setError("");
    setSelected(event.target.value);
  };
  const handleSearchKeyChange = (event) => {
    setError("");
    setSearchKey(event.target.value);
  };
  const onKeyUp = (event) => {
    if (event.code === 'Enter') {
        search();
    }
  }
  useEffect(() => {
    axios({
      method: "get",
      url: `http://${API_URL}/fields`,
    })
    .then(function (response) {
      var filtered = response.data.filter(f => f.stored && f.indexed && f.name !== 'id');
      filtered.unshift({name: "Any"})
      setFieldOptions(filtered);
   })
   .catch(function (response) {
      console.log(response);
   });

  }, [])
  const search = () => {
      setSearchResults([]);
      if(!searchKey) {
          setError("Please enter search key");
          return;
      }
      let fields;
      if(selected == 'Any') {
          fields = fieldOptions.filter(f => f.name !== "Any").map(f=> f.name);
      } else {
          fields = [selected];
      }
      setShowLoader(true)
      axios.post(`http://${API_URL}/search` , {
        fields: fields,
        key: searchKey
      })
      .then(function (response) {
        setSearchResults(response.data.response.docs);
        setShowLoader(false)
      })
     .catch(function (response) {
      setSearchResults([]);
      setShowLoader(false)
     });
  }
  return (
    <div>
       <Backdrop className={classes.backdrop} open={showLoader}>
        <CircularProgress color="inherit" />
        <div>
        Searching...
        </div>
      </Backdrop>
      <Box mt={3}>
      <Paper component="form" className={classes.root}>
      <FormControl  className={classes.formControl} fullWidth>
        <InputLabel id="demo-simple-select-outlined-label">Select Field</InputLabel>
        <Select
          labelId="demo-simple-select-outlined-label"
          id="demo-simple-select-outlined"
          value={selected}
          onChange={handleChange}
          label="Select Field"
          fullWidth
        >
          {fieldOptions.map(o => <MenuItem value={o.name}>{o.name}</MenuItem>)}
        </Select>
      </FormControl>
        <InputBase
          className={classes.input}
          placeholder="Search"
          inputProps={{ 'aria-label': 'search' }}
          onChange={handleSearchKeyChange}
          onKeyUp={onKeyUp}
        />
        <IconButton className={classes.iconButton} aria-label="search"
          onClick={search}
        >
          <SearchIcon />
        </IconButton>
      </Paper>
      </Box>
      <Box mt={3}>
        <Typography color="error">
            {error}
        </Typography>
      </Box>
      <Box mt={3}>
        <Typography>
            Found {searchResults.length} results
        </Typography>
      </Box>
      {searchResults && searchResults.length > 0 &&
        <>
          <Box mt={3}>
            <CollapsibleTable data={searchResults}/>
          </Box>
        </> 
        
      }
    
    </div>
  );
}
