import Nav from '../components/navbar';
import Footer from '../components/footer';

export default function MyLogPage() {
    return (
        <div>
        <Nav />
  <h1 className="h1">My Log</h1>
        <main className="col-span-1 space-y-4">
            <p className="h-[600px] w-[1200px] bg-white p-4 mx-auto mt-16 rounded-lg flex items-center justify-center">LOG</p>
        </main>
    <Footer />
    </div>
    );
    }