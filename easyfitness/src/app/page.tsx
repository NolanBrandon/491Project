
import Nav from './components/navbar';
import { Button } from "@nextui-org/react";
import Link from "next/link";
import Footer from './components/footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-[url('/bg.jpg')] bg-cover bg-center">
      <Nav />
      <div className="flex flex-col justify-center items-center min-h-[80vh]">
        <h1 className="text-4xl font-bold text-center font-akira">EasyFitness</h1>
      <Button as={Link} href="/login" className="btn-red mt-6">
      Sign Up
    </Button>
      </div>
  <Footer />
    </div>
  );
}