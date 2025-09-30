import { Link } from "@heroui/react";

export default function Footer() {
  return (
    <footer className="mt-12 border-t border-gray-300">
      <nav className="py-6 text-lg flex items-center">
        <ul className="flex flex-1 items-center list-none m-0 p-0">
          <li>
            <Link color="foreground" href="/contact" className="text-xl px-4 py-2">
              Contact Us
            </Link>
          </li>
        </ul>
        {/* Center: Empty for layout balance */}
        <div className="hidden sm:flex gap-6 flex-1 justify-center" />
        {/* Right: Empty for layout balance */}
        <div className="flex-1" />
      </nav>
    </footer>
  );
}
