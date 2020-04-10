import React, { Component } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";

import About from "./components/About";
import AddUser from "./components/AddUser";
import LoginForm from "./components/LoginForm";
import NavBar from "./components/NavBar";
import RegisterForm from "./components/RegisterForm";
import UsersList from "./components/UsersList";

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: [],
      title: "TestDriven.io"
    };

    this.addUser = this.addUser.bind(this);
    this.handleRegisterFormSubmit = this.handleRegisterFormSubmit.bind(this);
  }

  // Component Lifecycle Method that runs during the Commit Phase and can work with the DOM, run side effects, etc.
  componentDidMount() {
    this.getUsers();
  }

  // AJAX call to connect the client to the server
  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data });
      })
      .catch(err => {
        console.log(err);
      });
  }

  addUser(data) {
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  }

  handleRegisterFormSubmit(data) {
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`
    axios.post(url, data)
    .then((res) => {
      console.log(res.data);
    })
    .catch((err) => { console.log(err); });
};

  render() {
    return (
      <div>
        <NavBar title={this.state.title} />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Switch>
                  <Route
                    exact
                    path="/"
                    render={() => (
                      <div>
                        <h1 className="title is-1">Users</h1>
                        <hr />
                        <br />
                        <AddUser addUser={this.addUser} />
                        <br />
                        <br />
                        <UsersList users={this.state.users} />
                      </div>
                    )}
                  />
                  <Route exact path="/about" component={About} />
                  <Route
                    exact path='/register' render={() => (
                      <RegisterForm
                        handleRegisterFormSubmit={this.handleRegisterFormSubmit}
                      />
                    )}
                  />
                  <Route exact path="/login" component={LoginForm} />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
