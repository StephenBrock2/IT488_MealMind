import { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import KeyboardArrowLeftIcon from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";

const slides = [
  {
    id: 1,
    eyebrow: "Trending now",
    title: "Justin's famous salad",
    author: "By Justin McLinn",
    image:
      "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1600&q=80",
  },
  {
    id: 2,
    eyebrow: "Fresh ideas",
    title: "Creamy pasta\nfor weeknights",
    author: "By Noah Acton",
    image:
      "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=1600&q=80",
  },
  {
    id: 3,
    eyebrow: "Popular pick",
    title: "Berry pancakes\nfor breakfast",
    author: "By Bing Liang Lu",
    image:
      "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=1600&q=80",
  },
  {
    id: 4,
    eyebrow: "Chef favorite",
    title: "Chicken alfredo\nmade simple",
    author: "By Stephen Brock",
    image:
      "https://images.unsplash.com/photo-1515516969-d4008cc6241a?auto=format&fit=crop&w=1600&q=80",
  },
];

export default function HeroCarousel() {
  const [activeStep, setActiveStep] = useState(0);
  const maxSteps = slides.length;

  const handleNext = () => {
    setActiveStep((prev) => (prev + 1) % maxSteps);
  };

  const handleBack = () => {
    setActiveStep((prev) => (prev - 1 + maxSteps) % maxSteps);
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % maxSteps);
    }, 10000);

    return () => clearInterval(timer);
  }, [maxSteps]);

  const slide = slides[activeStep];

  return (
    <Box
      sx={{
        position: "relative",
        borderRadius: 5,
        overflow: "hidden",
        minHeight: { xs: 260, md: 360 },
        width: {xl: 1100},
        mb: 4,
        backgroundImage: `url(${slide.image})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <Box
        sx={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(90deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.32) 40%, rgba(0,0,0,0.10) 100%)",
        }}
      />

      <Box
        sx={{
          position: "relative",
          zIndex: 1,
          px: { xs: 3, md: 5 },
          py: { xs: 4, md: 8 },
          color: "white",
          maxWidth: 520,
        }}
      >
        <Typography
          sx={{
            color: "#F6784C",
            fontWeight: 700,
            mb: 1,
            fontSize: { xs: 22, md: 30 },
          }}
        >
          {slide.eyebrow}
        </Typography>

        <Typography
          sx={{
            fontWeight: 800,
            lineHeight: 1.05,
            whiteSpace: "pre-line",
            fontSize: { xs: "2rem", md: "3.4rem" },
            mb: 1.5,
          }}
        >
          {slide.title}
        </Typography>

        <Typography sx={{ fontSize: { xs: 18, md: 28 }, opacity: 0.95 }}>
          {slide.author}
        </Typography>
      </Box>

      <Stack
        direction="row"
        spacing={1}
        alignItems="center"
        sx={{
          position: "absolute",
          left: "50%",
          bottom: 22,
          transform: "translateX(-50%)",
          zIndex: 2,
        }}
      >
        <IconButton
          onClick={handleBack}
          sx={{
            color: "white",
            border: "1px solid rgba(255,255,255,0.7)",
            width: 42,
            height: 42,
          }}
        >
          <KeyboardArrowLeftIcon />
        </IconButton>

        <Stack direction="row" spacing={0.8}>
          {slides.map((item, index) => (
            <Box
              key={item.id}
              onClick={() => setActiveStep(index)}
              sx={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                cursor: "pointer",
                backgroundColor:
                  index === activeStep ? "white" : "rgba(255,255,255,0.55)",
              }}
            />
          ))}
        </Stack>

        <IconButton
          onClick={handleNext}
          sx={{
            color: "white",
            border: "1px solid rgba(255,255,255,0.7)",
            width: 42,
            height: 42,
          }}
        >
          <KeyboardArrowRightIcon />
        </IconButton>
      </Stack>
    </Box>
  );
}