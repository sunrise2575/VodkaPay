import "./App.css";

function App() {
  return (
    <div className="h-screen py-16 bg-gradient-to-br from-sky-50 to-gray-200 grid place-content-center">
      <div className="bg-white p-6 rounded-md">
        <div className="text-2xl font-bold">VodkaPay</div>
        <div className="flex flex-col gap-4 pt-6">
          <button className="border-2 rounded-lg text-xl py-4 px-12 text-center">New User</button>
          <button className="border-2 rounded-lg text-xl py-4 px-12 text-center">Pay</button>
        </div>
      </div>
    </div>
  );
}

export default App;
