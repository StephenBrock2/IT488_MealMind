import React from "react";
import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import RecipeSelectDialog from "../RecipeSelectDialog";

describe("RecipeSelectDialog", () => {
  afterEach(() => {
    cleanup();
  });

  const defaultProps = {
    open: true,
    recipes: [],
    loading: false,
    onClose: vi.fn(),
    onSelect: vi.fn(),
  };

  it("renders the dialog title when open", () => {
    render(<RecipeSelectDialog {...defaultProps} />);

    expect(screen.getByText(/select a recipe/i)).toBeInTheDocument();
  });

  it("does not render dialog content when open is false", () => {
    render(<RecipeSelectDialog {...defaultProps} open={false} />);

    expect(screen.queryByText(/select a recipe/i)).not.toBeInTheDocument();
  });

  it("shows loading state when loading is true", () => {
    render(
      <RecipeSelectDialog
        {...defaultProps}
        loading={true}
      />
    );

    expect(screen.getByText(/loading recipes/i)).toBeInTheDocument();
  });

  it("shows empty state when there are no recipes and not loading", () => {
    render(
      <RecipeSelectDialog
        {...defaultProps}
        recipes={[]}
        loading={false}
      />
    );

    expect(
      screen.getByText(/no saved recipes available/i)
    ).toBeInTheDocument();
  });

  it("renders recipe list when recipes are provided", () => {
    const recipes = [
      { id: 1, title: "Chicken Alfredo", cook_time: 20 },
      { id: 2, title: "Tacos", cook_time: 15 },
    ];

    render(
      <RecipeSelectDialog
        {...defaultProps}
        recipes={recipes}
      />
    );

    expect(screen.getByText("Chicken Alfredo")).toBeInTheDocument();
    expect(screen.getByText("Tacos")).toBeInTheDocument();
    expect(screen.getByText(/cook time: 20 min/i)).toBeInTheDocument();
    expect(screen.getByText(/cook time: 15 min/i)).toBeInTheDocument();
  });

  it("shows fallback text when recipe has no cook time", () => {
    const recipes = [{ id: 1, title: "Fruit Salad" }];

    render(
      <RecipeSelectDialog
        {...defaultProps}
        recipes={recipes}
      />
    );

    expect(screen.getByText("Fruit Salad")).toBeInTheDocument();
    expect(screen.getByText(/no cook time listed/i)).toBeInTheDocument();
  });

  it("calls onSelect when a recipe is clicked", () => {
    const onSelect = vi.fn();
    const recipes = [{ id: 1, title: "Chicken Alfredo", cook_time: 20 }];

    render(
      <RecipeSelectDialog
        {...defaultProps}
        recipes={recipes}
        onSelect={onSelect}
      />
    );

    fireEvent.click(screen.getByText("Chicken Alfredo"));

    expect(onSelect).toHaveBeenCalledTimes(1);
    expect(onSelect).toHaveBeenCalledWith(recipes[0]);
  });

  it("calls onClose when Cancel is clicked", () => {
    const onClose = vi.fn();

    render(
      <RecipeSelectDialog
        {...defaultProps}
        onClose={onClose}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /cancel/i }));

    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
