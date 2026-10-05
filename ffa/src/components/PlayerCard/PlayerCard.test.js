import { render, screen } from "@testing-library/react";
import PlayerCard from "./PlayerCard";

test.each([
  [19.1, "19.10"],
  [0, "0.00"],
  [null, "Unavailable"],
])("displays weekly points for %s", (points, expected) => {
  render(
    <PlayerCard
      player={{
        id: 123,
        name: "Test Player",
        position: "RB",
        scoringPeriodId: 4,
        points,
      }}
    />,
  );

  expect(screen.getByText(`Week 4 points: ${expected}`)).toBeInTheDocument();
});
