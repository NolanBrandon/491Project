import Nav from '../components/navbar';
import Footer from '../components/footer';

export default function RoutinePage() {
    return (
        <div className="page-container blur-bg">
            <Nav />
            <div className="content-grow">
                {/* <h1 className="h1">Routine Recommendation</h1> */}
      {/* You can add routine content here later */}
                <main className="col-span-1 space-y-4">
                    <p className="h-[600px] w-[1200px] bg-white p-4 mx-auto mt-16 rounded-lg flex items-center justify-center">LOG</p>
                </main>
            </div>
            <Footer />
        </div>
    );
}