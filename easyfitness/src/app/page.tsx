
import Nav from './components/navbar';
import { Button } from "@nextui-org/react";
import Link from "next/link";
import Footer from './components/footer';

export default function Home() {
  return (
    <div className="home-root">
      <Nav />
      <div className="home-hero">
        <h1 className="home-title">EasyFitness</h1>
      <Button as={Link} size="lg" href="/login" className="btn home-cta">
      Sign Up
    </Button>
      </div>
  <Footer />
    </div>
  );
}