import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import SavedRecipesTable from "../SavedRecipesTable";

const recipes = [
  {
    id: "1",
    title: "Spaghetti",
    cook_time: 45,
    instructions: "Cook pasta and sauce",
    ingredients: [
      { name: "pasta", quantity: 1, unit: "lb" },
      { name: "tomato sauce", quantity: 2, unit: "cups" },
    ],
  },
  {
    id: "2",
    title: "Chili",
    cook_time: 60,
    instructions: "Simmer ingredients",
    ingredients: [
      { name: "beans", quantity: 2, unit: "cups" },
      { name: "ground beef", quantity: 1, unit: "lb" },
    ],
  },
];

describe("SavedRecipesTable", () => {

  it("renders recipe titles", () => {
    render(<SavedRecipesTable recipes={recipes} />);

    expect(screen.getByText("Spaghetti")).toBeInTheDocument();
    expect(screen.getByText("Chili")).toBeInTheDocument();
  });

  it("shows empty message when no recipes exist", () => {
    render(<SavedRecipesTable recipes={[]} />);

    expect(screen.getByText(/no saved recipes/i)).toBeInTheDocument();
  });

  it("expands recipe details when clicking expand button", async () => {
    render(<SavedRecipesTable recipes={recipes} />);

    const expandButtons = screen.getAllByRole("button", {
      name: /expand recipe row/i,
    });

    await userEvent.click(expandButtons[0]);

    expect(screen.getByText(/recipe details/i)).toBeInTheDocument();
    expect(screen.getByText(/cook time/i)).toBeInTheDocument();
    expect(screen.getByText(/instructions/i)).toBeInTheDocument();
  });

  it("filters recipes by title", async () => {
    render(<SavedRecipesTable recipes={recipes} />);

    const filterInput = screen.getByLabelText(/filter by title/i);

    await userEvent.type(filterInput, "spa");

    expect(screen.getByText("Spaghetti")).toBeInTheDocument();
    expect(screen.queryByText("Chili")).not.toBeInTheDocument();
  });

});