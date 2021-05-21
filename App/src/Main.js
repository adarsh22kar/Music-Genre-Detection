
import React from 'react';
import './Main.css'



class Main extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            genre_detected: [["Genre", "0"], ["Genre", "0"], ["Genre", "0"]],
            data_received: false
        };

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage(ev) {
        ev.preventDefault();

        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);
        // data.append('filename', this.fileName.value);

        fetch('http://localhost:5000/upload', {
            method: 'POST',
            // mode: 'no-cors',
            body: data,
        })
            .then((response) => {
                response.json()
                    .then((body) => {
                        console.warn(body)
                        this.setState({ genre_detected: body, data_received: true })

                    });
            });
    }


    render() {
        return (
            <div className='app'>
                <div className="form">
                    <h2>Select a Music File (.wav)</h2>
                    <br />
                    <form onSubmit={this.handleUploadImage}>
                        <div>
                            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
                        </div>
                        <br />
                        <div>
                            <button>Check</button>
                        </div>
                    </form>
                    {this.state.data_received ?
                        <div className="output">
                            <p className="winner">{this.state.genre_detected[0][0]} {Math.round(this.state.genre_detected[0][1] * 100).toFixed(2)}%</p>
                            {this.state.genre_detected[1] ?
                                <p>{this.state.genre_detected[1][0]} {Math.round(this.state.genre_detected[1][1] * 100).toFixed(2)}%</p> : null}
                            {this.state.genre_detected[2] ?
                                <p>{this.state.genre_detected[2][0]} {Math.round(this.state.genre_detected[2][1] * 100).toFixed(2)}%</p> : null}
                        </div> : null}
                </div>

            </div>


        );
    }
}

export default Main;