import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";
import axios from "axios";
import About from "./components/About";
import AddUser from "./components/AddUser";
import UsersList from "./components/UsersList";

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: [],
      username: "",
      email: ""
    };

    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
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

  addUser(event) {
    event.preventDefault();

    const data = {
      username: this.state.username,
      email: this.state.email
    };

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

  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  render() {
    return (
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
                      <AddUser
                        username={this.state.username}
                        email={this.state.email}
                        addUser={this.addUser}
                        // eslint-disable-next-line react/jsx-handler-names
                        handleChange={this.handleChange}
                      />
                      <br />
                      <br />
                      <UsersList users={this.state.users} />
                    </div>
                  )}
                />
                <Route exact path="/about" component={About} />
              </Switch>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default App;
