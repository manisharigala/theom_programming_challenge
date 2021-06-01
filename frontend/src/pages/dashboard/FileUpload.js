import { Box, Button, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import React from 'react';
import { API_URL } from '../../config';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
const useStyles = makeStyles((theme) => ({
  formControl: {
      maxWidth: 350
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
}));

export default function SimpleSelect() {
  const classes = useStyles();
  const [file, setFile] = React.useState(null);
  const [error, setError] = React.useState("");
  const [showLoader, setShowLoader] = React.useState(false);
  const allowedFileFormats = new Set(['txt','json']);
  
  const handleFileChange = (event) => {
        let file = event.target.files[0];
        setError("")
        if(file) {
            let ext = file.name.split('.').pop();
            if(allowedFileFormats.has(ext)) {
                setFile(file)
            } else {
                setError("Please upload .txt or .json file");
                setFile(null)
            }
        }
  };
  const submitData = () => {
      if(!file) {
        setError("Please choose a file to upload");
        return;
      }
      
      var formData = new FormData();
      formData.append('file', file);
      setShowLoader(true)
      axios({
        method: "post",
        url: `http://${API_URL}/upload`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then(function (response) {
        setTimeout(() => {
          setShowLoader(false)
        }, 1000);
        console.log(response);
     })
     .catch(function (response) {
        setShowLoader(false)
        alert('Upload failed! Try again')
        console.log(response);
     });
  }
  return (
    <div>
      <Backdrop className={classes.backdrop} open={showLoader}>
        <CircularProgress color="inherit" />
        <div>
        Uploading...
        </div>
      </Backdrop>
      {/* <Box>
        <Typography color="textSecondary" variant="subtitle1">
            Instructions
        </Typography>
        <Typography color="textSecondary" variant="body1">
           1)  Add instructions here
        </Typography>
        <Typography color="textSecondary" variant="body1">
           2)  Add instructions here
        </Typography>
        <Typography color="textSecondary" variant="body1">
           3)  Add instructions here
        </Typography>
      </Box> */}
      <Box mt={3} display="flex">
        <Button
            variant="contained"
            component="label"
            style={{width: 200}}
            size="large"
        >
            Upload File
            <input id="file" type="file" name="file" aria-describedby="my-helper-text" accept=".json, .txt" onChange={handleFileChange}  hidden/>
        
        </Button>
        {file && 
            <Box display="flex" alignItems="center" ml={2}>
                <Typography >
                     {file.name}
                </Typography>  
            </Box>
             
        }
      </Box>
      <Box mt={3}>
        <Typography color="error">
            {error}
        </Typography>
      </Box>
      <Box mt={3}>
        <Button size="large" variant="contained" color="primary" onClick={submitData} style={{width: 200}}>
                Upload
        </Button>
      </Box>
    </div>
  );
}
