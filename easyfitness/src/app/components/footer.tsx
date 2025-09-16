import { Navbar, NavbarContent, NavbarItem, Link } from "@heroui/react";

export default function Footer() {
  return (
    <footer className="mt-12">
      <Navbar className="py-6 text-lg">
        {/* Left: Empty for layout balance */}
        <NavbarContent justify="start" className="flex-1" />

        {/* Center: Contact Us link */}
        <NavbarContent className="hidden sm:flex gap-6" justify="center">
          <NavbarItem>
            <Link color="foreground" href="/contact" className="text-xl px-4 py-2">
              Contact Us
            </Link>
          </NavbarItem>
        </NavbarContent>

        {/* Right: Empty for layout balance */}
        <NavbarContent justify="end" className="flex-1" />
      </Navbar>
    </footer>
  );
}
