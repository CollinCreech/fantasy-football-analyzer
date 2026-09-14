import "./PlayerCard.css";

function PlayerCard({ player }) {
  return (
    <div className="player-card">
      <div className="player-info">
        <h2>{player.name}</h2>
        <p>
          {player.position} - {player.team}
        </p>
        <p>Fantasy Points: {player.points}</p>
      </div>
    </div>
  );
}

export default PlayerCard;