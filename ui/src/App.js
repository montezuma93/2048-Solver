import React from 'react';
import KeyboardEventHandler from 'react-keyboard-event-handler';
import './index.css';

const gameBoardStyle = {
    width: '400px',
    height: '400px',
    tableLayout: 'fixed',
    background: 'pink',
};
const cellStyle = {
    width: '100px',
    height: '100px',
    border: '2px solid black',
    textAlign: 'center',
    fontSize: '50px',
};

class App extends React.Component {
    constructor() {
        super();
        this.state = {
            board: [[0, 0, 0, 0], [0, 0, 0, 0], [0,0,0,0], [0,0,0,0]]
        };
    }

    render() {
        return (
            <div className="App">
                <header className="2048">
                    <h1 className="App-title">2048</h1>
                </header>
                <div onKeyPress={(event) => this.add(event)}>
                    <KeyboardEventHandler
                        handleKeys={['left', 'right', 'up', 'down']}
                        onKeyEvent={(key, e) => this.executeKey(key)} />
                    <table style={gameBoardStyle}>
                    <tbody>
                        {this.createGameboard(this.state.board)}
                    </tbody>
                    </table>
                </div>
            </div>
        );
    }

    createGameboard = (board) => {
        let gameboard = []
        // Outer loop to create parent
        for (let i = 0; i < board.length; i++) {
            let children = []
            //Inner loop to create children
            for (let j = 0; j < board[i].length; j++) {
                children.push(<td style={cellStyle}>{board[i][j]}</td>)
            }
            //Create the parent and add the children
            gameboard.push(<tr style={cellStyle}>{children}</tr>)
        }
        return gameboard
    }

    componentWillMount() {
        const that = this;
        return fetch('http://127.0.0.1:5000/create_board', {
            method: 'POST',
            headers: {
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Authorization, Content-Type',
                'Access-Control-Allow-Origin': "*",
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then((response) => response.json())
            .then(function(data) {
                    that.setState({ board: data });
            });
    }
    executeKey = (key) => {
        const that = this;
        console.log(`do something upon keydown event of ${key}`)
        return fetch('http://127.0.0.1:5000/execute_key', {
            method: 'POST',
            headers: {
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Authorization, Content-Type',
                'Access-Control-Allow-Origin': "*",
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "key": key,
            })
        })
            .then((response) => response.json())
            .then(function(data) {
                if(data == "GAME_OVER") {
                    console.log("GAME_OVER")
                } else {
                    that.setState({ board: data });
                }
            });
    };
}


export default App;