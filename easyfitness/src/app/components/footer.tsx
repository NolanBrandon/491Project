import { Link } from "@heroui/react";

export default function Footer() {
  return (
    <footer className="footer-root">
      <nav className="footer-nav">
        {/* Left: Only Contact Us link */}
        <div className="footer-left">
          <Link href="/contact" color="foreground" className="footer-link">Contact Us</Link>
        </div>

        {/* Center spacer */}
        <div className="footer-center" />

        {/* Right spacer */}
        <div className="footer-right" />
      </nav>
    </footer>
  );
}
