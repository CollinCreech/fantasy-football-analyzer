import "./App.css";
import PlayerCard from "./components/PlayerCard/PlayerCard";
import { players } from "./data/players";
import { useState } from "react";

function App() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPlayers = players.filter((player) =>
    player.name.toLowerCase().includes(searchTerm.trim().toLowerCase()),
  );

  return (
    <div className="App">
      <h1>Fantasy Football Analyzer</h1>
      <p>Sample data for demonstration. Not current player statistics.</p>

      <div className="player-search">
        <label htmlFor="player-search">Search players</label>
        <input
          id="player-search"
          type="search"
          placeholder="Enter a player name"
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
        />
      </div>

      {filteredPlayers.length === 0 && <p role="status">No players found.</p>}

      <div className="player-list">
        {filteredPlayers.map((player) => (
          <PlayerCard key={player.id} player={player} />
        ))}
      </div>
    </div>
  );
}

export default App;
