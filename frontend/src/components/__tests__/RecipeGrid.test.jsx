import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import RecipeGrid from "../RecipeGrid";

describe("RecipeGrid", () => {
  it("renders demo recipes when no recipes prop is provided", () => {
    render(<RecipeGrid />);

    const titles = screen.getAllByText("Russian Salad");
    expect(titles).toHaveLength(6);
  });

  it("renders provided recipes instead of demo", () => {
    const recipes = [
      {
        id: "1",
        title: "Chili",
        cookingTimeMinutes: 30,
        rating: 4.5,
        ingredients: [],
        instructions: "Cook it",
      },
    ];

    render(<RecipeGrid recipes={recipes} />);

    expect(screen.getByText("Chili")).toBeInTheDocument();
    expect(screen.getByText("30 min")).toBeInTheDocument();
    expect(screen.getByText("4.5")).toBeInTheDocument();
  });

  it("shows dash when rating is missing", () => {
    const recipes = [
      {
        id: "2",
        title: "No Rating Recipe",
        cookingTimeMinutes: 15,
      },
    ];

    render(<RecipeGrid recipes={recipes} />);

    expect(screen.getByText("No Rating Recipe")).toBeInTheDocument();
    expect(screen.getByText("15 min")).toBeInTheDocument();
    expect(screen.getByText("—")).toBeInTheDocument();
  });

  it("falls back to default image when none provided", () => {
    const recipes = [
      {
        id: "3",
        title: "Image Test",
        cookingTimeMinutes: 20,
      },
    ];

    render(<RecipeGrid recipes={recipes} />);

    const img = screen.getByAltText("Image Test");
    expect(img).toHaveAttribute("src");
  });
});