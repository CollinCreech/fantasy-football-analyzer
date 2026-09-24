import "./App.css";
import PlayerCard from "./components/PlayerCard/PlayerCard";
import { players } from "./data/players";

function App() {
  return (
    <div className="App">
      <h1>Fantasy Football Analyzer</h1>
      <p>Sample data for demonstration. Not current player statistics.</p>

      <div className="player-list">
        {players.map((player) => (
          <PlayerCard key={player.id} player={player} />
        ))}
      </div>
    </div>
  );
}

export default App;
