import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link} from "@heroui/react";

export default function Nav() {
  return (
    <Navbar 
      className="nav-root">
      {/* Left: Brand/Logo centered in left section */}
      <NavbarContent justify="center" className="nav-left">
        <NavbarBrand>
          <Link href="/" className="nav-brand">EasyFitness</Link>
        </NavbarBrand>
      </NavbarContent>
        
      {/* Center: Navigation Headers */}
      <NavbarContent className="nav-center" justify="center">
        <NavbarItem>
          <Link as={Link} href="/mylog" color="foreground" className="nav-link">
            My Log
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link aria-current="page" href="/routines" className="nav-link">
            Routines
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/Nutrition" className="nav-link">
            Nutrition
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/Progress" className="nav-link">
            Progress
          </Link>
        </NavbarItem>
      </NavbarContent>

  
    </Navbar>
  );
}
