import { useEffect, useState } from 'react'
import './App.css'

interface DailyMatchup {
  gamePk: number;
  gameDate: string;
  awayTeam: string;
  homeTeam: string;
  awayPitcher: string;
  homePitcher: string;
  yrfiProbability: number;
}

function App() {
  const [matchups, setMatchups] = useState<DailyMatchup[]>([])

  useEffect(() => {
    fetch('http://localhost:8080/api/matchups/today')
      .then(response => response.json())
      .then((data: DailyMatchup[]) => setMatchups(data))
      .catch(error => console.error("Error fetching matchups:", error))
  }, [])

  return (
    <div className="App">
      <h1>MLB First-Inning Predictor</h1>
      
      {matchups.length === 0 ? (
        <p>Loading matchups or no games scheduled today...</p>
      ) : (
        <div className="matchup-grid">
          {matchups.map(game => (
            <div key={game.gamePk} className="card">
              <h2 id="teams">{game.awayTeam} <br/>@<br/> {game.homeTeam}</h2>
              <hr />
              <p><strong>Away Pitcher:</strong> {game.awayPitcher}</p>
              <p><strong>Home Pitcher:</strong> {game.homePitcher}</p>
              <h3 className={game.yrfiProbability > 50 ? "high-prob" : "low-prob"}>
                YRFI Probability: {game.yrfiProbability}%
              </h3>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App