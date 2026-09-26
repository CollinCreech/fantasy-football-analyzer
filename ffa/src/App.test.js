import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

test("displays all sample players initially", () => {
  render(<App />);

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(10);
  expect(
    screen.getByRole("heading", { name: "Ja'Marr Chase" }),
  ).toBeInTheDocument();
});

test("search ignores capitalization and surrounding spaces", async () => {
  render(<App />);

  const search = screen.getByRole("searchbox", {
    name: /search players/i,
  });

  await userEvent.type(search, " JOSH ");

  expect(
    screen.getByRole("heading", { name: "Josh Allen" }),
  ).toBeInTheDocument();
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);
});

test("shows no results and restores players when search is cleared", async () => {
  render(<App />);

  const search = screen.getByRole("searchbox", {
    name: /search players/i,
  });

  await userEvent.type(search, "zzzz");

  expect(screen.getByRole("status")).toHaveTextContent("No players found.");
  expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);

  await userEvent.clear(search);

  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(10);
});

test("combines position filtering with search and supports all positions", async () => {
  render(<App />);

  const position = screen.getByRole("combobox", { name: /position/i });
  const search = screen.getByRole("searchbox", { name: /search players/i });

  await userEvent.selectOptions(position, "QB");

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(2);
  expect(
    screen.getByRole("heading", { name: "Josh Allen" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("heading", { name: "Patrick Mahomes" }),
  ).toBeInTheDocument();

  await userEvent.type(search, "josh");

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);
  expect(
    screen.getByRole("heading", { name: "Josh Allen" }),
  ).toBeInTheDocument();

  await userEvent.selectOptions(position, "WR");

  expect(screen.getByRole("status")).toHaveTextContent("No players found.");
  expect(screen.queryAllByRole("heading", { level: 2 })).toHaveLength(0);

  await userEvent.selectOptions(position, "ALL");

  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(1);
  expect(
    screen.getByRole("heading", { name: "Josh Allen" }),
  ).toBeInTheDocument();

  await userEvent.clear(search);

  expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(10);
});
