import { render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import HeroCarousel from "../HeroCarousel";

describe("HeroCarousel", () => {

  it("renders the first slide", () => {
    render(<HeroCarousel />);

    expect(screen.getByText(/Trending now/i)).toBeInTheDocument();
    expect(screen.getByText(/Justin's famous salad/i)).toBeInTheDocument();
  });

  it("moves to next slide when right arrow is clicked", async () => {
    render(<HeroCarousel />);

    const nextButton = screen.getAllByRole("button")[1];

    await userEvent.click(nextButton);

    expect(screen.getByText(/Fresh ideas/i)).toBeInTheDocument();
  });

  it("moves to previous slide when left arrow is clicked", async () => {
    render(<HeroCarousel />);

    const prevButton = screen.getAllByRole("button")[0];

    await userEvent.click(prevButton);

    expect(screen.getByText(/Chef favorite/i)).toBeInTheDocument();
  });

});