import Chat from "./components/Chat";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          AI Chat Assistant
        </h1>
        <Chat />
      </div>
    </div>
  );
}

export default App;
