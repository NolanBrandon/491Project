
import Nav from './navbar';
import { Button } from "@heroui/react";
import Link from "next/link";

export default function Home() {
  return (
    <div>
      <Nav />
      <div className="flex flex-col justify-center items-center min-h-[80vh]">
        <h1 className="text-4xl font-bold text-center font-akira">EasyFitness</h1>
        <Button as={Link} href="/login" color="primary" variant="solid" className="mt-6">
          Sign Up
        </Button>
      </div>
    </div>
  );
}