import "./PlayerCard.css";

function PlayerCard({ player }) {
  return (
    <div className="player-card">
      <div className="player-info">
        <h2>{player.name}</h2>
        {player.position && (
          <p>
            {player.position}
            {player.team ? ` - ${player.team}` : ""}
          </p>
        )}
        <p>
          Week {player.scoringPeriodId} points:{" "}
          {player.points == null ? "Unavailable" : player.points.toFixed(2)}
        </p>{" "}
      </div>
    </div>
  );
}

export default PlayerCard;
