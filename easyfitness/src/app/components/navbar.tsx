import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button} from "@heroui/react";

export default function Nav() {
  return (
    <Navbar className="py-8 items-center text-lg border-b border-gray-300">
      {/* Left: Brand/Logo */}
      <NavbarContent justify="start" className="flex-1">
        <NavbarBrand>
          <Link href="/" className="text-2xl font-bold" style={{fontFamily: 'Akira Expanded, sans-serif'}}>EasyFitness</Link>
        </NavbarBrand>
      </NavbarContent>
        

      {/* Center: Navigation Headers */}
      <NavbarContent className="hidden sm:flex gap-6 items-center" justify="center">
        <NavbarItem>
          <Link as={Link} href="/mylog" color="foreground" className="text-xl px-4 py-2" style={{fontFamily: 'Akira Expanded, sans-serif'}}>
            My Log
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link aria-current="page" href="/routine" className="text-xl px-4 py-2" style={{fontFamily: 'Akira Expanded, sans-serif'}}>
            Routine Recommendation
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/calorietrack" className="text-xl px-4 py-2" style={{fontFamily: 'Akira Expanded, sans-serif'}}>
            Calorie Tracker
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/calculation" className="text-xl px-4 py-2" style={{fontFamily: 'Akira Expanded, sans-serif'}}>
            Calculation
          </Link>
        </NavbarItem>
      </NavbarContent>

  {/* Right: (removed Login/Sign Up, keep empty for layout balance) */}
  <NavbarContent justify="end" className="flex-1 items-center" />
    </Navbar>
  );
}
