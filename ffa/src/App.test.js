import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

const originalFetch = global.fetch;

const teams = [
  { id: 1, name: "Team One" },
  { id: 2, name: "Team Two" },
];

const rosters = {
  1: [
    { id: 101, name: "Josh Allen", position: "QB" },
    { id: 102, name: "Chase Brown", position: "RB" },
  ],
  2: [{ id: 201, name: "Patrick Mahomes", position: "QB" }],
};

beforeEach(() => {
  global.fetch = jest.fn(async (url) => {
    if (url === "/api/teams") {
      return { ok: true, json: async () => teams };
    }

    const match = url.match(/^\/api\/teams\/(\d+)\/roster$/);
    const players = match && rosters[match[1]];

    if (players) {
      return {
        ok: true,
        json: async () => ({
          teamId: Number(match[1]),
          players,
        }),
      };
    }

    throw new Error(`Unexpected request: ${url}`);
  });
});

afterEach(() => {
  global.fetch = originalFetch;
});

async function selectTeam(id = "1") {
  const selector = await screen.findByRole("combobox", {
    name: /my team/i,
  });

  await userEvent.selectOptions(selector, id);

  const name = id === "1" ? "Josh Allen" : "Patrick Mahomes";
  await screen.findByRole("heading", { name });

  return selector;
}

test("shows a selection prompt without loading a roster initially", async () => {
  render(<App />);
  await screen.findByRole("combobox", { name: /my team/i });

  expect(
    screen.getByText("Select a team to view its roster."),
  ).toBeInTheDocument();
  expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);
  expect(global.fetch).toHaveBeenCalledTimes(1);
});

test("loads the selected team's roster", async () => {
  render(<App />);
  await selectTeam();

  expect(global.fetch).toHaveBeenCalledWith(
    "/api/teams/1/roster",
    expect.objectContaining({ signal: expect.anything() }),
  );
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(2);
  expect(
    screen.getByRole("heading", { name: "Chase Brown" }),
  ).toBeInTheDocument();
});

test("combines case-insensitive search with position filtering", async () => {
  render(<App />);
  await selectTeam();

  const search = screen.getByRole("searchbox", { name: /search players/i });
  const position = screen.getByRole("combobox", { name: /^position$/i });

  await userEvent.type(search, " JOSH ");
  await userEvent.selectOptions(position, "QB");

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);
  expect(
    screen.getByRole("heading", { name: "Josh Allen" }),
  ).toBeInTheDocument();

  await userEvent.selectOptions(position, "RB");

  expect(screen.getByText("No players found.")).toBeInTheDocument();
  expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);

  await userEvent.clear(search);

  expect(
    screen.getByRole("heading", { name: "Chase Brown" }),
  ).toBeInTheDocument();
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);

  await userEvent.selectOptions(position, "ALL");

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(2);
});

test("switching teams resets filters and replaces the roster", async () => {
  render(<App />);
  await selectTeam();

  const search = screen.getByRole("searchbox", { name: /search players/i });
  const position = screen.getByRole("combobox", { name: /^position$/i });

  await userEvent.type(search, "chase");
  await userEvent.selectOptions(position, "RB");
  await selectTeam("2");

  expect(search).toHaveValue("");
  expect(position).toHaveValue("ALL");
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);
  expect(
    screen.queryByRole("heading", { name: "Chase Brown" }),
  ).not.toBeInTheDocument();
});

test("clearing the team selection removes the roster", async () => {
  render(<App />);
  const selector = await selectTeam();

  await userEvent.selectOptions(selector, "");

  await waitFor(() => {
    expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);
  });
  expect(
    screen.getByText("Select a team to view its roster."),
  ).toBeInTheDocument();
});

test("shows an error and removes the old roster when a request fails", async () => {
  render(<App />);
  const selector = await selectTeam();

  global.fetch.mockResolvedValueOnce({ ok: false });
  await userEvent.selectOptions(selector, "2");

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Unable to load roster.",
  );
  expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);
  expect(screen.queryByText("No players found.")).not.toBeInTheDocument();
});
