import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button} from "@heroui/react";

export default function Nav() {
  return (
    <Navbar className="py-6 text-lg">
      {/* Left: Brand/Logo */}
      <NavbarContent justify="start">
        <NavbarBrand>
        </NavbarBrand>
      </NavbarContent>
        

      {/* Center: Navigation Headers */}
      <NavbarContent className="hidden sm:flex gap-6" justify="center">
        <NavbarItem>
          <Link color="foreground" href="/mylog" className="text-xl px-4 py-2">
            My Log
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/routine" className="text-xl px-4 py-2">
            Routine Recommendation
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/calorietrack" className="text-xl px-4 py-2">
            Calorie Tracker
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/calculation" className="text-xl px-4 py-2">
            Calculation
          </Link>
        </NavbarItem>
      </NavbarContent>

  {/* Right: (removed Login/Sign Up, keep empty for layout balance) */}
  <NavbarContent justify="end" />
    </Navbar>
  );
}
