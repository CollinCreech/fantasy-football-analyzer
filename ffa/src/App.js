import "./App.css";
import PlayerCard from "./components/PlayerCard/PlayerCard";
import { players } from "./data/players";
import { useEffect, useState } from "react";

function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedPosition, setSelectedPosition] = useState("ALL");
  const [teams, setTeams] = useState([]);
  const [selectedTeamId, setSelectedTeamId] = useState("");
  const [teamsLoading, setTeamsLoading] = useState(true);
  const [teamsError, setTeamsError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function loadTeams() {
      try {
        const response = await fetch("/api/teams", {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error("Unable to load league teams.");
        }

        const data = await response.json();
        setTeams(data);
      } catch (error) {
        if (error.name !== "AbortError") {
          setTeamsError("Unable to load league teams. Try refreshing the page.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setTeamsLoading(false);
        }
      }
    }

    loadTeams();
    return () => controller.abort();
  }, []);

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
        {teamsLoading && <p role="status">Loading league teams…</p>}
        {teamsError && <p role="alert">{teamsError}</p>}

        {!teamsLoading && !teamsError && (
          <>
            <label htmlFor="team-selector">My team</label>
            <select
              id="team-selector"
              value={selectedTeamId}
              onChange={(event) => setSelectedTeamId(event.target.value)}
            >
              <option value="">Select your team</option>
              {teams.map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))}
            </select>

            {teams.length === 0 && <p>No league teams found.</p>}
          </>
        )}
      </div>

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
