import React from 'react';
import Dashboard from '../pages/dashboard/Dashboard';
import { Switch, Route } from "react-router-dom";

export default function Routes() {
  return (
    <Switch>
        <Route path="/" exact component={Dashboard} />
    </Switch>
  );
}
