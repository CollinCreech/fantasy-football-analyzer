import "./App.css";
import PlayerCard from "./components/PlayerCard/PlayerCard";

function App() {
  const player = {
    name: "Ja'Marr Chase",
    position: "WR",
    team: "CIN",
    points: 24.7,
    image: "https://a.espncdn.com/i/headshots/nfl/players/full/4362628.png",
  };

  return (
    <div className="App">
      <h1>My Fantasy Team</h1>

      <PlayerCard player={player} />
    </div>
  );
}

export default App;