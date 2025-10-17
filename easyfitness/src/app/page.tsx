import { Button } from "@nextui-org/react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="home-root">
      <main className="home-hero content-grow">
        <h1 className="home-title">EasyFitness</h1>
        <div className="flex flex-col sm:flex-row gap-4">
          <Button
            as={Link}
            size="lg"
            href="/signup"
            role="button"
            className="btn home-cta"
            aria-label="Sign Up"
          >
            Sign Up
          </Button>
          <Button
            as={Link}
            size="lg"
            href="/login"
            role="button"
            className="btn home-cta"
            aria-label="Log In"
          >
            Log In
          </Button>
        </div>
      </main>
    </div>
  );
}