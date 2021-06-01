import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, Toolbar,Typography} from '@material-ui/core';
import clsx from 'clsx';

const drawerWidth = 240;
const useStyles = makeStyles((theme) => ({
    toolbar: {
      paddingRight: 24, // keep right padding when drawer closed
    },
    appBar: {
      zIndex: theme.zIndex.drawer + 1,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
    },
    appBarShift: {
      marginLeft: drawerWidth,
      width: `calc(100% - ${drawerWidth}px)`,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    },
    menuButton: {
      marginRight: 36,
    },
    menuButtonHidden: {
      display: 'none',
    },
    title: {
      flexGrow: 1,
      textAlign: "center",
      textTransform: "uppercase"
    },
  }));
  
export default function TopBar(props) {
  const classes = useStyles();

  return (
    <AppBar position="absolute" className={clsx(classes.appBar, props.open && classes.appBarShift)}>
        <Toolbar className={classes.toolbar}>
          <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            INDEXING AND SEARCH 
          </Typography>
        </Toolbar>
      </AppBar>
  );
}
