import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import Home from "../Home";

vi.mock("../assets/mealmind-logo.png", () => ({ default: "logo.png" }));
vi.mock("../assets/default-recipe.svg", () => ({ default: "default.svg" }));

vi.mock("../../components/RecipeGrid", () => ({
  default: ({ recipes = [] }) => (
    <div data-testid="recipe-grid">
      {recipes.map((r) => (
        <div key={r.id} data-testid="recipe-card">
          {r.title}
        </div>
      ))}
    </div>
  ),
}));

vi.mock("../components/CreateRecipeDialog", () => ({
  default: () => <div data-testid="create-recipe-dialog" />,
}));

function mockFetchJson(data, ok = true, status = 200) {
  global.fetch = vi.fn().mockResolvedValue({
    ok,
    status,
    json: vi.fn().mockResolvedValue(data),
  });
}

function mockFetchStatus(status) {
  global.fetch = vi.fn().mockResolvedValue({
    ok: false,
    status,
    json: vi.fn().mockResolvedValue({}),
  });
}

describe("Home", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    global.fetch = vi.fn();

    if (!global.crypto) global.crypto = {};
    if (!global.crypto.randomUUID) {
      global.crypto.randomUUID = vi.fn(() => "test-uuid");
    }
  });

  afterEach(() => {
    cleanup();
  });

  it("fetches saved recipes on initial page load with limit=6", async () => {
    mockFetchJson([], true, 200);

    render(<Home />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    expect(global.fetch).toHaveBeenCalledWith("/api/recipe?limit=6");
  });

  it("shows loading UI while fetching", async () => {
    let resolveFetch;
    global.fetch = vi.fn(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        })
    );

    render(<Home />);

    expect(screen.getByText(/Loading saved recipes/i)).toBeInTheDocument();

    resolveFetch({
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue([]),
    });

    await waitFor(() => {
      expect(screen.queryByText(/Loading saved recipes/i)).not.toBeInTheDocument();
    });
  });

  it("renders up to 6 recipes when API returns more than 6", async () => {
    const recipes = Array.from({ length: 10 }).map((_, i) => ({
      id: String(i + 1),
      title: `Recipe ${i + 1}`,
    }));

    mockFetchJson(recipes, true, 200);

    render(<Home />);

    const cards = await screen.findAllByTestId("recipe-card");
    expect(cards).toHaveLength(6);

    expect(screen.getByText("Recipe 1")).toBeInTheDocument();
    expect(screen.getByText("Recipe 6")).toBeInTheDocument();
    expect(screen.queryByText("Recipe 7")).not.toBeInTheDocument();
  });

  it("shows empty-state message when API returns 404 (no recipes endpoint yet)", async () => {
    mockFetchStatus(404);

    render(<Home />);

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());

    expect(
      screen.getByText(/No saved recipes yet/i)
    ).toBeInTheDocument();

    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("shows error alert when fetch throws", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("Network down"));

    render(<Home />);

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Oops — couldn’t load recipes right now.");
  });

  it("supports API response shape { items: [] }", async () => {
    mockFetchJson(
      { items: [{ id: "a", title: "From Items" }] },
      true,
      200
    );

    render(<Home />);

    expect(await screen.findByText("From Items")).toBeInTheDocument();
  });
});