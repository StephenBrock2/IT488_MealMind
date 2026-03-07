import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
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

vi.mock("../../components/CreateRecipeDialog", () => ({
  default: () => <div data-testid="create-recipe-dialog" />,
}));

function renderHome() {
  return render(
    <MemoryRouter>
      <Home />
    </MemoryRouter>
  );
}

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

  it("fetches saved recipes on initial page load", async () => {
    mockFetchJson([], true, 200);

    renderHome();

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    expect(global.fetch).toHaveBeenCalledWith("/api/recipe_list");
  });

  it("shows loading UI while fetching", async () => {
    let resolveFetch;
    global.fetch = vi.fn(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        })
    );

    renderHome();

    expect(screen.getByText(/Loading recipes/i)).toBeInTheDocument();

    resolveFetch({
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue([]),
    });

    await waitFor(() => {
      expect(screen.queryByText(/Loading recipes/i)).not.toBeInTheDocument();
    });
  });

  it("renders up to 6 recipes in Your Recipes and 3 in Recommended when API returns more than 6", async () => {
    const recipes = Array.from({ length: 10 }).map((_, i) => ({
      id: String(i + 1),
      title: `Recipe ${i + 1}`,
    }));

    mockFetchJson(recipes, true, 200);

    renderHome();

    const cards = await screen.findAllByTestId("recipe-card");
    expect(cards).toHaveLength(9);
  });

  it("shows empty-state message when API returns 404", async () => {
    mockFetchStatus(404);

    renderHome();

    await waitFor(() => expect(global.fetch).toHaveBeenCalled());

    expect(screen.getByText(/No recipes saved\./i)).toBeInTheDocument();
    expect(screen.getByText(/No recommended recipes available\./i)).toBeInTheDocument();
  });

  it("shows empty-state message when fetch throws", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("Network down"));

    renderHome();

    expect(await screen.findByText(/No recipes saved\./i)).toBeInTheDocument();
    expect(screen.getByText(/No recommended recipes available\./i)).toBeInTheDocument();
  });

  it("renders the View All Recipes button", async () => {
    mockFetchJson([], true, 200);

    renderHome();

    expect(
      screen.getByRole("button", { name: /view all recipes/i })
    ).toBeInTheDocument();
  });
});