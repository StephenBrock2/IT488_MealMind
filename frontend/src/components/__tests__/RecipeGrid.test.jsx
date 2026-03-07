import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import RecipeGrid from "../RecipeGrid";

describe("RecipeGrid", () => {
  it("renders no recipes when no recipes prop is provided", () => {
    render(<RecipeGrid />);

    expect(screen.queryByTestId("recipe-card")).not.toBeInTheDocument();
  });

  it("renders provided recipes", () => {
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

  it("renders cook_time from backend format", () => {
    const recipes = [
      {
        id: "4",
        title: "Backend Recipe",
        cook_time: 25,
        rating: 4.2,
      },
    ];

    render(<RecipeGrid recipes={recipes} />);

    expect(screen.getByText("Backend Recipe")).toBeInTheDocument();
    expect(screen.getByText("25 min")).toBeInTheDocument();
    expect(screen.getByText("4.2")).toBeInTheDocument();
  });
});