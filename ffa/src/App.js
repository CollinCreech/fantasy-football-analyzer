import "./App.css";
import PlayerCard from "./components/PlayerCard/PlayerCard";
import { players } from "./data/players";
import { useState } from "react";

function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedPosition, setSelectedPosition] = useState("ALL");

  const filteredPlayers = players.filter((player) => {
    const matchesSearch = player.name
      .toLowerCase()
      .includes(searchTerm.trim().toLowerCase());

    const matchesPosition =
      selectedPosition === "ALL" || player.position === selectedPosition;

    return matchesSearch && matchesPosition;
  });

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
        <label htmlFor="position-filter">Position</label>
        <select
          id="position-filter"
          value={selectedPosition}
          onChange={(event) => setSelectedPosition(event.target.value)}
        >
          <option value="ALL">All positions</option>
          <option value="QB">Quarterback</option>
          <option value="RB">Running back</option>
          <option value="WR">Wide receiver</option>
          <option value="TE">Tight end</option>
        </select>
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
