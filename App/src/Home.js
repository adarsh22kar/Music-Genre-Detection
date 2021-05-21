
import React from 'react'
import Typist from 'react-typist';
import TypistLoop from 'react-typist-loop'
import { useHistory } from 'react-router-dom';
import './Home.css'


export default function Home() {
    const history = useHistory();
    const handleClick = () => history.push('/classifier');
    return (
        <div className="container">
            <div className="textBox">
                <TypistLoop interval={200}>
                    {[
                        'Music Classifier',
                        'Genre Classifier',
                        'Mini Project',
                    ].map(text => <Typist key={text} startDelay={100} className="animateText">
                        {text}
                        <Typist.Backspace count={18} delay={500} />
                    </Typist>)}
                </TypistLoop>
            </div>
            <div className="buttonDiv">
                <button
                    className="button"
                    onClick={handleClick}
                >Get Started</button>
            </div>
        </div>
    )
}
