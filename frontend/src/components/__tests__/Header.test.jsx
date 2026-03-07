import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import Header from "../Header";

const mockNavigate = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

vi.mock("../assets/mealmind-logo.png", () => ({
  default: "/src/assets/mealmind-logo.png",
}));

describe("Header", () => {
  it("renders the MealMind logo", () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>
    );

    const logo = screen.getByAltText(/mealmind logo/i);
    expect(logo).toBeInTheDocument();
    expect(logo).toHaveAttribute("src", "/src/assets/mealmind-logo.png");
  });

  it("navigates to home when the logo is clicked", async () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>
    );

    const logo = screen.getByAltText(/mealmind logo/i);
    await userEvent.click(logo);

    expect(mockNavigate).toHaveBeenCalledWith("/");
  });
});