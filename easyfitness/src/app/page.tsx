
import Nav from './components/navbar';
import { Button } from "@nextui-org/react";
import Link from "next/link";
import Footer from './components/footer';

export default function Home() {
  return (
    <div className="home-root">
      <Nav />
      <main className="home-hero content-grow">
        <h1 className="home-title">EasyFitness</h1>
        <Button
          as={Link}
          size="lg"
          href="/login"
          role="button"
          className="btn home-cta"
          aria-label="Sign Up"
        >
          Sign Up
        </Button>
      </main>
      <Footer />
    </div>
  );
}