import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: []
    };
  };

  // Component Lifecycle Method that runs during the Commit Phase and can work with the DOM, run side effects, etc.
  componentDidMount() {
    this.getUsers();
  };

  // AJAX call to connect the client to the server
  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
    .then((res) => { this.setState({ users: res.data }); })
    .catch((err) => { console.log(err); });
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br/>
              <h1 className="title is-1">Users</h1>
              <hr/><br/>
              {
                this.state.users.map((user) => {
                  return (
                    <p
                      key={user.id}
                      className="box title is-4 username"
                    >{ user.username }
                    </p>
                  )
                })
              }
            </div>
          </div>
        </div>
      </section>
    )
  }
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
