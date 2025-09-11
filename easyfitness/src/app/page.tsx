import Nav from './navbar';

export default function Home() {
  return (
    <div>
      <Nav />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">EasyFitness</h1>
        <div className="text-center">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Track Workouts</h2>
              <p className="text-gray-600">Log your exercises and monitor your progress</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Set Goals</h2>
              <p className="text-gray-600">Define and achieve your fitness objectives</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">View Stats</h2>
              <p className="text-gray-600">Analyze your performance with detailed insights</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}